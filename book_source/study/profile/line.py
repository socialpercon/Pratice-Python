import random, time

def sleep():
    seconds = random.randint(0, 5)
    print 'Sleeping %s seconds' % seconds
    time.sleep(seconds)

@profile
def test():
    sleep()
    sleep()
    sleep()

test()
