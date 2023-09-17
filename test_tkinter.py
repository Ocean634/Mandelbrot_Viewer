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
    raise ImportError ["tkinter module not installed"]


class Displayer:

    def __init__(self):
        self.Master = self.create_window()
        self.Canvas = self.create_canvas(self.Master)
        self.Master.mainloop()


    def create_window(self):
        """ Create tkinter root window

        Returns:
            Tk_instance: main window of the application
        """
        self.Master = tkinter.Tk()
        self.Master.state("zoomed")
        self.Master.update()
        return self.Master


    def create_canvas(self, Master):
        """ Create a drawing space in the window

        Returns:
            Canvas_instance: Drawing surface
        """
        self.Frm = tkinter.Frame(self.Master)
        self.Frm.pack()
        self.Canvas = tkinter.Canvas(self.Frm,
                                     bg="black",
                                     height=Master.winfo_height()-4,
                                     width=Master.winfo_width()-4
                                    )
        self.Canvas.pack()
        self.Master.update()
        return self.Canvas
