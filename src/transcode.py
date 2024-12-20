from sys import argv, stderr, exit
from os import path
from typing import Callable, Any
import struct
from colour import Color



# standard definitions
HEADER_SIZE = 2

# program definitions
MODE_ARGV = 1
INPUT_PATH_ARGV = 2
OUTPUT_PATH_ARGV = 3
INVALID_MODE_ERR = "please supply a valid mode of operation"
INVALID_INPUT_PATH_ERR = "please supply a valid input file path"
INVALID_OUTPUT_PATH_ERR = "please supply a valid output file path"
BLACK_PIXEL = "□"
WHITE_PIXEL = "■"
HELP_MSG = """
Usage:
    transcode.py MODE INPUTFILE [OUTPUTFILE]
Modes:
    -d  --decode    decode INPUTFILE and print pixels to stdout
    -e  --encode    encode OUTPUTFILE (out.bin in same directory as INPUTFILE by default) from INPUTFILE    (WIP - not implemented yet)
    -?  --help      show this message
"""




def get_image_data(image_path) -> dict[str, int | bytes]:
    """
    gets image data from a file and splits it into image width information and pixel data
    following the standard defined at https://github.com/DevLung/DerLungRLE)

    Return image data as dict containing
      "width": image width
      "data": pixel data
    """

    with open(image_path, "rb") as file:
        data: bytes = file.read()
    return {
        "width": struct.unpack(">H", data[:HEADER_SIZE])[0],
        "pxdata": data[HEADER_SIZE:]
    }



def color(color_byte: int) -> Color:
    """decodes color byte into Color object (7-bit grayscale)"""

    color_byte_decimal: float = color_byte / 0b0111_1111
    return Color(saturation=0, luminance=color_byte_decimal)



def decode(image_width: int, pixel_data: bytes) -> list[list[Color]]:
    """
    decodes pixel data encoded following the standard defined at https://github.com/DevLung/DerLungRLE)
    into a 2D list of pixels that can easily be iterated over or converted to NumPy array

    image_width
      width of image in pixels
    pixel_data
      DerLungRLE-encoded bytes of pixel data

    Return list of Pixel objects
    """

    pxcount: int = 1
    pixels: list[list[Color]] = [[]]
    column: int = 0

    for byte in pixel_data:
        if byte & 0b1000_0000 != 0: # if most left bit is set
            pxcount = byte & ~(1<<7) # clear most left bit
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



def pixels_to_stdout(pixels: list[list[Color]]) -> None:
    """print a given list of Pixel objects to terminal"""

    for row in pixels:
        for pixel in row:
            if pixel.get_luminance() > 0.5:
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

    assert len(argv) > MODE_ARGV, INVALID_MODE_ERR
    match argv[MODE_ARGV].lower():
        case "-?" | "--help":
            return "HELP"
        case "-d" | "--decode":
            return "DECODE"
        case "-e" | "--encode":
            return "ENCODE"
        case _:
            raise AssertionError(INVALID_MODE_ERR)



def get_file_path(argv_index: int) -> str:
    """
    gets and validates file path from given argv index
    
    Return file path

    Raise AssertionError if file path is invalid
    """

    error_msg: str = INVALID_INPUT_PATH_ERR if argv_index == INPUT_PATH_ARGV else INVALID_OUTPUT_PATH_ERR
    assert len(argv) > argv_index, error_msg
    file_path: str = argv[argv_index]
    assert path.exists(file_path), error_msg
    return file_path



def handle_critical_exception(function: Callable, *args, exception=Exception, status_code=1) -> Any:
    try:
        output: Any = function(*args)
    except exception as ex:
        print(f"{ex}\n{HELP_MSG}", file=stderr)
        exit(status_code)
    return output



def decode_to_stdout(image_path) -> None:
    """
    display image file at given path in terminal
    following the standard defined at https://github.com/DevLung/DerLungRLE)
    """

    image_data: dict[str, int | bytes] = get_image_data(image_path)
    pixels: list[list[Color]] = decode(image_data["width"], image_data["pxdata"])
    pixels_to_stdout(pixels)




if __name__ == "__main__":
    mode: str = handle_critical_exception(get_mode, exception=AssertionError)
    match mode:
        case "HELP":
            print(HELP_MSG)
        case "DECODE":
            input_path: str = handle_critical_exception(get_file_path, INPUT_PATH_ARGV, exception=AssertionError)
            decode_to_stdout(input_path)
        case "ENCODE":
            raise NotImplementedError