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

try:
    import tkinter_displayer as display
except ImportError:
    raise ImportError("tkinter_displayer module not found")

import time

class Task_Manager:

    task_list = []
    Pool = []
    display = None

    def __init__(self, display):

        # print("Task_Manager.__init__", display, threading.current_thread().name)

        self.display = display


    def create_lonely_thread(self):

        # print("Task_Manager.create_lonely_thread", threading.current_thread().name)

        employer = threading.Thread(target=self.start_processing, name="employer")
        employer.start()


    def create_pool(self, number_of_workers):
        """ Prepare a set of threads in a usable space """

        # print("Task_Manager.create_pool", number_of_workers, threading.current_thread().name)

        for worker in range(number_of_workers):
            self.Pool.append(My_Thread(display=self.display, name=f"Worker {worker+1}", args=[None, None, None, None]))

    @profile
    def start_processing(self):
        """ Execute the task list entirely with async threads """

        starting_time = time.time()
        while len(self.task_list) > 0:

            for space_number in range(len(self.Pool)):
                # print(self.Pool[space_number].Thread.name, self.Pool[space_number].state, f"row {self.Pool[space_number].args[3]}", end="  ")
                if self.Pool[space_number].state != 'RUNNING' and len(self.task_list) != 0:

                    # print(self.Pool[space_number].Thread.name, f"row {self.Pool[space_number].args[3]}", end="   ")
                    (target, args) = self.task_list.pop(0)
                    self.Pool[space_number] = My_Thread(target=target,
                                                        args=args,
                                                        display=self.display,
                                                        manager=self,
                                                        name=self.Pool[space_number].name
                                                       )
                    self.Pool[space_number].start()
            # print("")
        print(time.time()-starting_time)


class My_Thread:

    result = None
    state = None
    target = None
    args = []
    Thread = None
    display = None
    manager = None
    name = None
    time = 0

    def __init__(self, target=None, args=None, display=None, manager=None, name=None, time=0):
        self.state = 'INIT'
        self.target = target
        self.args = args
        self.display = display
        self.manager = manager
        self.name = name
        self.time = time
        self.Thread = threading.Thread(target=self.task, args=[], name=self.name)

    @profile
    def start(self):
        self.state = 'RUNNING'
        self.Thread.start()

    @profile
    def task(self):
        self.result = self.target(*self.args)
        self.display.result_queue.append(self.result)
        self.state = 'DEAD'