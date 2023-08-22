import io
import tkinter as tk
from tkinter import filedialog as fd
from typing import List
from PIL import Image, ImageTk
import os
import logging
import matplotlib.pyplot as plt

logging.basicConfig(
        level = logging.DEBUG, format = "%(asctime)s %(thread)s %(funcName)s %(message)s"
)


class State:
    image: Image
    image_out: Image
    photo: ImageTk.PhotoImage
    photo_out: ImageTk.PhotoImage
    old_results: List[ImageTk.PhotoImage]

    def __init__(self):
        self.image = None
        self.photo = None
        self.image_out = None
        self.photo_out = None
        self.old_results = []


state = State()


# Pre init code, safe to be synchronous
def new_menu(menu_bar: tk.Menu, label: str, commands: dict) -> None:
    # Create a new menu with the given label and commands.
    # commands is a dictionary of {label: command}, where command is a function
    menu = tk.Menu(menu_bar, tearoff = 0)
    menu_bar.add_cascade(label = label, menu = menu)
    for command in commands:
        menu.add_command(label = command, command = commands[command])


def open_image(cb) -> None:
    logging.debug("Opening image")

    # Filetypes
    filetypes = [
        ("PNG", "*.png"),
        ("JPEG", "*.jpg"),
        ("All files", "*.*")
    ]

    def open() -> Image:
        logging.debug("Blocking open")
        f = fd.askopenfile(filetypes = filetypes)
        logging.debug("Got file")
        image = Image.open(os.path.abspath(f.name))
        f.close()
        return image

    state.image = open()
    cb()


def gen_histogram(cb) -> None:
    logging.debug("Generating histogram")
    hist_list = state.image.histogram()
    reds = hist_list[0:256]
    greens = hist_list[256:512]
    blues = hist_list[512:768]
    v256 = list(range(0, 256))
    plt.plot(v256, reds, color = "red")
    plt.plot(v256, greens, color = "green")
    plt.plot(v256, blues, color = "blue")
    # canvas = plt.get_current_fig_manager().canvas
    # canvas.draw()
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format = 'png')
    plt.clf()
    # im = Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    im = Image.open(img_buf)
    state.image_out = im
    cb()


def init() -> tk.Tk:
    # Pre init code, safe to be synchronous
    root = tk.Tk()
    root.title("Image tool")

    # Create a menu bars
    menu_bar = tk.Menu(root)
    root.config(menu = menu_bar)

    # Frame results
    results_frame = tk.Frame(root, padx = 30, pady = 30, width = 700, height = 300)
    results_frame.grid(row = 1, column = 0, columnspan = 2)
    # Add a Scrollbar(horizontal)
    scrollbar = tk.Scrollbar(results_frame, orient = tk.HORIZONTAL)
    # Span the scrollbar across all columns, but align it to the east and west
    scrollbar.grid(row = 2, column = 0, columnspan = 2, sticky = tk.E + tk.W)

    # Add a Canvas widget to display images
    canvas = tk.Canvas(results_frame, xscrollcommand = scrollbar.set, width = 700, height = 300)
    canvas.grid(row = 0, column = 0, columnspan = 2)

    # Configure the scrollbar to work with the canvas
    scrollbar.config(command = canvas.xview)

    # Create a frame to hold the images (inside the canvas)
    images_frame = tk.Frame(canvas)
    images_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion = canvas.bbox("all")))
    canvas.create_window((0, 0), window = images_frame, anchor = tk.NW)

    def redraw_results() -> None:
        logging.debug("redraw_results")
        for i in range(len(state.old_results)):
            label = tk.Label(images_frame, image = state.old_results[i])
            label.grid(row = 0, column = i, padx = 30, pady = 30)

    def show_image() -> None:
        height = 300
        logging.debug("showImage")
        img = state.image.resize((int(state.image.width * height / state.image.height), height))
        state.photo = ImageTk.PhotoImage(img)
        label = tk.Label(root, image = state.photo)
        label.grid(row = 0, column = 0, padx = 30, pady = 30)

    def show_image_out() -> None:
        height = 250
        logging.debug("showImageOut")
        img = state.image_out.resize((int(state.image_out.width * height / state.image_out.height), height))
        saved_img = state.image_out.resize((int(state.image_out.width * 200 / state.image_out.height), 200))
        state.photo_out = ImageTk.PhotoImage(img)
        state.old_results.append(ImageTk.PhotoImage(saved_img))
        label = tk.Label(root, image = state.photo_out)
        label.grid(row = 0, column = 1, padx = 30, pady = 30)
        redraw_results()

    # Create the file menu
    file_commands = {
        "Open": lambda: open_image(show_image),
        "Exit": lambda: root.destroy()
    }
    new_menu(menu_bar, "File", file_commands)

    # Create the edit menu
    edit_commands = {
        "Histogram": lambda: gen_histogram(show_image_out)
    }
    new_menu(menu_bar, "Edit", edit_commands)

    return root


def main() -> None:
    init().mainloop()

if __name__ == '__main__':
    main()
