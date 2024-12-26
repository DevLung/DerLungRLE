"""
Language packs for information and error messages in DerLungRLE utilities.
"""


class LanguagePack():
    """Common base class for all language packs."""

    SHORT = 0
    LONG = 1

    NATIVE_NAME: str
    LANGUAGE_CODE: str

    class Label:
        """label texts"""
        FILE_MENU: str
        FILE_OPEN_BTN: str
        FILE_SAVEAS_BTN: str
        FILE_CLOSE_BTN: str
        QUIT_BTN: str
        OPTIONS_MENU: str
        LANGUAGE_SELECT: str

    class Info:
        """info messages"""
        TRANSCODE_HELP: str
        VIEWER_HELP: tuple[str, str]

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

    NATIVE_NAME = "English (US)"
    LANGUAGE_CODE = "en-us"

    class Label:
        FILE_MENU = "File"
        FILE_OPEN_BTN = "Open..."
        FILE_SAVEAS_BTN = "Save as..."
        FILE_CLOSE_BTN = "Close"
        QUIT_BTN = "Quit"
        OPTIONS_MENU = "Options"
        LANGUAGE_SELECT = "Language"
    
    class Info:
        TRANSCODE_HELP = """
Usage:
    transcode.py MODE INPUTFILE [OUTPUTFILE] [OPTIONS]
Modes:
    -d  --decode    decode INPUTFILE and print pixels to stdout
    -e  --encode    encode OUTPUTFILE (out.bin in same directory as INPUTFILE by default) from INPUTFILE
    -?  --help      show this message
Options:
    --lang      PARAMETER: language code (ISO 639-1), changes language of program
"""
        VIEWER_HELP = ("Help", """Usage:
    viewer.pyw [INPUTFILE] [OPTIONS [PARAMETERS]]
Options:
    --lang      PARAMETER: language code (ISO 639-1), changes language of program
    -?          show this message
""")

    class Error:
        EXCEPTION_PREFIX = "Error message:"
        FILE_TOO_SHORT = "supplied file is too short"
        WIDTH_ZERO = "the image width needs to be >0"
        TOO_LARGE_FOR_WIDTH = "width over 65535 not supported"
        TOO_LARGE_FOR_PXCOUNT = "pxcount value over 127 not supported: please use multiple pxcount-color-pairs"
        INVALID_MODE = "Please supply a valid mode of operation."
        INVALID_INPUT_PATH = "Please supply a valid input file path."
        INVALID_OUTPUT_PATH = "Please supply a valid output file path."
        IMAGE_TOO_SMALL_TO_DISPLAY = ("Image too small", "Image width or height is too small to be displayed.")








class GermanDE(LanguagePack):
    """German (DE) language"""

    NATIVE_NAME = "Deutsch (DE)"
    LANGUAGE_CODE = "de-de"

    class Label:
        FILE_MENU = "Datei"
        FILE_OPEN_BTN = "Öffnen..."
        FILE_SAVEAS_BTN = "Speichern unter..."
        FILE_CLOSE_BTN = "Schließen"
        QUIT_BTN = "Beenden"
        OPTIONS_MENU = "Optionen"
        LANGUAGE_SELECT = "Sprache"
    
    class Info:
        TRANSCODE_HELP = """
Nutzung:
    transcode.py MODUS INPUTFILE [OUTPUTFILE]
Modi:
    -d  --decode    INPUTFILE decodieren und in stdout schreiben
    -e  --encode    OUTPUTFILE aus INPUTFILE codieren (standardmäßig out.bin im gleichen Verzeichnis wie INPUTFILE)
    -?  --help      diese Nachricht anzeigen
Options:
    --lang      PARAMETER: Sprachen-Code (ISO 639-1), ändert die Sprache des Programms
"""
        VIEWER_HELP = ("Hilfe", """Nutzung:
    viewer.pyw [INPUTFILE] [OPTIONEN [PARAMETER]]
Optionen:
    --lang      PARAMETER: Sprachen-Code (ISO 639-1), ändert die Sprache des Programms
    -?          diese Nachricht anzeigen
""")

    class Error:
        EXCEPTION_PREFIX = "Fehlermeldung:"
        FILE_TOO_SHORT = "Datei ist zu kurz"
        WIDTH_ZERO = "die Breite des Bildes muss >0 sein"
        TOO_LARGE_FOR_WIDTH = "Breite über 65535 nicht unterstützt"
        TOO_LARGE_FOR_PXCOUNT = "pxcount Wert über 127 nicht unterstützt: bitte nutze mehrere pxcount-color-Paare"
        INVALID_MODE = "Bitte geben Sie einen gültigen Modus an."
        INVALID_INPUT_PATH = "Bitte geben Sie einen gültigen Input-Dateipfad an."
        INVALID_OUTPUT_PATH = "Bitte geben Sie einen gültigen Output-Dateipfad an."
        IMAGE_TOO_SMALL_TO_DISPLAY = ("Bild zu klein", "Bildbreite oder -höhe ist zu klein, um angezeigt zu werden.")