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
    number_of_workers = 1
    Pool = []


    def create_pool(self, number_of_workers):
        """ Prepare a set of threads in a usable space """

        for worker in range(number_of_workers):
            self.Pool.append(threading.Thread())
        return self.Pool


    def start_processing(self):
        """ Execute the task list entirely with async threads """

        while len(self.task_list) > 0:
            for worker in self.Pool:
                if not worker.is_alive() and len(self.task_list) != 0:
                    (target, args) = self.task_list.pop(0)
                    worker = threading.Thread(target=target, args=args)
                    worker.start()