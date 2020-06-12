import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from .picture_button import Button
import numpy as np

class MainPictureComponent(tk.Label):
    def  __init__(self, master, image, file):
        tk.Label.__init__(self, master = master, width = 180, height = 200, image = image, padx=10, pady=10, borderwidth=0)
        
        self.bind("<Enter>", self.select_image)
        self.bind("<Leave>", self.remove_buttons)
        self.bind("<Double-Button-1>", self.destroy_self)
        self.file = file
        self.image = image
        self.btn_move_image = ImageTk.PhotoImage(Image.open("Data\\repos\\move.png").resize((30,30), Image.ANTIALIAS))
        self.btn_crop_image = ImageTk.PhotoImage(Image.open("Data\\repos\\crop.png").resize((30,30), Image.ANTIALIAS))
        self.width = 180
        self.height = 200
        self.initialize_crop_buttons()
        self.initialize_resize_buttons()
        self.cropping = [False, False, False, False]

    def destroy_self(self, event):
        self.destroy()

    def remove_buttons(self, event):
        self.unshow_buttons()

    def unshow_buttons(self):
        for i in range(4):
            self.resize_buttons[i].place_forget()
        self.move.place_forget()
        self.crop.place_forget()
        for i in range(4):
            if not self.cropping[i]:
                self.crop_buttons_frames[i].place_forget()

    def select_image(self, event):
        self.width = event.widget.winfo_width()
        self.height = event.widget.winfo_height() 
        self.select(self.width, self.height)

    def select(self, width, height):
        self.unshow_buttons()
        self.display_crop_buttons(width, height)
        self.update_buttons_position(width, height)

    def resize_crop_buttons(self, width, height):
        for i in range (4):
            btn_width = width if (i % 2) == 0 else 10
            btn_height = height if (i % 2) != 0 else 10
            self.crop_buttons_frames[i].config(width = btn_width, height = btn_height)
            if not self.cropping[i]:
                self.display_crop_buttons(width, height)

    def initialize_crop_buttons(self):
        self.crop_buttons = []
        self.crop_buttons_frames = []
        for i in range(4):
            width = self.width
            height = self.height
            btn_width = width if (i % 2) == 0 else 10
            btn_height = height if (i % 2) != 0 else 10
            self.crop_buttons_frames.append(tk.Frame(self, width = btn_width, height = btn_height))
            self.crop_buttons_frames[i].propagate(False)
            self.crop_buttons.append(tk.Button(self.crop_buttons_frames[i], bg="red"))
            self.crop_buttons[i].bind("<B1-Motion>", self.update_crop_position)
            self.crop_buttons[i].bind("<ButtonRelease-1>", self.release_update_crop_position)
 
            self.crop_buttons[i].pack(expand = True, fill= tk.BOTH)
            self.crop_buttons[i].id = i
        
    def display_crop_buttons(self, width, height):
        positions = [
            ['nw', 0, 0],
            ['ne', width, 0],
            ['sw', 0, height],
            ['nw', 0, 0]
        ]
        for i in range(4):
            if not self.cropping[i]:
                self.crop_buttons_frames[i].place(anchor = positions[i][0], x = positions[i][1] , y = positions[i][2])
   
    def initialize_resize_buttons(self):
        ids = [11, 1, 0, 10]
        anchors = ['nw', 'ne', 'se', 'sw']
        self.resize_buttons = []
        for i in range(4):
            self.resize_buttons.append(Button(master = self, id = ids[i], anchor = anchors[i], config = {"width":2, "height":1, "text":"", "bg":'black'}))
            self.resize_buttons[i].bind("<B1-Motion>", self.resize_picture)
            self.resize_buttons[i].bind("<ButtonRelease-1>", self.update)

        self.move = tk.Button(self, width = 30, height = 30, image = self.btn_move_image)
        self.crop = tk.Button(self, width = 30, height = 30, image = self.btn_crop_image)

        self.move.bind("<B1-Motion>", self.move_picture)
        self.move.bind("<ButtonRelease-1>", self.stop_move_picture)
        self.crop.bind("<Button-1>", self.crop_image)

    def update(self, event):
        width = self.winfo_width()
        height = self.winfo_height()
        self.update_buttons_position(width, height)
        self.resize_crop_buttons(width, height)
        self.image = ImageTk.PhotoImage(self.resized)
        self.config(image = self.image)    
        self.select(width, height)
        self.width = width
        self.height = height

    def update_buttons_position(self, width, height):
        for i in range(4):
            self.resize_buttons[i].place_button(width, height)
            self.resize_buttons[i].event_x = 0
            self.resize_buttons[i].event_y = 0
        self.move.place(anchor="center", x = width/2, y = height/2)
        self.crop.place(anchor="center", x = width/2, y = height - 40)
    
    def update_crop_position(self, event):
        widget = event.widget.master
        widget_x = widget.winfo_x()
        widget_y = widget.winfo_y()
        if event.widget.id % 2 == 1:
            widget.place(x = widget_x + event.x, y = widget_y, anchor="nw")
        else:
            widget.place(y = widget_y + event.y, x = widget_x, anchor = "nw")
        self.cropping[event.widget.id] = True

    def release_update_crop_position(self, event):
        self.select(self.width, self.height)

    def crop_image (self, event):
        img_width, img_height = event.widget.master.file.size
        ratio_x = img_width / self.winfo_width()
        ratio_y = img_height / self.winfo_height()
        box = []
        buttons = self.crop_buttons_frames
        box.append(buttons[3].winfo_x() * ratio_x)
        box.append(buttons[0].winfo_y() * ratio_y)
        box.append((buttons[1].winfo_x() + buttons[1].winfo_width()) * ratio_x)
        box.append((buttons[2].winfo_y() + buttons[2].winfo_height()) * ratio_y)

        file = event.widget.master.file
        new_image = file.crop(box).resize((self.width, self.height), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(new_image)
        self.file = new_image
        self.config(image = self.image)
        self.cropping = [False, False, False, False]
        self.select(self.width, self.height)

    def move_picture(self, event):
        self.unshow_buttons()
        container = event.widget.master
        container_x = container.winfo_x()
        container_y = container.winfo_y()

        container_width = container.winfo_width()
        container_height = container.winfo_height()
        
        canvas = container.master
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        if (container_x + event.x > 0) & (container_y + event.y > 0) & (event.x + container_width + container_x < canvas_width) & (event.y + container_height + container_y < canvas_height): 
            container.place(anchor="nw", x = event.x + container_x,  y = event.y + container_y)

    def stop_move_picture(self, event):
        self.select(self.width, self.height)

    def resize_picture(self, event):
        self.unshow_buttons()
        button = event.widget
        offset_x = int (button.id / 10)
        offset_y = button.id % 10

        container = button.master
        container_width = container.winfo_width()
        container_height = container.winfo_height()
        container_x = container.winfo_x() - 2
        container_y = container.winfo_y() - 2

        canvas_width = container.master.winfo_width()
        canvas_height = container.master.winfo_height()
        button.event_x = event.x - button.event_x
        button.event_y = event.y - button.event_y
        new_width = max((container_width + (button.event_x if offset_x == 0 else -event.x), 50))
        new_height = max((container_height + (button.event_y if offset_y == 0 else -event.y), 150))
        
        if (container_width + button.event_x > 0) & (container_height + button.event_y > 0) & (container_x + new_width < canvas_width) & (container_y + new_height < canvas_height): 
            self.resized = self.file.resize((new_width, new_height), Image.ANTIALIAS)
            container.config(width = new_width, height = new_height)                   
            container.place(x = offset_x * (container_width - new_width) + container_x, y = offset_y * (container_height - new_height) + container_y, anchor="nw")
        button.event_x = event.x
        button.event_y = event.y