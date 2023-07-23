import threading
import random
from threading import *


class Obj:
    def __init__(self, data):
        self.lock = threading.Lock()
        self.data = data


class worker_producer:
    array = []
    lock = threading.Lock()
    lock1 = threading.Lock()
    find = {}
    worker_semaphore = Semaphore(10)
    mutex = threading.Lock()
    producers_semaphore = Semaphore(3)

    @staticmethod
    def worker(x):
        founded = False
        worker_producer.worker_semaphore.acquire()
        for key in worker_producer.find.keys():
            if founded:
                break
            item = worker_producer.find[key]
            if not item[0]:  # have not found yet
                OBJ = worker_producer.array[key]
                data = OBJ.data
                OBJ.lock.acquire(blocking=True)
                for j in range(len(worker_producer.array)):
                    array_data = worker_producer.array[j].data
                    if item[0]:  # founded
                        founded = True
                        break

                    if j not in list(item[1]) and key != j:
                        item[1].add(j)
                        if data[::-1] == array_data:
                            # print(worker_producer.find,key)
                            print(f"worker{x} found {key} inverse in index {j} !")
                            item[0] = True
                            item[2] = key

                OBJ.lock.release()

        worker_producer.worker_semaphore.release()

    @staticmethod
    def producer():
        worker_producer.producers_semaphore.acquire()
        data = []
        for j in range(2):#(30):
            num = random.randint(0, 1)
            data.append(num)

        worker_producer.array.append(Obj(data))
        worker_producer.find[len(worker_producer.array) - 1] = [False, set(), None]
        worker_producer.producers_semaphore.release()


producers = []
workers = []
for l in range(10):
    producers.append(threading.Thread(target=worker_producer.producer, args=[]))
for k in range(10):
    workers.append(threading.Thread(target=worker_producer.worker, args=[k]))
for p in producers:
    p.start()
for p in producers:
    p.join()

for w in workers:
    w.start()
for w in workers:
    w.join()
# print(worker_producer.find)
