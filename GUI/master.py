import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from .canvas import Canvas
from .main_picture import MainPicture
from .side_panel import SidePanel
from NeuralNetwork.setup import setup

class Master(tk.Tk):
 
    def __init__(self):
        tk.Tk.__init__(self)
        self.neuralNetwork = setup()

        self.objects = ['airplane', 'apple', 'banana', 'bicycle', 'bird']
        font = 'Arial 14'

        self.state("zoomed")
        self.title('Sketch Me')
        self.config(bg = "cadet blue")

        self.main_picture = MainPicture(self)
        self.main_picture.place(y = 100, x = 850, anchor="nw") 

        self.side_panel = SidePanel(self)
        self.side_panel.place(anchor="nw", x=1650, y = 400)

        self.canvas = Canvas(self)
        self.canvas.place(y = 100, x = 50, anchor="nw") 

        self.btn_done = tk.Button(self, text = 'Done Sketching', width = 18, height = 3, font = font, command=self.canvas.done_sketching)
        self.btn_done.place(anchor="nw", x = 1650, y = 100)

        self.btn_clear = tk.Button(self, text = 'Clear the canvas', width = 18, height = 3, font = font, command=self.canvas.clear_canvas) 
        self.btn_clear.place(anchor="nw", x = 1650, y = 200)

        self.btn_export  = tk.Button(self, text = 'Export Image', width = 18, height = 3, font = font, command=self.main_picture.export)
        self.btn_export.place(anchor="nw", x = 1650, y = 300)

        self.mainloop()