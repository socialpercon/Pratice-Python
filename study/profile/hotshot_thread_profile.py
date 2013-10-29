#### EXAMPLE ##################################################################

from time import sleep
from threading import Thread
import random
import hotshot, hotshot.stats

def test_function():
    pass

class T(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):                  # takes about 5 seconds
        for i in xrange(100):
            self.test_method()
            test_function()

    def test_method(self):
        sleep(random.random() / 10)

profile_filename = "prof.result"
prof = hotshot.Profile(profile_filename)
prof.start()
#######################
threads = [T() for i in xrange(3)]
for t in threads:
    t.start()
for i in xrange(100):
    test_function()
for t in threads:
    t.join()
#######################
prof.stop()
prof.close()
stats = hotshot.stats.load(profile_filename)
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats()
