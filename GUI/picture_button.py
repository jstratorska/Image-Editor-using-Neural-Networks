import tkinter as tk
import numpy as np


class Button(tk.Button):

    def __init__(self, master, id, anchor, config):
        tk.Button.__init__(self, master = master)
        self.id = id
        self.anchor = anchor
        self.config(config)
        

    def place_button(self, width, height):
        offset_x = 0 if np.floor(self.id / 10) == 1 else 1
        offset_y = 0 if self.id % 10 == 1 else 1
        width = width * offset_x + (-1) ** (1 + offset_x) * 10
        height = height * offset_y + (-1) ** (1 + offset_y) * 10
        self.place(anchor = self.anchor, x = width, y = height)

