# Créé par Ocean6, le 07/04/2023 en Python 3.11

try:
    import tkinter_displayer as display
except ImportError:
    raise ImportError("tkinter_displayer module not found")

try:
    import task_manager
except ImportError:
    raise ImportError("task_manager module not found")

import time

def compute_image(max_iterations, corner_1, corner_2, canvas_size,
                  number_of_workers, manager):

    manager.create_pool(number_of_workers)

    for row in range(canvas_size[0]):
        manager.task_list.append((compute_line, (max_iterations, corner_1,
                                  corner_2, row, canvas_size)))

    manager.create_lonely_thread()


def compute_line(max_iterations, corner_1, corner_2, row, canvas_size):
    # print("compute_line", row, task_manager.threading.current_thread().name, end="     ")
    start_time = time.time()
    divergence_values = []
    imaginary = corner_1[1] - row * ((corner_1[1]-corner_2[1]) / canvas_size[0])

    for column in range(canvas_size[1]):
        flag = False
        real = corner_1[0] + column * ((corner_2[0]-corner_1[0]) / canvas_size[1])
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
                flag = True
                break

        if flag is False:
            divergence_values.append(iteration)
    # print(time.time()-start_time)
    # print(row)
    return (divergence_values, row)


def get_center(corner_1, corner_2):
    x = corner_1[0] + 0.5*(corner_2[0]-corner_1[0])
    y = corner_2[1] + 0.5*(corner_1[1]-corner_2[1])
    return (x, y)


def fit_screen_size(corner_1, corner_2, screen):
    height = corner_1[1]-corner_2[1]
    width = corner_2[0]-corner_1[0]
    ratio_image = width / height
    center = get_center(corner_1, corner_2)
    print(center, width, height)

    if screen.ratio > ratio_image: # modify width [0]
        new_width = screen.ratio * height
        print(new_width)
        corner_1 = (center[0]-(0.5*new_width), corner_1[1])
        corner_2 = (center[0]+(0.5*new_width), corner_2[1])
        print(corner_1, corner_2)

    elif screen.ratio < ratio_image: # modify height [1]
        new_height = width / screen.ratio
        print(new_height)
        corner_1 = (corner_1[0], center[1]+(0.5*new_height))
        corner_2 = (corner_2[0], center[1]-(0.5*new_height))
        print(corner_1, corner_2)

    return (corner_1, corner_2)

# _____________Main_Programm_________________ #

max_iterations = 70
# zoom_power = 2
corner_1 = (-2, 1.2)
corner_2 = (1, -1.2)
number_of_workers = 2


def main():
    global max_iterations
    global zoom_power
    global corner_1
    global corner_2
    global number_of_workers
    screen = display.Displayer()
    canvas_size = (screen.canvas_height, screen.canvas_width)
    manager = task_manager.Task_Manager(screen)
    (corner_1, corner_2) = fit_screen_size(corner_1, corner_2, screen)
    compute_image(max_iterations,
                  corner_1,
                  corner_2,
                  canvas_size,
                  number_of_workers,
                  manager,
                 )
    screen.start_running(manager)


if __name__ == "__main__":
    main()