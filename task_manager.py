#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      clene
#
# Created:     17/09/2023
# Copyright:   (c) clene 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------

try:
    import threading
except ImportError:
    raise ImportError('threading module not found')

try:
    import mandelbrot_core
except ImportError:
    raise ImportError("mandelbrot_core module not found")

class Task_Manager:

    task_list = []
    Pool = []


    def create_pool(self, number_of_workers):
        for worker in range(number_of_workers):
            self.Pool.append(threading.Thread())
        return self.Pool


    def start_processing(self):
        pass