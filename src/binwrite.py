from definitions.standard import DerLungRLE
import definitions.lang as lang


STANDARD = DerLungRLE(lang.EnglishUS)
BLACK = 0b0000_0000
WHITE = 0b0111_1111




filename: str = "a.bin"

data: bytes = bytes([
    *STANDARD.encode_width(10),

    STANDARD.to_pxcount(7), WHITE,
    STANDARD.to_pxcount(3), BLACK,
    STANDARD.to_pxcount(3), WHITE,
    STANDARD.to_pxcount(3), BLACK,
    STANDARD.to_pxcount(2), WHITE,
    STANDARD.to_pxcount(2), BLACK,
    STANDARD.to_pxcount(2), WHITE,
    STANDARD.to_pxcount(5), BLACK,
    STANDARD.to_pxcount(2), WHITE,
    BLACK,
    STANDARD.to_pxcount(2), WHITE,
    STANDARD.to_pxcount(5), BLACK,
    STANDARD.to_pxcount(5), WHITE,
    STANDARD.to_pxcount(5), BLACK,
    STANDARD.to_pxcount(6), WHITE,
    STANDARD.to_pxcount(3), BLACK,
    STANDARD.to_pxcount(8), WHITE,
    BLACK,
    STANDARD.to_pxcount(9), WHITE,
    BLACK,
    STANDARD.to_pxcount(9), WHITE,
    BLACK,
    STANDARD.to_pxcount(5), WHITE,
    STANDARD.to_pxcount(10), BLACK
])




if __name__ == "__main__":
    with open(filename, "wb") as file:
        file.write(data)