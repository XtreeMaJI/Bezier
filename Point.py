import tkinter as tk

point_size = 5


class Point:

    def __init__(self, new_x=0, new_y=0, new_color=None, new_canvas=None):
        self.x = new_x
        self.y = new_y
        self.color = new_color
        self.canvas = new_canvas

    def draw(self):
        global point_size
        # смещение относительно центра точки
        offset = point_size / 2
        x = self.x
        y = self.y
        canvas = self.canvas
        color = self.color
        canvas.create_oval(x - offset, y - offset, x + offset, y + offset, fill=color)

    def set_pos(self, x, y):
        self.x = x
        self.y = y