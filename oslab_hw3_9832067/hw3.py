import threading


class consumers_producers:
    def __init__(self, maximum):
        self.product = []
        self.size = 0
        self.full = maximum
        self._lock = threading.Lock()

    def isFull(self):
        return self.size == self.full

    def isEmpty(self):
        return self.size == 0

    def producer(self):
        if not self.isFull():
            self._lock.acquire()
            self.size += 1
            self.product.append(self.size)
            self._lock.release()
            print(self.product)
        else:
            print("Array is full!")

    def consumer(self):
        if not self.isEmpty():
            self._lock.acquire()
            self.size -= 1
            self.product.pop()
            self._lock.release()
            print(self.product)
        else:
            print("Nothing to consume!")


test = consumers_producers(10)
print(test.size)
threads = []
for i in range(11):
    threads.append(threading.Thread(target=test.producer))
for i in range(12):
    threads.append(threading.Thread(target=test.consumer))
for t in threads:
    t.start()
for t in threads:
    t.join()
