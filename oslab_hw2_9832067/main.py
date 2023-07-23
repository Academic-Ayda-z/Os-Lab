import multiprocessing
import random
import threading

global result


def calc_sum(x):
    global result
    result += sum(x)


def sub_process(ls, start, end):
    threads = []
    #defult step
    x = 10
    for i in range(start, end, 10):
        if i + x > end:
            x = end - i
        t = threading.Thread(target=calc_sum(ls[i:i + x]))
       # print(result, i, start, end, ls[i:i + x])
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    ls_len = 10
    ls = []
    for i in range(ls_len):
        ls.append(random.randint(1, 5))
    process_no = 7
    processes = []
    sub_ls_len = ls_len // process_no
    index = 0
    result = 0
    for i in range(process_no):
        if i == process_no - 1:
            p = multiprocessing.Process(target=sub_process(ls, index, ls_len), )
        else:
            p = multiprocessing.Process(target=sub_process(ls, index, index + sub_ls_len), )
        processes.append(p)
        p.start()
        index += sub_ls_len

    for p in processes:
        p.join()
print("The input Array is : {}\nThe result is : {}\nThe Real sum is : {}".format(ls, result, sum(ls)))
