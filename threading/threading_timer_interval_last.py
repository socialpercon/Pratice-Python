from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.start()

    def _run(self):
        if self.is_running:
            self.function(*self.args, **self.kwargs)
            self.schedule()

    def schedule(self):
        self._timer = Timer(self.interval, self._run)
        self._timer.start()
        
    def start(self):
        self.is_running = True
        self.schedule()

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def main():
    from time import sleep

    def hello(name):
        print "Hello %s!" % name

    print "starting..."
    rt = RepeatedTimer(1, hello, "World") # it auto-starts, no need of rt.start()
    try:
        sleep(5) # your long-running job goes here...
    finally:
        rt.stop() # better in a try/finally block to make sure the program ends!

if __name__ == '__main__':
    main()
