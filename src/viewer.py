from numpy._typing._array_like import NDArray
import transcode
import numpy as np
from typing import Any
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog




INPUT_PATH_ARGV = 1
BG_COLOR = "#343a40"




def fit_image(event) -> None:
    global image_tk

    canvas_ratio: float = event.width / event.height
    if canvas_ratio < image_ratio: # if canvas is narrower than image
        width = int(event.width)
        height = int(width / image_ratio)
    else:
        height = int(event.height)
        width = int(height * image_ratio)
    
    image_tk = ImageTk.PhotoImage(image.resize((width, height), Image.Resampling.NEAREST))
    image_canvas.create_image(
        int(event.width / 2),
        int(event.height / 2),
        image=image_tk,
        anchor="center")
    


def open_image() -> None:
    global image_canvas, image, image_ratio

    try:
        file_path: str = transcode.get_file_path(INPUT_PATH_ARGV)
    except AssertionError:
        file_path: str = filedialog.askopenfilename()

    image_data: dict[str, int | bytes] = transcode.get_image_data(file_path)
    pixel_list: list[list[int]] = transcode.decode(image_data["width"], image_data["pxdata"])
    pixels: np.ndarray[Any, np.dtype[int]] = np.array(pixel_list)

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
file_menu.add_command(label="Open...", command=open_image)
file_menu.add_command(label="Save as...", command=save_image, state="disabled")
file_menu.add_command(label="Close", command=close_image, state="disabled")
file_menu.add_command(label="Quit", command=window.quit)


image_canvas: tk.Canvas | None = None
image: Image.Image
image_ratio: float


window.mainloop()