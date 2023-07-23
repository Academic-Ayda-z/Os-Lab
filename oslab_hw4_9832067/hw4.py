import threading
import random


class smoke:
    def __init__(self):
        self.supplier_flag = False
        self.supplies = [False, False, False]
        self.lock = threading.Lock()

    def supplier(self):
        self.lock.acquire()
        x = random.randint(0, 2)
        self.supplies[x] = False
        for i in range(3):
            if i != x:
                self.supplies[i] = True
        print(x+1)
        self.supplier_flag=True
        self.lock.release()

    def check(self, turn):
        self.lock.acquire()
        if not self.supplies[turn] and self.supplier_flag:
            self.supplies = [False for i in range(3)]
            self.supplier_flag=False
            self.lock.release()
            return True
        self.lock.release()
        return False

    def smoker0(self):
        if self.check(0):
            print("Smoker1 smoked.")

    def smoker1(self):
        if self.check(1):
            print("Smoker2 smoked.")

    def smoker2(self):
        if self.check(2):
            print("Smoker3 smoked.")


threads = []
test = smoke()
for i in range(20):
    threads.append(threading.Thread(test.supplier()))
    threads.append(threading.Thread(test.smoker0()))
    threads.append(threading.Thread(test.smoker1()))
    threads.append(threading.Thread(test.smoker2()))
