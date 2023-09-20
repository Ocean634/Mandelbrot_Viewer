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


# Report

##Displayer.__init__ MainThread
##Displayer.create_window MainThread
##Displayer.create_canvas MainThread
##Task_Manager.__init__ <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> MainThread
##compute_image 70 (-1.75, 1) (0.25, -1) (1005, 1916) 4 <task_manager.Task_Manager object at 0x0000027E0E7B16D0> MainThread
##Task_Manager.create_pool 4 MainThread
##My_Thread.__init__ None None <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> None MainThread
##My_Thread.__init__ None None <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> None MainThread
##My_Thread.__init__ None None <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> None MainThread
##My_Thread.__init__ None None <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> None MainThread
##Task_Manager.create_lonely_thread MainThread
##Task_Manager.start_processing employer
##Displayer.start_running <task_manager.Task_Manager object at 0x0000027E0E7B16D0> MainThread
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 0, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##My_Thread.task Thread-5 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 1, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##compute_line 70 (-1.75, 1) (0.25, -1) 0 (1005, 1916) Thread-5 (task)
##My_Thread.task Thread-6 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 1 (1005, 1916) Thread-6 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 2, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 0 MainThread
##My_Thread.task Thread-7 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 2 (1005, 1916) Thread-7 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 3, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##My_Thread.task Thread-8 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 3 (1005, 1916) Thread-8 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 4, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##My_Thread.task Thread-9 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 4 (1005, 1916) Thread-9 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 5, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##My_Thread.task Thread-10 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 6, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##compute_line 70 (-1.75, 1) (0.25, -1) 5 (1005, 1916) Thread-10 (task)
##My_Thread.task Thread-11 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 6 (1005, 1916) Thread-11 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 7, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##My_Thread.task Thread-12 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 7 (1005, 1916) Thread-12 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 8, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##My_Thread.task Thread-13 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 9, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##compute_line 70 (-1.75, 1) (0.25, -1) 8 (1005, 1916) Thread-13 (task)
##My_Thread.task Thread-14 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 9 (1005, 1916) Thread-14 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 10, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##My_Thread.task Thread-15 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 10 (1005, 1916) Thread-15 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 11, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##My_Thread.task Thread-16 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 11 (1005, 1916) Thread-16 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 12, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##My_Thread.task Thread-17 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 12 (1005, 1916) Thread-17 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 13, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##My_Thread.task Thread-18 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 13 (1005, 1916) Thread-18 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 14, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##My_Thread.task Thread-19 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 14 (1005, 1916) Thread-19 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 15, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##My_Thread.task Thread-20 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 15 (1005, 1916) Thread-20 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 16, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##My_Thread.task Thread-21 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 16 (1005, 1916) Thread-21 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 17, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##My_Thread.task Thread-22 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 18, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##compute_line 70 (-1.75, 1) (0.25, -1) 17 (1005, 1916) Thread-22 (task)
##My_Thread.start employer
##My_Thread.task Thread-23 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 18 (1005, 1916) Thread-23 (task)
##My_Thread.__init__ <function compute_line at 0x0000027E1067E020> (70, (-1.75, 1), (0.25, -1), 19, (1005, 1916)) <tkinter_displayer.Displayer object at 0x0000027E1066FDD0> <task_manager.Task_Manager object at 0x0000027E0E7B16D0> employer
##My_Thread.start employer
##My_Thread.task Thread-24 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 19 (1005, 1916) Thread-24 (task)
# to __________________________________1004___________________________
# then
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 4 MainThread
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 5 MainThread
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 6 MainThread
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 7 MainThread
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 8 MainThread
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 9 MainThread
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 10 MainThread
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 11 MainThread
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 12 MainThread
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 13 MainThread
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 14 MainThread
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 15 MainThread



