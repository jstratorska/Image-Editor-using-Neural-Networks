import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk, ImageDraw
import numpy as np

class SidePanel(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master = master, width = 200, height = 530, bg = "white", highlightbackground="black", highlightthickness=1)
        self.images = []
        font = tkFont.Font(size = 24)
        self.message = tk.Label(self, width = 0, height = 0, text = "The sketch \ncouldn't be \nmatched", font = font)
        # self.add_image(r"C:\Users\Jasminka\Desktop\e\47.2.jpg")

    def no_match(self):
        self.remove_images()
        self.message.place(x = 20, y = 20)

    def add_image(self, path):
        x = (len(self.images) % 2)  * 110
        y = 110 * np.floor(len(self.images) / 2)

        file = Image.open(path)
        image = ImageTk.PhotoImage(file.resize((90, 90),Image.ANTIALIAS))
        self.images.append(tk.Label(self, width = 90, height = 90, image = image))
        self.images[-1].image = image
        self.images[-1].file = file
        self.images[-1].place(x = x, y = y)
        self.images[-1].bind("<Button-1>", self.master.main_picture.show_selected_image)

    def remove_images(self):
        for i in range(len(self.images)):
            self.images[i].place_forget()
        self.message.place_forget()
        self.images.clear()