from sys import argv
import struct


HEADER_LENGTH: int = 2
BLACK_PIXEL: str = "□"
WHITE_PIXEL: str = "■"


with open(argv[1], "rb") as file:
    data: bytes = file.read()

width: int = struct.unpack(">H", data[:HEADER_LENGTH])[0]
pixels: bytes = data[HEADER_LENGTH:]


pxcount: int = 1
column: int = 0

for byte in pixels:
    # check if most left bit is set
    is_pxcount: bool = byte & 0b1000_0000 != 0

    if is_pxcount:
        pxcount = byte & ~(1<<7) # clear most left bit
        continue


    pixel: str = BLACK_PIXEL
    if byte > 1:
        pixel = WHITE_PIXEL
    
    for i in range(pxcount):
        print(pixel, end="")

        column += 1
        if column == width:
            print("") # newline
            column = 0

    pxcount = 1