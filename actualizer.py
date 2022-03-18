import multiprocessing as mp
from time import sleep

from app.utils import class_updater

if __name__ == '__main__':
    while True:
        q = mp.Queue()
        p = mp.Process(target=class_updater)
        p.start()
        print(q.get())
        p.join()

        sleep(3600)
