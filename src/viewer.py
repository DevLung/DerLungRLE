import definitions.lang as lang
import transcode
from sys import argv, executable, stderr, exit
from os import path
import logging
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import inspect
from subprocess import Popen




DEBUG_ARGV_OPTION = "--debug"
LANG_ARGV_OPTION = "--lang"
HELP_ARGV_OPTION = "-?"
INPUT_PATH_ARGV = 1
BG_COLOR = "#343a40"
LOG_PATH: str = path.realpath(path.join(path.dirname(__file__), "debug.log"))
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(filename)s: %(lineno)d, in %(funcName)s]:  %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    encoding="utf-8",
    filename=LOG_PATH,
    filemode="w"
)
if DEBUG_ARGV_OPTION in argv:
    logging.getLogger().setLevel(logging.DEBUG)
LANG: lang.LanguagePack = lang.EnglishUS()
# if there is enough argvs to fit lang option AND if option flag is supplied AND if there is another argv behind it
if len(argv) > 2 and LANG_ARGV_OPTION in argv and argv.index(LANG_ARGV_OPTION) < len(argv) - 1:
    for _, language in inspect.getmembers(lang, inspect.isclass):
        if not language == lang.LanguagePack and language.LANGUAGE_CODE == argv[argv.index(LANG_ARGV_OPTION) + 1].lower():
            LANG = language






def fit_image(event: tk.Event) -> None:
    """
    fits image into widget; bind to <Configure> event of widget to use
    
    needs a PIL Image object (image: Image.Image)
    and a corresponding aspect ratio (image_ratio: float) in global scope
    """

    global image_tk

    canvas_ratio: float = event.width / event.height
    if canvas_ratio < image_ratio: # if canvas is narrower than image
        width = int(event.width)
        height = int(width / image_ratio)
    else:
        height = int(event.height)
        width = int(height * image_ratio)
    
    try:
        image_tk = ImageTk.PhotoImage(image.resize((width, height), Image.Resampling.NEAREST))
    except ValueError as ex:
        logging.exception(ex)
        close_image()
        messagebox.showerror(
            LANG.Error.IMAGE_TOO_SMALL_TO_DISPLAY[LANG.SHORT],
            LANG.Error.IMAGE_TOO_SMALL_TO_DISPLAY[LANG.LONG] + f"\n{LANG.Error.EXCEPTION_PREFIX} {ex}"
        )
        return
    
    image_canvas.create_image(
        int(event.width / 2),
        int(event.height / 2),
        image=image_tk,
        anchor="center")



def open_image(file_path) -> None:
    """
    gets image file at given path, converts it to PIL Image object
    and puts it (image: Image.Image) and its calculated aspect ratio (image_ratio: float) into global scope

    Raise AssertionError if image path is invalid
    """
    logging.debug(f"opening image {file_path}")

    global image, image_ratio

    assert path.exists(file_path), LANG.Error.INVALID_INPUT_PATH

    image_data: dict[str, int | bytes] = transcode.get_image_data(file_path)
    pixel_list: list[list[int]] = transcode.decode(*image_data.values())

    pixels: np.ndarray[tuple[int, ...], np.dtype[np.uint8]] = np.array(pixel_list, dtype=np.uint8)
    image = Image.fromarray(pixels)
    image_ratio = image.width / image.height
    logging.debug(f"calculated image ratio: {image_ratio}")



def display_image(image_path) -> None:
    """
    calls open_image(image_path) (--> Raise AssertionError of image path is invalid)
    and displays live-fitting image on canvas
    """
    logging.info(f"displaying image {image_path}")

    global image_canvas

    open_image(image_path)

    if image_canvas != None:
        logging.debug("destroying old image canvas")
        image_canvas.destroy()
    logging.debug("displaying image on new image canvas")
    image_canvas = tk.Canvas(window, bg=BG_COLOR, highlightthickness=0)
    image_canvas.bind("<Configure>", fit_image)
    image_canvas.pack(expand=True, fill="both")
    # enable "Save as...", "Close" buttons in file menu
    file_menu.entryconfigure(2, state="normal")
    file_menu.entryconfigure(3, state="normal")



def open_image_dialog() -> None:
    file_path: str = filedialog.askopenfilename()
    try:
        display_image(file_path)
    except AssertionError as ex:
        logging.exception(ex)



def save_image() -> None:
    raise NotImplementedError



def close_image() -> None:
    global image_canvas

    logging.info("closing currently displayed image")
    image_canvas.destroy()
    # disable "Save as...", "Close" buttons in file menu
    file_menu.entryconfigure(2, state="disabled")
    file_menu.entryconfigure(3, state="disabled")



def change_language() -> None:
    logging.debug(f"changing language to {selected_language.get()}")
    if selected_language.get() == LANG.LANGUAGE_CODE:
        logging.debug("Selected language is currently loaded, doing nothing.")
        return
    
    Popen((executable, # interpreter path
        path.realpath(__file__), # this script's path
        LANG_ARGV_OPTION, selected_language.get())) # selected language as argv
    window.quit()






logging.info(f"__main__: {path.realpath(__file__)}")
logging.info(f"language set to '{LANG.NATIVE_NAME}'")
try:
    window = tk.Tk()
    window.title("DerLungRLE Viewer")
    window.config(bg=BG_COLOR)
    window.geometry("800x500")
    window.state("zoomed")
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)



    window_menu = tk.Menu(window)
    window.config(menu=window_menu)

    file_menu = tk.Menu(window_menu)
    window_menu.add_cascade(label=LANG.Label.FILE_MENU, menu=file_menu)
    file_menu.add_command(label=LANG.Label.FILE_OPEN_BTN, command=open_image_dialog)
    file_menu.add_command(label=LANG.Label.FILE_SAVEAS_BTN, command=save_image, state="disabled")
    file_menu.add_command(label=LANG.Label.FILE_CLOSE_BTN, command=close_image, state="disabled")
    file_menu.add_command(label=LANG.Label.QUIT_BTN, command=window.quit)


    options_menu = tk.Menu(window_menu)
    window_menu.add_cascade(label=LANG.Label.OPTIONS_MENU, menu=options_menu)

    language_select = tk.Menu(options_menu)
    options_menu.add_cascade(label=LANG.Label.LANGUAGE_SELECT, menu=language_select)
    selected_language = tk.StringVar(window, value=LANG.LANGUAGE_CODE)
    # add all available languages to menu
    for _, language in inspect.getmembers(lang, inspect.isclass):
        if not language == lang.LanguagePack:
            language_select.add_radiobutton(label=language.NATIVE_NAME,
                                            value=language.LANGUAGE_CODE,
                                            variable=selected_language,
                                            command=change_language)



    image_canvas: tk.Canvas | None = None
    image: Image.Image
    image_ratio: float



    try:
        file_path: str = transcode.get_file_path(INPUT_PATH_ARGV)
        display_image(file_path)
    except AssertionError as ex:
        logging.info("can't find an image supplied via argv (so the following error can probably be ignored)")
        logging.exception(ex)


    if HELP_ARGV_OPTION in argv:
        logging.info("showing help message")
        messagebox.showinfo(*LANG.Info.VIEWER_HELP)



    window.mainloop()
    logging.info("Exiting with status code 0.")


except Exception as ex:
    logging.critical(ex, exc_info=True)
    print(LANG.Error.UNEXPECTED_CRITICAL + f"\n({LANG.Error.EXCEPTION_PREFIX} {repr(ex)})", file=stderr)
    logging.critical("Exiting with status code 1.")
    exit(1)