import yappi
from threading import Thread

yappi.start()
def test(n=100):
    return sum(x for x in xrange(n))
test(10000)
yappi.stop()

def recursive(n=100):
    if n == 0:
        return n
    return n+recursive(n-1)
yappi.start()
recursive(100)
yappi.stop()

yappi.start()
class TestThread(Thread):
    def __init__(self, n=100):
        Thread.__init__(self)
        self.n = n

    def run(self):
        self.output = sum(x for x in xrange(self.n))

t_list = []
for t_n in xrange(10):
    t = TestThread(100000)
    t_list.append(t)
    t.start()

for t in t_list:
    t.join()
    print t.output
yappi.stop()

print('\n'.join(yappi.get_stats()))
