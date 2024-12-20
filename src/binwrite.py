BLACK = 0b0000_0000
WHITE = 0b0111_1111

def encode_width(width: int) -> bytes:
    assert width <= 0b1111_1111_1111_1111, "width over 65535 not supported"
    return width.to_bytes(2, "big")

def pxcount(count) -> int:
    assert count <= 0b0111_1111, "pxcount value over 127 not supported: use multiple pxcount-color-pairs"
    return 0b1000_0000 + count




filename: str = "a.bin"

data: bytes = bytes([
    *encode_width(10),

    pxcount(7), WHITE,
    pxcount(3), BLACK,
    pxcount(3), WHITE,
    pxcount(3), BLACK,
    pxcount(2), WHITE,
    pxcount(2), BLACK,
    pxcount(2), WHITE,
    pxcount(5), BLACK,
    pxcount(2), WHITE,
    BLACK,
    pxcount(2), WHITE,
    pxcount(5), BLACK,
    pxcount(5), WHITE,
    pxcount(5), BLACK,
    pxcount(6), WHITE,
    pxcount(3), BLACK,
    pxcount(8), WHITE,
    BLACK,
    pxcount(9), WHITE,
    BLACK,
    pxcount(9), WHITE,
    BLACK,
    pxcount(5), WHITE,
    pxcount(10), BLACK
])




if __name__ == "__main__":
    with open(filename, "wb") as file:
        file.write(data)