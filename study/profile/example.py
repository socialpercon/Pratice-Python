import time

def my_func():
    time.sleep(3)
    a = [1] * (10 ** 6)
    time.sleep(3)
    b = [2] * (2 * 10 ** 7)
    time.sleep(3)
    #del b
    #time.sleep(3)
    return a

if __name__ == '__main__':
    for i in range(100):
        my_func()
