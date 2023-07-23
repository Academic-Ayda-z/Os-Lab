import threading


#     0 hungry    1 eating     2 thinking
class Monitor_DPH(object):
    def __init__(self):
        self.states = [2 for i in range(5)]
        self.lock = threading.Lock()
        self.lock1 = threading.Lock()
        self.lock2 = threading.Lock()
        self.forks = [threading.Condition(self.lock) for i in range(5)]

    def test(self, i):
        with self.lock1:
            if self.states[i] == 0 and self.states[(i + 1) % 5] != 1 and self.states[(i + 4) % 5] != 1:
                self.states[i] = 1  # eating
                self.forks[i].notify()


    def pickup_F(self, i):
        with self.lock:
            # hungry
            self.states[i] = 0
            self.test(i)
            # while state is not eating wait.
            if self.states[i] != 1:
                self.forks[i].acquire()
            else:
                print("pickup" + str(i))

    def putdown_F(self, i):
        with self.lock2:
            if self.states[i] == 1:
                print("putdown" + str(i))

            self.states[i] = 2
            # check for neighbors whither want to eat or not.
            # print(self.states)
            self.test((i + 1) % 5)
            #            print(self.states)
            self.test((i + 4) % 5)


#           print(self.states)

main = Monitor_DPH()
t = []
for i in range(5):
    w = threading.Thread(target=main.pickup_F, args=[i])
    t.append(w)
for i in range(5):
    w = threading.Thread(target=main.putdown_F, args=[i])
    t.append(w)
for x in t:
    x.start()
for k in t:
    k.join()
