"""
Language packs for information and error messages in DerLungRLE utilities.
"""



class LanguagePack():
    """Common base class for all language packs."""

    SHORT = 0
    LONG = 1

    class Label:
        """label texts"""
        FILE_MENU: str
        FILE_OPEN_BTN: str
        FILE_SAVEAS_BTN: str
        FILE_CLOSE_BTN: str
        QUIT_BTN: str

    class Info:
        """info messages"""
        TRANSCODE_HELP: str

    class Error:
        """error messages"""
        EXCEPTION_PREFIX: str
        FILE_TOO_SHORT: str
        WIDTH_ZERO: str
        TOO_LARGE_FOR_WIDTH: str
        TOO_LARGE_FOR_PXCOUNT: str
        INVALID_MODE: str
        INVALID_INPUT_PATH: str
        INVALID_OUTPUT_PATH: str
        IMAGE_TOO_SMALL_TO_DISPLAY: tuple[str, str]




class EnglishUS(LanguagePack):
    """English (US) language"""

    class Label:
        FILE_MENU = "File"
        FILE_OPEN_BTN = "Open..."
        FILE_SAVEAS_BTN = "Save as..."
        FILE_CLOSE_BTN = "Close"
        QUIT_BTN = "Quit"
    
    class Info:
        TRANSCODE_HELP = """
Usage:
    transcode.py MODE INPUTFILE [OUTPUTFILE]
Modes:
    -d  --decode    decode INPUTFILE and print pixels to stdout
    -e  --encode    encode OUTPUTFILE (out.bin in same directory as INPUTFILE by default) from INPUTFILE    (WIP - not implemented yet)
    -?  --help      show this message
"""

    class Error:
        EXCEPTION_PREFIX = "Error message:"
        FILE_TOO_SHORT = "supplied file is too short"
        WIDTH_ZERO = "the image width needs to be >0"
        TOO_LARGE_FOR_WIDTH = "width over 65535 not supported"
        TOO_LARGE_FOR_PXCOUNT = "pxcount value over 127 not supported: use multiple pxcount-color-pairs"
        INVALID_MODE = "please supply a valid mode of operation"
        INVALID_INPUT_PATH = "please supply a valid input file path"
        INVALID_OUTPUT_PATH = "please supply a valid output file path"
        IMAGE_TOO_SMALL_TO_DISPLAY = ("Image too small", "Image width or height is too small to be displayed.")