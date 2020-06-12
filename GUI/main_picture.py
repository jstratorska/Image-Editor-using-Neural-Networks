import tkinter as tk
import os
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageGrab
from .main_picture_component import MainPictureComponent

class MainPicture(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master = master, relief = tk.FLAT, width=700, height=830, bg="white", borderwidth= 2)
        self.pictures = []
    
    def show_selected_image(self, event):
        file = event.widget.file
        image = ImageTk.PhotoImage(file.resize((180, 200), Image.ANTIALIAS))
        self.pictures.append(MainPictureComponent(self, image, file))
        self.pictures[-1].place(x = 20, y = 20)
        self.pictures[-1].image = image

    def export(self):
        result = filedialog.asksaveasfilename(initialdir = os.getcwd(), title="Select file", defaultextension='.jpg', filetypes=(
        ('JPEG', ('*.jpg', '*.jpeg', '*.jpe')), ('PNG', '*.png'), ('BMP', ('*.bmp', '*.jdib')), ('GIF', '*.gif')))
        if result:
            x = self.winfo_rootx()
            y = self.winfo_rooty()
            height = self.winfo_height() + y
            width = self.winfo_width() + x
            ImageGrab.grab().crop((x, y, width, height)).save(result)