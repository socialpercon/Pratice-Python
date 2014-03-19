#### EXAMPLE ##################################################################

from time import sleep
from threading import Thread
import random
import cProfile

def test_function():
    pass

class T(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run_profile(self):
        for i in xrange(100):
            self.test_method()
            test_function()
            
    def run(self):                  # takes about 5 seconds
        t = T()
        cProfile.run("t.run_profile()")

    def test_method(self):
        sleep(random.random() / 10)

#######################
threads = [T() for i in xrange(3)]
for t in threads:
    t.start()
for i in xrange(100):
    test_function()
for t in threads:
    t.join()
#######################
