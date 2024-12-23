import transcode
from typing import Any
from os import path
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox




INPUT_PATH_ARGV = 1
BG_COLOR = "#343a40"




def fit_image(event: tk.Event) -> None:
    """fits image into widget; bind to <Configure> event of widget to use"""

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
        close_image()
        messagebox.showerror("Image too small", "Image width or height is too small to display." + f"\nError message: {ex}")
    
    image_canvas.create_image(
        int(event.width / 2),
        int(event.height / 2),
        image=image_tk,
        anchor="center")



def open_image(image_path) -> None:
    global image_canvas, image, image_ratio

    assert path.exists(image_path), transcode.INVALID_INPUT_PATH_ERR

    image_data: dict[str, int | bytes] = transcode.get_image_data(image_path)
    pixel_list: list[list[int]] = transcode.decode(image_data["width"], image_data["pxdata"])
    pixels: np.ndarray[tuple[int, ...], np.dtype[Any]] = np.array(pixel_list, dtype=np.uint8)

    image = Image.fromarray(pixels)
    image_ratio = image.width / image.height

    if image_canvas != None:
        image_canvas.destroy()
    image_canvas = tk.Canvas(window, bg=BG_COLOR, highlightthickness=0)
    image_canvas.bind("<Configure>", fit_image)
    image_canvas.pack(expand=True, fill="both")
    # enable "Save as...", "Close" buttons in file menu
    file_menu.entryconfigure(2, state="normal")
    file_menu.entryconfigure(3, state="normal")



def open_image_dialog() -> None:
    file_path: str = filedialog.askopenfilename()
    try:
        open_image(file_path)
    except AssertionError:
        pass



def save_image() -> None:
    raise NotImplementedError



def close_image() -> None:
    global image_canvas

    image_canvas.destroy()
    # disable "Save as...", "Close" buttons in file menu
    file_menu.entryconfigure(2, state="disabled")
    file_menu.entryconfigure(3, state="disabled")





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
window_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open...", command=open_image_dialog)
file_menu.add_command(label="Save as...", command=save_image, state="disabled")
file_menu.add_command(label="Close", command=close_image, state="disabled")
file_menu.add_command(label="Quit", command=window.quit)


image_canvas: tk.Canvas | None = None
image: Image.Image
image_ratio: float


try:
    file_path: str = transcode.get_file_path(INPUT_PATH_ARGV)
    open_image(file_path)
except AssertionError:
    pass



window.mainloop()