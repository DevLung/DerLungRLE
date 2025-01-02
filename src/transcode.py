import definitions.standard as standard
import definitions.lang as lang
from sys import argv, stderr, exit
from os import path
from typing import Callable, Any
import logging
import struct
import inspect
from functools import lru_cache




MODE_ARGV = 1
INPUT_PATH_ARGV = 2
OUTPUT_PATH_ARGV = 3
DEBUG_ARGV_OPTION = "--debug"
LANG_ARGV_OPTION = "--lang"
BLACK_PIXEL = "□"
WHITE_PIXEL = "■"
LOG_PATH: str = path.realpath(path.join(path.dirname(__file__), "debug.log"))
LOGGING_LEVEL = logging.INFO
if DEBUG_ARGV_OPTION in argv:
    LOGGING_LEVEL = logging.DEBUG
logging.basicConfig(
    level=LOGGING_LEVEL,
    format="[%(asctime)s] [%(levelname)s] [%(filename)s: %(lineno)d, in %(funcName)s]:  %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    encoding="utf-8",
    filename=LOG_PATH,
    filemode="w"
)
LANG: lang.LanguagePack = lang.EnglishUS()
# if there is enough argvs to fit lang option AND if option flag is supplied AND if there is another argv behind it
if len(argv) > 2 and LANG_ARGV_OPTION in argv and argv.index(LANG_ARGV_OPTION) < len(argv) - 1:
    for _, language in inspect.getmembers(lang, inspect.isclass):
        if not language == lang.LanguagePack and language.LANGUAGE_CODE == argv[argv.index(LANG_ARGV_OPTION) + 1].lower():
            LANG = language
logging.info(f"language set to '{LANG.NATIVE_NAME}'")
STANDARD = standard.DerLungRLE(LANG)




def get_image_data(image_path) -> dict[str, int | bytes]:
    """
    gets image data from a file and splits it into image width information and pixel data
    following the standard defined at https://github.com/DevLung/DerLungRLE)

    Return image data as dict containing
      "width": image width
      "data": pixel data

    Raise AssertionError if file is too short or if width is 0
    """
    logging.debug(f"getting image data from {image_path}")

    with open(image_path, "rb") as file:
        data: bytes = file.read()
    assert len(data) >= STANDARD.HEADER_SIZE + 1, LANG.Error.FILE_TOO_SHORT
    
    image_data: dict[str, int | bytes] = {
        "width": struct.unpack(">H", data[:STANDARD.HEADER_SIZE])[0],
        "pxdata": data[STANDARD.HEADER_SIZE:]
    }
    assert image_data["width"] > 0, LANG.Error.WIDTH_ZERO
    logging.debug(f"read {len(data)} bytes of image data (pixel data: {len(image_data['pxdata'])}B, width={image_data['width']})")
    return image_data



def color(color_byte: int) -> int:
    """decodes color byte into uint8 luminance value (grayscale)"""

    luminance_uint8 = int(color_byte / 0b0111_1111 * 0b1111_1111)
    return luminance_uint8



@lru_cache(maxsize=64)
def decode(image_width: int, pixel_data: bytes) -> list[list[int]]:
    """
    decodes pixel data encoded following the standard defined at https://github.com/DevLung/DerLungRLE)
    into a 2D list of pixel luminance values that can easily be iterated over or converted to NumPy array

    image_width
      width of image in pixels
    pixel_data
      DerLungRLE-encoded bytes of pixel data

    Return list of pixel luminance values
    """
    logging.debug(f"decoding {len(pixel_data)} bytes of pixel data with width={image_width}")

    pxcount: int = 1
    pixels: list[list[int]] = [[]]
    column: int = 0

    for byte in pixel_data:
        if STANDARD.is_pxcount(byte):
            pxcount = STANDARD.from_pxcount(byte)
            continue

        for _ in range(pxcount):
            if column == image_width:
                pixels.append([]) # new row
                column = 0

            pixels[-1].append(color(byte))
            column += 1

        pxcount = 1
    
    # extend last row with black pixels if needed to create a complete pixel grid
    if len(pixels[-1]) < image_width:
        pixels[-1].extend([color(0b0000_0000)
                           for _ in range(image_width - len(pixels[-1]))])
    return pixels



