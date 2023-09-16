#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Ocean6
#
# Created:     06/06/2023
# Copyright:   (c) Ocean6 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from threading import Thread
from multiprocessing import Pool


import time


def a(time_to_sleep,message):
    """

    :param time_to_sleep: (Double) the time in sec
    :param message: (String) the message to return
    """
    t1 = time.time()
    time.sleep(time_to_sleep)
    print(message, time.time()-t1)




class MonThread(Thread):
    def __init__(self, time_to_sleep, message):
        super(MonThread, self).__init__()
        self.time_to_sleep = time_to_sleep
        self.message = message

    def run(self):

        t1 = time.time()

        time.sleep(self.time_to_sleep)
        print(self.message, time.time() - t1)


if __name__ == '__main__':
    thread1=Thread(target=a,args=(3, "thread1 termine"))
    thread2=Thread(target=a,args=( 6, "thread2 termine"))

    thread1.start()
    thread2.start()
    print("le thread principal continue")

    thread1.join()
    print('j attend la fin du thread 1')
    thread2.join()
    print('j attend a fin du thread 2')

    print("par classe")

    thread1= MonThread(2, "thead3")
    thread2 = MonThread(4, "thread4")
    thread2.start()
    thread1.start()
    thread2.join()
    thread1.join()
    print("fin")
    print("multiprocess")


   # La fonction Pool est une méthode simple pour faire plusieurs fois la même fonction avec des arguments différents
    with Pool(2)as p:
        p.starmap(a, [(1, "01"), (2, '02')])