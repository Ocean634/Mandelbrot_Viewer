# Créé par Ocean6, le 07/04/2023 en Python 3.11

import pygame
import threading

# _______________Additional_Functions_________________ #


def draw_tile(height, width, depth, center, zoom):
    """ Compute and draw a piece of the Mandelbrot fractal

    Parameters:
        height (int): height in pixels of the image to compute
        width (int): width in pixel of the image to compute
        depth (int): represent the limit to decide if a point is divergent or not
        center (tuple): coordinates of the center of the window on the fractal
        zoom (int): zoom power

    Returns:

    """
    global unit
    unit = 3/zoom

    memory = [[(0,0,0)]*width]*3

    for y_row in range (height):
        for x_column in range (width):

            iteration = compute_pixel(width, height, x_column, y_row, depth, center)

            color = iteration_to_color(iteration, depth)
            memory[2][x_column] = color

        if y_row == 0:
            memory = memory_shift(memory, width)

        else:
            for x in range(width):
                # color = color_smoothing(memory, x)
                print_pixel(memory[1][x], (x, y_row-1))

            memory = memory_shift(memory, width)

        if y_row == height-1:
            for x in range(width):
                # color = color_smoothing(memory, x)
                print_pixel(memory[1][x], (x, y_row))


def compute_pixel(width, height, x_column, y_row, depth, center):
    """ Compute and draw a piece of the Mandelbrot fractal

    Parameters:
        height (int): height in pixels of the image to compute
        width (int): width in pixel of the image to compute
        depth (int): represent the limit to decide if a point is divergent or not
        center (tuple): coordinates of the center of the window on the fractal
        zoom (int): zoom power

    Returns:

    """

    imaginary = (x_column/width)*unit - (0.5*unit - center[0])
    real = (y_row/height)*unit - (0.5*unit - center[1])

    complex_number = complex(real, imaginary)

    # starting position
    progression_number = complex(0, 0)

    for iteration in range(depth):

        # next progression number
        progression_number = progression_number * progression_number + complex_number

        # check if divergent
        if abs(progression_number.real) > 2 or abs(progression_number.imag) > 2:
            return iteration

    return iteration


def iteration_to_color(iteration, depth):
    # not divergent
    if iteration == depth-1:
        return (0,0,0)

    # playing on the hue value
    h,l,s = iteration%360, 1.0, 0.5
    r,g,b = hsl_to_rgb(h, l, s)
    return (r,g,b)


def memory_shift(memory, width):
    memory[0] = memory[1]
    memory[1] = memory[2]
    memory[2] = [(0,0,0)]*width
    return memory


def color_smoothing(memory, x):
    red, green, blue = 0, 0, 0
    for row in range(3):
        for column in range(3):
            if row == 1 and column == 1:
                red += memory[column][x+(row-1)][0]
                green += memory[column][x+(row-1)][1]
                blue += memory[column][x+(row-1)][2]
            else:
                try:
                    red += memory[column][x+(row-1)][0]/8
                    green += memory[column][x+(row-1)][1]/8
                    blue += memory[column][x+(row-1)][2]/8
                except IndexError:
                    continue
    red /= 2
    green /= 2
    blue /= 2
    return (int(red+0.5), int(green+0.5), int(blue+0.5))


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

    try:
        position_on_screen = (screen.get_width()/2-screen.get_height()/2+position[0], position[1])

        pygame.draw.rect(screen, color, (position_on_screen[0], position_on_screen[1], 1, 1))
        if position[0] == screen.get_height()-1:
            pygame.display.update((position_on_screen[0]-screen.get_height()-1, position_on_screen[1], screen.get_height(), 1))
    except pygame.error:
        import sys
        sys.exit()


def init_pygame_window(height, width):
    """ Init pygame and create a window

    Parameters:
        height (int): height of the window in pixels
        width (int): width of the window in pixels

    Returns:

    """
    pygame.init()
    global screen
    screen = pygame.display.set_mode((width,height))
    global clock
    clock = pygame.time.Clock()

# _____________Main_Programm_________________ #

screen_height = 700
screen_width = 1200
depth = 70
zoom = 10
current_zoom = 1
current_center = (0, -0.75)
print(current_zoom, current_center, depth)
init_pygame_window(screen_height, screen_width)

thread1 = threading.Thread(target=draw_tile, args=(screen_height, screen_height, depth, current_center, current_zoom))
thread1.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not thread1.is_alive():
            if pygame.mouse.get_focused():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    x = x - (screen_width/2-screen_height/2)

                    if 0 <= x < screen_height:
                        global unit
                        x = x/screen_height*unit-(0.5*unit) + current_center[0]
                        y = y/screen_height*unit-(0.5*unit) + current_center[1]
                        current_zoom *= zoom
                        current_center = (x, y)
                        # depth += int(1/(zoom/6) * depth)
                        depth += 100
                        print(current_zoom, current_center, depth)

                        thread1 = threading.Thread(target=draw_tile, args=(screen_height, screen_height, depth, current_center, current_zoom))
                        thread1.start()
    clock.tick(60)

pygame.quit()