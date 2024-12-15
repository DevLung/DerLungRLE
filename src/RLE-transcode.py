from sys import argv, stderr, exit
from os import path
from dataclasses import dataclass
import struct
from colour import Color



# standard definitions
HEADER_SIZE = 2

# program definitions
MODE_ARGV = 1
FILE_PATH_ARGV = 2
ENTER_PATH_PROMPT = "please enter a file path"
INVALID_PATH_ERR = "please supply a valid file path"
BLACK_PIXEL = "□"
WHITE_PIXEL = "■"



@dataclass(repr=True, eq=True)
class Pixel:
    """stores the color of a pixel and if it should be followed by a line break."""
    color: Color
    newline_after: bool = False



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



def decode(image_width: int, pixel_data: bytes) -> list[Pixel]:
    """
    decodes pixel data encoded following the standard defined at https://github.com/DevLung/DerLungRLE)
    into a list of pixels that can easily be displayed

    Return list of Pixel objects
    """

    pxcount: int = 1
    column: int = 0
    pixels: list[Pixel] = []

    for byte in pixel_data:
        # check if most left bit is set
        is_pxcount: bool = byte & 0b1000_0000 != 0
        if is_pxcount:
            pxcount = byte & ~(1<<7) # clear most left bit
            continue

        for _ in range(pxcount):
            column += 1

            newline: bool = False
            if column == image_width:
                newline = True
                column = 0

            pixels.append(Pixel(color(byte), newline))

        pxcount = 1
    return pixels



def pixels_to_stdout(pixels: list[Pixel]) -> None:
    """print a given list of Pixel objects to terminal"""

    for pixel in pixels:
        print_end: str = "\n" if pixel.newline_after else ""
        if pixel.color.get_luminance() > 0.5:
            print(WHITE_PIXEL, end=print_end)
            continue
        print(BLACK_PIXEL, end=print_end)



def get_file_path() -> str:
    """
    gets file path from argv or, if no argv was supplied, asks user to input path into an input field
    
    Return file path

    Raise AssertionError if file path supplied via argv is invalid
    """

    # check argv
    if len(argv) > FILE_PATH_ARGV:
        file_path: str = argv[FILE_PATH_ARGV]
        assert path.exists(file_path), INVALID_PATH_ERR
        return file_path
    
    # use input field
    print(ENTER_PATH_PROMPT)
    while True:
        file_path: str = input(" > ")
        if path.exists(file_path):
            return file_path
        print(INVALID_PATH_ERR, file=stderr)



def decode_to_stdout(image_path) -> None:
    """
    display image file at given path in terminal
    following the standard defined at https://github.com/DevLung/DerLungRLE)
    """

    image_data: dict[str, int | bytes] = get_image_data(image_path)
    pixels: list[Pixel] = decode(image_data["width"], image_data["pxdata"])
    pixels_to_stdout(pixels)




if __name__ == "__main__":
    try:
        file_path: str = get_file_path()
    except AssertionError as ex:
        print(ex, file=stderr)
        exit(1)
    except KeyboardInterrupt:
        exit()

    decode_to_stdout(file_path)