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


def create_window():
    """ Create tkinter root window

    Returns:
        Tk_instance: main window of the application
    """
    Master = tkinter.Tk()
    Master.state("zoomed")
    Master.update()
    return Master


def create_canvas(Master):
    """ Create a drawing space in the window

    Returns:
        Canvas_instance: Drawing surface
    """
    Frm = tkinter.Frame(Master)
    Frm.pack()
    Canvas = tkinter.Canvas(Frm,
                            bg="black",
                            height=Master.winfo_height()-4,
                            width=Master.winfo_width()-4
                           )
    Canvas.pack()
    Master.update()
    return Canvas

Master = create_window()
Canvas = create_canvas(Master)
Master.mainloop()