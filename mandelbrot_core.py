# Créé par Ocean6, le 07/04/2023 en Python 3.11

try:
    import tkinter_displayer as display
except ImportError:
    raise ImportError("tkinter_displayer module not found")

try:
    import task_manager
except ImportError:
    raise ImportError("task_manager module not found")


def compute_image(max_iterations,
                  corner_1,
                  corner_2,
                  canvas_size,
                  number_of_workers,
                  manager
                 ):

    print("compute_image", max_iterations, corner_1, corner_2, canvas_size, number_of_workers, manager, task_manager.threading.current_thread().name)

    number_of_row = canvas_size[0]

    manager.create_pool(number_of_workers)
    for row in range(number_of_row):
        manager.task_list.append((compute_line,
                                  (max_iterations,
                                   corner_1,
                                   corner_2,
                                   row,
                                   canvas_size)
                                 ))

    manager.create_lonely_thread()


def compute_line(max_iterations, corner_1, corner_2, row, canvas_size):
    print("compute_line", max_iterations, corner_1, corner_2, row, canvas_size, task_manager.threading.current_thread().name)

    divergence_values = []
    imaginary = ((corner_1[1] - corner_2[0]) / canvas_size[0])\
                * (canvas_size[0] - row)

    for pixel in range(canvas_size[1]):
        real = pixel
        complex_number = complex(real, imaginary)
        progression_number = complex(0, 0)

        for iteration in range(max_iterations):
        # next progression number
            progression_number = progression_number * progression_number\
                                 + complex_number

        # check if divergent
            if abs(progression_number.real) > 2\
               or abs(progression_number.imag) > 2:
                divergence_values.append(iteration)
                break
        divergence_values.append(iteration)
    return (divergence_values, row)


def iteration_to_color(iteration, max_iterations):
    # not divergent
    if iteration == max_iterations-1:
        return (0,0,0)

    # playing on the hue value
    h,l,s = iteration%360, 1.0, 0.5
    r,g,b = hsl_to_rgb(h, l, s)
    return (r,g,b)


def hsl_to_rgb(H, S, L):
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

    (r,g,b) = ((R+m)*255, (G+m)*255,(B+m)*255)
    return (int(r+0.5),int(g+0.5),int(b+0.5))

# _____________Main_Programm_________________ #

max_iterations = 70
zoom_power = 2
corner_1 = (-1.75, 1)
corner_2 = (0.25, -1)
number_of_workers = 4

if __name__ == "__main__":
    screen = display.Displayer()
    canvas_size = (screen.canvas_height, screen.canvas_width)
    manager = task_manager.Task_Manager(screen)
    compute_image(max_iterations,
                  corner_1,
                  corner_2,
                  canvas_size,
                  number_of_workers,
                  manager,
                 )
    screen.start_running(manager)

# https://code.activestate.com/recipes/579048-python-mandelbrot-fractal-with-tkinter/