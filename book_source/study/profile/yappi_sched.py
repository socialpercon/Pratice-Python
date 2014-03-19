import time
import yappi
from threading import Timer

def print_time():
    print "From print_time", time.time()

def print_some_times():
    print time.time()
    print_time()
    print_time()
    print time.time()

yappi.start()
print_some_times()
yappi.get_thread_stats().print_all()
