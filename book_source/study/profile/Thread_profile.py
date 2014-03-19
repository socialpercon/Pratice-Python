from threading import Thread
 
import cProfile
import pstats
 
def enable_thread_profiling():
    '''Monkey-patch Thread.run to enable global profiling.
    Each thread creates a local profiler; statistics are pooled
    to the global stats object on run completion.'''
    Thread.stats = None
    thread_run = Thread.run
               
    def profile_run(self):
        self._prof = cProfile.Profile()
        self._prof.enable()
        thread_run(self)
        self._prof.disable()

        if Thread.stats is None:
            Thread.stats = pstats.Stats(self._prof)
        else:
            Thread.stats.add(self._prof)

        Thread.run = profile_run

def get_thread_stats():
    stats = getattr(Thread, 'stats', None)
    if stats is None:
        raise ValueError, 'Thread profiling was not enabled,'\
                'or no threads finished running.'
    return stats

if __name__ == '__main__':
    enable_thread_profiling()
    import time
    t = Thread(target=time.sleep, args=(1,))
    t.start()
    t.join()

    get_thread_stats().print_stats()
