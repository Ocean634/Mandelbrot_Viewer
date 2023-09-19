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
    result_queue = []

    def __init__(self, display):
        self.display = display


    def create_lonely_thread(self):
        employer = threading.Thread(target=self.start_processing, name="employer")
        employer.start()


    def create_pool(self, number_of_workers):
        """ Prepare a set of threads in a usable space """

        for worker in range(number_of_workers):
            self.Pool.append(My_Thread(display=self.display))


    def start_processing(self):
        """ Execute the task list entirely with async threads """
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


    def thread_end(self, event):
        result = []
        data = self.result_queue.pop(0)
        # treatment function / palette
        for pixel in data[0]:
            if pixel == mandelbrot_core.max_iterations-1:
                result.append((0, 0, 0))
            else:
                result.append((1, 1, 1))

        self.display.draw_line(result, data[1])


class My_Thread:

    result = None
    state = None
    target = None
    args = []
    Thread = None
    display = None
    manager = None

    def __init__(self, target=None, args=None, display=None, manager=None):
        if target:
            self.target = target
        if args:
            self.args = args
        if display:
            self.display = display
        if manager:
            self.manager = manager
        self.Thread = threading.Thread(target=self.task, args=[])
        self.state = 'INIT'


    def start(self):
        self.Thread.start()
        self.state = 'RUNNING'


    def task(self):
        self.result = self.target(*self.args)
        self.manager.result_queue.append(self.result)
        self.display.Master.event_generate('<<Thread_finished>>')
        self.state = 'DEAD'