BLACK: int = 0b0000_0000
WHITE: int = 0b0111_1111

def pxcount(count) -> int:
    assert count <= 127, "value is too big for pxcount"
    return 0b1000_0000 + count


filename: str = "test.bin"

data: bytes = bytes([
    0b0000_0000,
    0b0000_1010,

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


with open(filename, "wb") as file:
    file.write(data)