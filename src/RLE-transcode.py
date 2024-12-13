from sys import argv, stderr, exit
from dataclasses import dataclass
import struct
from os import path
from colour import Color



HEADER_LENGTH: int = 2
BLACK_PIXEL: str = "□"
WHITE_PIXEL: str = "■"



@dataclass(repr=True, eq=True)
class Pixel:
    """Class for storing the color of a pixel and if it should be followed by a line break."""
    color: Color
    newline_after: bool = False



def get_image_data(image_path) -> dict[str, int | bytes]:
    """
    gets image data from a file and splits it into
    - width information
    - pixel data

    following the standard defined at https://github.com/DevLung/RLE-transcode)
    """

    with open(image_path, "rb") as file:
        data: bytes = file.read()
    return {
        "width": struct.unpack(">H", data[:HEADER_LENGTH])[0],
        "pxdata": data[HEADER_LENGTH:]
    }



def color(color_byte: int) -> Color:
    """decodes color bytes into Color objects (grayscale)"""

    color_byte_decimal: float = color_byte / 0b0111_1111
    return Color(saturation=0, luminance=color_byte_decimal)



def decode(image_width: int, pixel_data: bytes) -> list[Pixel]:
    """
    decodes pixel data encoded following the standard defined at https://github.com/DevLung/RLE-transcode)
    into a list of pixels that can easily be displayed
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



def display_image(pixels: list[Pixel]) -> None:
    for pixel in pixels:
        print_end: str = "\n" if pixel.newline_after else ""
        if pixel.color.get_luminance() > 0.5:
            print(WHITE_PIXEL, end=print_end)
            continue
        print(BLACK_PIXEL, end=print_end)




if __name__ == "__main__":
    # get file path, either...
    if len(argv) > 1: # ...from argv
        file_path: str = argv[1]
        if not path.exists(file_path):
            print("please supply a valid file path", file=stderr)
            exit(1)
    else: # ...or from input field
        print("please enter a file path")
        while True:
            try:
                file_path: str = input(" > ")
                if path.exists(file_path):
                    break
                print("please supply a valid file path", file=stderr)
            except KeyboardInterrupt:
                exit()

    image_data: dict[str, int | bytes] = get_image_data(file_path)
    pixels: list[Pixel] = decode(image_data["width"], image_data["pxdata"])
    display_image(pixels)