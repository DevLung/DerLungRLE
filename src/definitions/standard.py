"""
DerLungRLE encoding standard definitions following the definition here: https://github.com/DevLung/DerLungRLE
"""


import definitions.lang as lang


class DerLungRLE:
    """DerLungRLE encoding standard definitions following the definition here: https://github.com/DevLung/DerLungRLE"""
    def __init__(self, msg_lang: lang.LanguagePack) -> None:
        self.MSG: lang.LanguagePack = msg_lang



    HEADER_SIZE = 2 # bytes



    def encode_width(self, width: int) -> bytes:
        """
        encodes given width value following the standard

        Raise AssertionError if value is too small or too large to be converted to width bytes
        """
        assert width > 0, self.MSG.Error.WIDTH_ZERO
        assert width <= 0b1111_1111_1111_1111, self.MSG.Error.TOO_LARGE_FOR_WIDTH
        return width.to_bytes(2, "big")
    

    def is_pxcount(self, byte: int) -> bool:
        """Return if given byte is a pxcount byte"""
        return byte & 0b1000_0000 != 0 # if first bit is set


    def to_pxcount(self, count: int) -> int:
        """
        creates pxcount byte from a given value
        
        Raise AssertionError if value is too large to be converted to pxcount byte
        """
        assert count <= 0b0111_1111, self.MSG.Error.TOO_LARGE_FOR_PXCOUNT
        return 0b1000_0000 + count
    

    def from_pxcount(self, byte: int) -> int:
        """converts pxcount byte to int"""
        return byte & ~(1<<7) # clear first bit