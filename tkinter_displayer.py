#-----------------------------------------------------------------------------
# Name:        test_tkinter
# Purpose:
#
# Author:      Ocean6
#
# Created:     16/09/2023
# Copyright:   (c) Ocean6 2023
# Licence:     <your licence>
#-----------------------------------------------------------------------------
try:
    import tkinter
except ImportError:
    raise ImportError("tkinter module not found")

try:
    import task_manager
except ImportError:
    raise ImportError("task_manager module not found")


class Displayer:

    Master = None
    Frm = None
    Canvas = None
    canvas_height = 0
    canvas_width = 0
    ratio = 0

    def __init__(self):
        self.Master = self.create_window()
        self.Canvas = self.create_canvas()


    def start_running(self, manager):
        self.Master.bind("<<Thread_finished>>", manager.thread_end)
        self.Master.mainloop()

    def create_window(self):
        """ Create tkinter root window

        Returns:
            Tk_instance: main window of the application
        """
        Master = tkinter.Tk()
        Master.minsize(width=320, height=180)
        Master.state("zoomed")
        Master.title("Mandelbrot Viewer")
        Master.update()
        return Master


    def create_canvas(self):
        """ Create a drawing space in the window

        Returns:
            Canvas_instance: Drawing surface
        """
        self.Frm = tkinter.Frame(self.Master)
        self.Frm.pack()
        self.canvas_height = self.Master.winfo_height()-4
        self.canvas_width = self.Master.winfo_width()-4
        self.ratio = self.canvas_width / self.canvas_height
        Canvas = tkinter.Canvas(self.Frm,
                                bg="black",
                                height = self.canvas_height,
                                width = self.canvas_width
                               )
        Canvas.pack()
        self.Master.update()
        return Canvas


    def get_canvas_size(self):
        """ Return the size of the drawing surface """
        return (self.canvas_height, self.canvas_width)


    def draw_line(self, line, row):
        for pixel in range(len(line)):
                self.draw_pixel((pixel, row+10), (pixel+1, row+10), line[pixel])


    def draw_pixel(self, pos1, pos2, color):
        self.Canvas.create_line(pos1, pos2, fill='cyan')