# When running debug
##Displayer.__init__ MainThread
##Displayer.create_window MainThread
##Displayer.create_canvas MainThread
##Task_Manager.__init__ <tkinter_displayer.Displayer object at 0x000001BA11440150> MainThread
##compute_image 70 (-1.75, 1) (0.25, -1) (1005, 1916) 4 <task_manager.Task_Manager object at 0x000001BA11440C90> MainThread
##Task_Manager.create_pool 4 MainThread
##My_Thread.__init__ None None <tkinter_displayer.Displayer object at 0x000001BA11440150> None MainThread
##My_Thread.__init__ None None <tkinter_displayer.Displayer object at 0x000001BA11440150> None MainThread
##My_Thread.__init__ None None <tkinter_displayer.Displayer object at 0x000001BA11440150> None MainThread
##My_Thread.__init__ None None <tkinter_displayer.Displayer object at 0x000001BA11440150> None MainThread
##Task_Manager.create_lonely_thread MainThread
##Task_Manager.start_processing employer
##Displayer.start_running <task_manager.Task_Manager object at 0x000001BA11440C90> MainThread
##My_Thread.__init__ <function compute_line at 0x000001BA1150E020> (70, (-1.75, 1), (0.25, -1), 0, (1005, 1916)) <tkinter_displayer.Displayer object at 0x000001BA11440150> <task_manager.Task_Manager object at 0x000001BA11440C90> employer
##My_Thread.start employer
##My_Thread.task Thread-5 (task)
##My_Thread.__init__ <function compute_line at 0x000001BA1150E020> (70, (-1.75, 1), (0.25, -1), 1, (1005, 1916)) <tkinter_displayer.Displayer object at 0x000001BA11440150> <task_manager.Task_Manager object at 0x000001BA11440C90> employer
##My_Thread.start employer
##compute_line 70 (-1.75, 1) (0.25, -1) 0 (1005, 1916) Thread-5 (task)
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 0 MainThread
##My_Thread.task Thread-6 (task)
##compute_line 70 (-1.75, 1) (0.25, -1) 1 (1005, 1916) Thread-6 (task)
##My_Thread.__init__ <function compute_line at 0x000001BA1150E020> (70, (-1.75, 1), (0.25, -1), 2, (1005, 1916)) <tkinter_displayer.Displayer object at 0x000001BA11440150> <task_manager.Task_Manager object at 0x000001BA11440C90> employer
##My_Thread.start employer
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 1 MainThread
##My_Thread.task Thread-7 (task)
##My_Thread.__init__ <function compute_line at 0x000001BA1150E020> (70, (-1.75, 1), (0.25, -1), 3, (1005, 1916)) <tkinter_displayer.Displayer object at 0x000001BA11440150> <task_manager.Task_Manager object at 0x000001BA11440C90> employer
##My_Thread.start employer
##compute_line 70 (-1.75, 1) (0.25, -1) 2 (1005, 1916) Thread-7 (task)
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 2 MainThread
##My_Thread.task Thread-8 (task)
##My_Thread.__init__ <function compute_line at 0x000001BA1150E020> (70, (-1.75, 1), (0.25, -1), 4, (1005, 1916)) <tkinter_displayer.Displayer object at 0x000001BA11440150> <task_manager.Task_Manager object at 0x000001BA11440C90> employer
##My_Thread.start employer
##compute_line 70 (-1.75, 1) (0.25, -1) 3 (1005, 1916) Thread-8 (task)
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3831 3 MainThread
##My_Thread.task Thread-9 (task)
##My_Thread.__init__ <function compute_line at 0x000001BA1150E020> (70, (-1.75, 1), (0.25, -1), 5, (1005, 1916)) <tkinter_displayer.Displayer object at 0x000001BA11440150> <task_manager.Task_Manager object at 0x000001BA11440C90> employer
##My_Thread.start employer
##compute_line 70 (-1.75, 1) (0.25, -1) 4 (1005, 1916) Thread-9 (task)
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 4 MainThread
##My_Thread.task Thread-10 (task)
##My_Thread.__init__ <function compute_line at 0x000001BA1150E020> (70, (-1.75, 1), (0.25, -1), 6, (1005, 1916)) <tkinter_displayer.Displayer object at 0x000001BA11440150> <task_manager.Task_Manager object at 0x000001BA11440C90> employer
##compute_line 70 (-1.75, 1) (0.25, -1) 5 (1005, 1916) Thread-10 (task)
##My_Thread.start employer
##Task_Manager.thread_end <VirtualEvent event x=0 y=0> MainThread
##Displayer.draw_line, len(line) = 3832 5 MainThread
##My_Thread.task Thread-11 (task)