# Créé par Ocean6, le 07/04/2023 en Python 3.11

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

import time

class Displayer:

    Master = None
    Frm = None
    Canvas = None
    img = None
    canvas_height = 0
    canvas_width = 0
    ratio = 0
    result_queue = []
    raw_image = ""


    def __init__(self):
        self.Master = self.create_window()
        self.Canvas = self.create_canvas()


    def start_running(self, manager):
        running = True
        while running:
            try:
                self.Master.update()
                self.display_data()
            except tkinter._tkinter.TclError:
                running = False

        self.Master.quit()

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
        self.img = tkinter.PhotoImage(height=self.canvas_height, width=self.canvas_width)
        Canvas.create_image((0, 0), image = self.img, state = "normal", anchor = tkinter.NW)
        self.Master.update()
        return Canvas


    def iteration_to_color(self, iteration, max_iterations):
        # not divergent
        if iteration == max_iterations-1:
            return (0,0,0)

        # playing on the hue value
        h,l,s = iteration%360, 1.0, 0.5
        r,g,b = self.hsl_to_rgb(h, l, s)
        return (r,g,b)


    def hsl_to_rgb(self, H, S, L):
        """ Transfert colorization format from HLS to RGB

        Parameters :
            H (float): hue value (between 0° and 360°)
            S (float): saturation value (between 0 and 1)
            L (float): lightness (between 0 and 1)

        Returns:
            int: red value
            int: green value
            int: blue value

        """
        C = (1 - abs(2*L - 1)) * S
        X = C * (1 - abs((H / 60) % 2 - 1))
        m = L - C/2

        if 0 <= H < 60:
            R,G,B = C,X,0
        elif 60 <= H < 120:
            R,G,B = X,C,0
        elif 120 <= H < 180:
            R,G,B = 0,C,X
        elif 180 <= H < 240:
            R,G,B = 0,X,C
        elif 240 <= H < 300:
            R,G,B = X,0,C
        elif 300 <= H < 360:
            R,G,B = C,0,X
        else:
            raise ValueError("hue value can't be outside of 0°-360°")

        (r,g,b) = ((R+m)*255, (G+m)*255, (B+m)*255)
        (r,g,b) = ((r+0.5)//1, (g+0.5)//1, (b+0.5)//1)
        return (r,g,b)


    def display_data(self):
        if  len(self.result_queue) > 10:
            for i in range(10):
                self.put_data()
        elif len(self.result_queue) > 0:
            self.put_data()
        self.img.put(self.raw_image)



    def put_data(self):
        max_iter = mandelbrot_core.max_iterations
        data = self.result_queue.pop(0)[0]
        line = " {"
        line += " ".join(self.rgb_to_hex(self.iteration_to_color(value, max_iter)) for value in data)
        line += "}"
        self.raw_image += line


    def rgb_to_hex(self, color):
        return ' #{:02x}{:02x}{:02x}'.format(int(color[0]), int(color[1]), int(color[2]))