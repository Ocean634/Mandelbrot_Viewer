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


    def create_window(self):
        """ Create tkinter root window

        Returns:
            Tk_instance: main window of the application
        """
        Master = tkinter.Tk()
        Master.state("zoomed")
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
        self.ratio = self.width / self.height
        self.Canvas = tkinter.Canvas(self.Frm,
                                     bg="black",
                                     height = self.height,
                                     width = self.width
                                    )
        self.Canvas.pack()
        self.Master.update()
        return self.Canvas


    def get_canvas_size(self):
        """ Return the size of the drawing surface """
        return (self.canvas_height, self.canvas_width)
