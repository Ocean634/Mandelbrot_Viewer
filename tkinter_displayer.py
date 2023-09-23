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

try:
    import mandelbrot_core
except ImportError:
    raise ImportError("mandelbrot_core module not found")

try:
    import sys
except ImportError:
    raise ImportError("sys module not found")


class Displayer:

    Master = None
    Frm = None
    Canvas = None
    img = None
    canvas_height = 0
    canvas_width = 0
    ratio = 0
    result_queue = []

    def __init__(self):

        print("Displayer.__init__", task_manager.threading.current_thread().name)

        self.Master = self.create_window()
        self.Canvas = self.create_canvas()


    def start_running(self, manager):

        print("Displayer.start_running", manager, task_manager.threading.current_thread().name)

        running = True
        while running:
            self.Master.update()

            try:
                self.Master.winfo_exists()
            except tkinter._tkinter.TclError:
                running = False

            for i in range(10):
                if len(self.result_queue) >= 1:
                    self.display_data()
        self.Master.quit()

    def create_window(self):
        """ Create tkinter root window

        Returns:
            Tk_instance: main window of the application
        """

        print("Displayer.create_window", task_manager.threading.current_thread().name)

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

        print("Displayer.create_canvas", task_manager.threading.current_thread().name)

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
        self.img = tkinter.PhotoImage(height=self.canvas_height, width=self.canvas_width)
        Canvas.create_image((0, 0), image = self.img, state = "normal", anchor = tkinter.NW)
        self.Master.update()
        return Canvas


    def display_data(self):
        print("Displayer.display_data", task_manager.threading.current_thread().name)

        result = []
        data = self.result_queue.pop(0)
        # treatment function / palette
        for pixel in data[0]:
            if pixel == mandelbrot_core.max_iterations-1:
                result.append((0, 0, 0))
            else:
                result.append((1, 1, 1))
        self.draw_line(result, data[1])


    def draw_line(self, line, row):

        print("Displayer.draw_line, len(line) =", len(line), row, task_manager.threading.current_thread().name)

        for pixel in range(len(line)):
            # self.draw_pixel(pixel, row, pixel+1, row, line[pixel])
            pass


    def rgb_to_hex(r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)