def pixels_to_stdout(pixels: list[list[int]]) -> None:
    """prints a given list of pixel luminances to terminal (black/white only)"""
    logging.debug(f"printing {len(pixels)} rows of {len(pixels[0])} pixels to stdout")

    for row in pixels:
        for pixel in row:
            if pixel > 0b1111_1111 / 2:
                print(WHITE_PIXEL, end="")
                continue
            print(BLACK_PIXEL, end="")
        print() # newline



def get_mode() -> str:
    """
    gets mode of operation from argv

    Return 'DECODE' for decode, 'ENCODE' for encode, 'HELP' for help

    Raise AssertionError if no mode is supplied or if mode is invalid
    """
    logging.debug(f"getting mode of operation from argv[{MODE_ARGV}]")

    assert len(argv) > MODE_ARGV, LANG.Error.INVALID_MODE
    match argv[MODE_ARGV].lower():
        case "-?" | "--help":
            return "HELP"
        case "-d" | "--decode":
            return "DECODE"
        case "-e" | "--encode":
            return "ENCODE"
        case _:
            raise AssertionError(LANG.Error.INVALID_MODE)



def get_file_path(argv_index: int) -> str:
    """
    gets and validates file path from given argv index
    
    Return file path

    Raise AssertionError if file path is invalid
    """
    logging.debug(f"getting file path from argv[{argv_index}]")

    error_msg: str = LANG.Error.INVALID_OUTPUT_PATH if argv_index == OUTPUT_PATH_ARGV else LANG.Error.INVALID_INPUT_PATH
    assert len(argv) > argv_index, error_msg
    file_path: str = path.abspath(argv[argv_index])
    assert path.exists(file_path), error_msg
    return file_path



def handle_critical_exception(function: Callable, *args, exception=Exception, status_code=1) -> Any:
    """
    catches any exceptions of given type in given function,
    logs them, prints them together with a help message to stdout
    and exits the program with the given status code

    function
      the function to handle exceptions in
    *args
      any arguments to be passed to the function
    exception=Exception
      the type of exception to handle
    status_code=1
      the status code to exit with
    """
    logging.debug(f"setting up exception handler for {exception.__name__} in {function.__name__}")
    
    try:
        output: Any = function(*args)
    except exception as ex:
        logging.exception(ex)
        print(ex, file=stderr)
        print(LANG.Info.TRANSCODE_HELP)
        exit(status_code)
    return output



def decode_to_stdout(image_path) -> None:
    """
    displays image file at given path in terminal
    following the standard defined at https://github.com/DevLung/DerLungRLE)
    """
    logging.info(f"decoding {image_path} to stdout")

    image_data: dict[str, int | bytes] = get_image_data(image_path)
    pixels: list[list[int]] = decode(*image_data.values())
    pixels_to_stdout(pixels)




def main() -> None:
    mode: str = handle_critical_exception(get_mode, exception=AssertionError)
    logging.info(f"running {mode}")
    match mode:
        case "HELP":
            print(LANG.Info.TRANSCODE_HELP)
        case "DECODE":
            input_path: str = handle_critical_exception(get_file_path, INPUT_PATH_ARGV, exception=AssertionError)
            handle_critical_exception(decode_to_stdout, input_path, exception=AssertionError)
        case "ENCODE":
            raise NotImplementedError


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logging.critical(ex, exc_info=True)
        print(LANG.Error.UNEXPECTED_CRITICAL + f"\n({LANG.Error.EXCEPTION_PREFIX} {repr(ex)})", file=stderr)
        exit(1)