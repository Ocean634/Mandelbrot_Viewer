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
    number_of_workers = 1
    Pool = []
    display = None

    def __init__(self, display):

        print("Task_Manager.__init__", display, threading.current_thread().name)

        self.display = display


    def create_lonely_thread(self):

        print("Task_Manager.create_lonely_thread", threading.current_thread().name)

        employer = threading.Thread(target=self.start_processing, name="employer")
        employer.start()


    def create_pool(self, number_of_workers):
        """ Prepare a set of threads in a usable space """

        print("Task_Manager.create_pool", number_of_workers, threading.current_thread().name)

        for worker in range(number_of_workers):
            self.Pool.append(My_Thread(display=self.display))


    def start_processing(self):
        """ Execute the task list entirely with async threads """

        print("Task_Manager.start_processing", threading.current_thread().name)

        while len(self.task_list) > 0:
            for worker in self.Pool:
                if worker.state != 'RUNNING' and len(self.task_list) != 0:
                    (target, args) = self.task_list.pop(0)
                    worker = My_Thread(target=target,
                                       args=args,
                                       display=self.display,
                                       manager=self
                                      )
                    worker.start()


class My_Thread:

    result = None
    state = None
    target = None
    args = []
    Thread = None
    display = None
    manager = None

    def __init__(self, target=None, args=None, display=None, manager=None):

        print("My_Thread.__init__", target, args, display, manager, threading.current_thread().name)
        self.state = 'INIT'
        if target:
            self.target = target
        if args:
            self.args = args
        if display:
            self.display = display
        if manager:
            self.manager = manager
        self.Thread = threading.Thread(target=self.task, args=[])


    def start(self):
        self.state = 'RUNNING'
        print("My_Thread.start", threading.current_thread().name)
        self.Thread.start()


    def task(self):

        print("My_Thread.task", threading.current_thread().name)
        self.result = self.target(*self.args)
        self.display.result_queue.append(self.result)
        self.state = 'DEAD'