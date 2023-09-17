# Créé par Ocean6, le 07/04/2023 en Python 3.11

import tkinter_displayer as display
import task_manager

# _______________Additional_Functions_________________ #


def compute_image(max_iterations, corner_1, corner_2, canvas_size, number_of_workers, manager):

    number_of_row = canvas_size[0]

    pool = manager.create_pool(number_of_workers)
    for row in range(number_of_row):
        manager.task_list.append((compute_line, (max_iterations, corner_1, corner_2, row)))
        manager.start_processing()



def compute_pixel(width, height, x_column, y_row, max_iterations, center):
    """ Compute and draw a piece of the Mandelbrot fractal

    Parameters:
        height (int): height in pixels of the image to compute
        width (int): width in pixel of the image to compute
        max_iterations (int): represent the limit to decide if a point is divergent or not
        center (tuple): coordinates of the center of the window on the fractal
        zoom (int): zoom power

    Returns:

    """

    imaginary = (x_column/width)*unit - (0.5*unit - center[0])
    real = (y_row/height)*unit - (0.5*unit - center[1])

    complex_number = complex(real, imaginary)

    # starting position
    progression_number = complex(0, 0)

    for iteration in range(max_iterations):

        # next progression number
        progression_number = progression_number * progression_number + complex_number

        # check if divergent
        if abs(progression_number.real) > 2 or abs(progression_number.imag) > 2:
            return iteration

    return iteration


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


def print_pixel(color, position):
    """ Draw one pixel on screen

    Parameters:
        color (tuple): r,g,b values for the pixel
        position (tuple): x and y corrdinates of the pixel inside the image

    Returns:

    """
    global screen
    position_on_screen = (screen.get_width()/2-screen.get_height()/2+position[0], position[1])

    pygame.draw.rect(screen, color, (position_on_screen[0], position_on_screen[1], 1, 1))
    if position[0] == screen.get_height()-1:
        pygame.display.update((position_on_screen[0]-screen.get_height()-1, position_on_screen[1], screen.get_height(), 1))

# _____________Main_Programm_________________ #

max_iterations = 70
zoom_power = 2
# center = (-0.75, 0)
# unit = 2
corner_1 = (-1.75, 1)
corner_2 = (0.25, -1)

if __name__ == "__main__":
    # screen = display.Displayer()
    # canvas_size = screen.get_canvas_size()
    # manager = task_manager.Task_Manager()
    pass


##thread1 = threading.Thread(target=draw_tile, args=(screen_height, screen_height, max_iterations, current_center, current_zoom))
##thread1.start()
##
##running = True
##while running:
##    for event in pygame.event.get():
##        if event.type == pygame.QUIT:
##            running = False
##
##        if not thread1.is_alive():
##            if pygame.mouse.get_focused():
##                if event.type == pygame.MOUSEBUTTONDOWN:
##                    x, y = pygame.mouse.get_pos()
##                    x = x - (screen_width/2-screen_height/2)
##
##                    if 0 <= x < screen_height:
##                        global unit
##                        x = x/screen_height*unit-(0.5*unit) + current_center[0]
##                        y = y/screen_height*unit-(0.5*unit) + current_center[1]
##                        current_zoom *= zoom
##                        current_center = (x, y)
##                        # max_iterations += int(1/(zoom/6) * max_iterations)
##                        max_iterations += 100
##                        print(current_zoom, current_center, max_iterations)
##
##                        thread1 = threading.Thread(target=draw_tile, args=(screen_height, screen_height, max_iterations, current_center, current_zoom))
##                        thread1.start()
##    clock.tick(60)
##
##pygame.quit()