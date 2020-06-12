import tkinter as tk
from PIL import Image
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import random
from DataPreprocess.read_sketches import read_sketch_data
from DataPreprocess.read_data import find_files

class Canvas(tk.Canvas):

    def __init__(self, master):
        tk.Canvas.__init__(self, master = master, relief = tk.FLAT, width=700, height=830, bg="white", borderwidth= 2)
        self.number_of_strokes = 0
        self.coords = []
        self.x1 = self.x2 = self.y1 = self.y2 = 0
        self.bind("<Button-1>", self.reset_drawing_coords)
        self.bind("<B1-Motion>", self.draw_line)

    def clear_canvas(self):
        self.delete("all")
        self.number_of_strokes = 0
        self.coords = []

    def recreate_sketch(self, dim):
        width = dim[1] - dim[3] + 10
        height = dim[2] - dim[0] + 10
        x_offset = dim[3] - 5
        y_offset = dim[0] - 5
        optimized_window = tk.Tk()
        optimized_window.geometry(str(width) + "x" + str(height))

        canvas = tk.Canvas(optimized_window, width = width, height = height, bg = "white")
        canvas.pack()
        for stroke in self.coords:
            for i in range (0, len(stroke[0]) - 1):
                canvas.create_line(stroke[0][i] - x_offset, stroke[1][i] - y_offset, stroke[0][i+1] - x_offset, stroke[1][i+1] - y_offset, width = 2)
        optimized_window.mainloop()

    def suggest_pictures(self, index):
        self.master.side_panel.remove_images()
        images = find_files("Data\\images\\" + self.master.objects[index] + "\\*")
        for i in range(min(12, len(images))):
            self.master.side_panel.add_image(images[i])

    def predict_sketch(self, data):
        for i in range(5):
            prediction = self.master.neuralNetwork[i].predict_value(data, i)
            if prediction == 1:
                self.suggest_pictures(i)
                break
            if i == 4:
                self.master.side_panel.no_match()

    def done_sketching(self):
        self.sketch_to_picture()
        data = self.picture_to_array()
        self.predict_sketch(data)

    def picture_to_array(self):
        image = Image.open(self.path)
        data = np.array(image)
        data = pd.DataFrame((data[:,:,0]/255).reshape(1, -1))
        return data.T

    def sketch_to_picture(self):
        fig = plt.figure(figsize=(1,1))
        plt.axis('off')        
        for stroke in range(len(self.coords)): 
            plt.plot(self.coords[stroke][0], self.coords[stroke][1], linewidth=2, color='black')
        self.path = "Data\\user_sketches\\" + str(random.randint(10000, 2500000)) + ".png"
        fig.savefig(self.path)
        plt.close(fig)

    def normalize_sketch(self):
        max_x_coord = max( [max(stroke[0]) for stroke in self.coords])
        max_y_coord = max( [max(stroke[1]) for stroke in self.coords])

        min_x_coord = min([min(stroke[0]) for stroke in self.coords])
        min_y_coord = min([min(stroke[1]) for stroke in self.coords])
    
        dim = [min_y_coord, max_x_coord, max_y_coord, min_x_coord]
        self.recreate_sketch(dim)
            
    def draw_line(self, event):
        self.x1 , self.x2 = self.x2, (event.x)
        self.y1, self.y2 = self.y2, event.y
        self.create_line(self.x1, self.y1, self.x2, self.y2, width=2)
        self.coords[self.number_of_strokes-1][0].append(self.x1)
        self.coords[self.number_of_strokes-1][1].append(self.y1)

    def reset_drawing_coords(self, event):
        self.x2 = event.x
        self.y2 = event.y
        self.coords.append([])
        self.coords[self.number_of_strokes].append([])
        self.coords[self.number_of_strokes].append([])
        self.number_of_strokes += 1