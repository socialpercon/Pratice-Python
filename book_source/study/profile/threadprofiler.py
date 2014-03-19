from profile import Profile
from threading import Lock
import threading
import sys

def run(statement, filename=None, sort=-1):
    """Run statement under profiler optionally saving results in filename

    This function takes a single argument that can be passed to the
    "exec" statement, and an optional file name.  In all cases this
    routine attempts to "exec" its first argument and gather profiling
    statistics from the execution. If no file name is present, then this
    function automatically prints a simple profiling report, sorted by the
    standard name string (file/line/function-name) that is presented in
    each line.
    """
    prof = ThreadProfile()
    #~ print prof.timer, prof.get_time
    try:
        prof = prof.run(statement)
    except SystemExit:
        pass
    if filename is not None:
        prof.dump_stats(filename)
    else:
        return prof.print_stats(sort)

class ThreadProfile(Profile):
    def __init__(self, *args, **kws):
        self._lock = Lock()
        self._local = threading.local()
        self._local.cur = None
    
        Profile.__init__( self, *args, **kws )
        
    # Heavily optimized dispatch routine for os.times() timer

    def trace_dispatch(self, frame, event, arg):
        self._lock.acquire()
        try:
            if not hasattr( self._local, "t" ):
                self._local.t = self.get_time()
            
            timer = self.timer
            t = timer()
            t = t[0] + t[1] - self._local.t - self.bias
    
            if event == "c_call":
                self._local.c_func_name = arg.__name__
    
            if self.dispatch[event](self, frame,t):
                t = timer()
                self._local.t = t[0] + t[1]
            else:
                r = timer()
                self._local.t = r[0] + r[1] - t # put back unrecorded delta
        finally:
            self._lock.release()

    # Dispatch routine for best timer program (return = scalar, fastest if
    # an integer but float works too -- and time.clock() relies on that).

    def trace_dispatch_i(self, frame, event, arg):
        self._lock.acquire()
        try:
            if not hasattr( self._local, "t" ):
                self._local.t = self.get_time()
            
            timer = self.timer
            t = timer() - self._local.t - self.bias
    
            if event == "c_call":
                self._local.c_func_name = arg.__name__
    
            if self.dispatch[event](self, frame, t):
                self._local.t = timer()
            else:
                self._local.t = timer() - t  # put back unrecorded delta
        finally:
            self._lock.release()

    # Dispatch routine for macintosh (timer returns time in ticks of
    # 1/60th second)

    def trace_dispatch_mac(self, frame, event, arg):
        self._lock.acquire()
        try:
            if not hasattr( self._local, "t" ):
                self._local.t = self.get_time()
            
            timer = self.timer
            t = timer()/60.0 - self._local.t - self.bias
    
            if event == "c_call":
                self._local.c_func_name = arg.__name__
    
            if self.dispatch[event](self, frame, t):
                self._local.t = timer()/60.0
            else:
                self._local.t = timer()/60.0 - t  # put back unrecorded delta
        finally:
            self._lock.release()

    # SLOW generic dispatch routine for timer returning lists of numbers

    def trace_dispatch_l(self, frame, event, arg):
        self._lock.acquire()
        try:
            get_time = self.get_time
            
            if not hasattr( self._local, "t" ):
                self._local.t = get_time()
            
            t = get_time() - self._local.t - self.bias
    
            if event == "c_call":
                self._local.c_func_name = arg.__name__
    
            if self.dispatch[event](self, frame, t):
                self._local.t = get_time()
            else:
                self._local.t = get_time() - t # put back unrecorded delta
        finally:
            self._lock.release()

    # In the event handlers, the first 3 elements of self._local.cur are unpacked
    # into vrbls w/ 3-letter names.  The last two characters are meant to be
    # mnemonic:
    #     _pt  self._local.cur[0] "parent time"   time to be charged to parent frame
    #     _it  self._local.cur[1] "internal time" time spent directly in the function
    #     _et  self._local.cur[2] "external time" time spent in subfunctions

    def trace_dispatch_exception(self, frame, t):
        rpt, rit, ret, rfn, rframe, rcur = self._local.cur
        if (rframe is not frame) and rcur:
            return self.trace_dispatch_return(rframe, t)
        self._local.cur = rpt, rit+t, ret, rfn, rframe, rcur
        return 1

    def trace_dispatch_call(self, frame, t):
        if not hasattr( self._local, "cur" ):
            self._local.cur = None
        
        if self._local.cur and frame.f_back is not self._local.cur[-2]:
            rpt, rit, ret, rfn, rframe, rcur = self._local.cur
            if not isinstance(rframe, Profile.fake_frame):
                assert rframe.f_back is frame.f_back, ("Bad call", rfn,
                                                       rframe, rframe.f_back,
                                                       frame, frame.f_back)
                self.trace_dispatch_return(rframe, 0)
                assert (self._local.cur is None or \
                        frame.f_back is self._local.cur[-2]), ("Bad call",
                                                        self._local.cur[-3])
        fcode = frame.f_code
        fn = (fcode.co_filename, fcode.co_firstlineno, fcode.co_name)
        self._local.cur = (t, 0, 0, fn, frame, self._local.cur)
        timings = self.timings
        if fn in timings:
            cc, ns, tt, ct, callers = timings[fn]
            timings[fn] = cc, 0, tt, ct, callers
        else:
            timings[fn] = 0, 0, 0, 0, {}
        
        if not hasattr( self._local, "stack_func_counts" ):
            self._local.stack_func_counts = {}
        
        if fn in self._local.stack_func_counts:
            self._local.stack_func_counts[fn] += 1
        else:
            self._local.stack_func_counts[fn] = 0
        
        return 1

    def trace_dispatch_c_call (self, frame, t):
        fn = ("<C Module>", 0, self._local.c_func_name)
        self._local.cur = (t, 0, 0, fn, frame, self._local.cur)
        timings = self.timings
        if timings.has_key(fn):
            cc, ns, tt, ct, callers = timings[fn]
            timings[fn] = cc, 0, tt, ct, callers
        else:
            timings[fn] = 0, 0, 0, 0, {}
        
        if not hasattr( self._local, "stack_func_counts" ):
            self._local.stack_func_counts = {}
        
        if fn in self._local.stack_func_counts:
            self._local.stack_func_counts[fn] += 1
        else:
            self._local.stack_func_counts[fn] = 0
        return 1

    def trace_dispatch_return(self, frame, t):
        #if self._local.cur is None:
        #    print "threadprofiler return weirdness."
        #    return 1
        
        if self._local.cur[-3] == ("profile", 0, "<After last return>"):
            print "threadprofiler return weirdness."
            return 1
        
        if frame is not self._local.cur[-2]:
            assert frame is self._local.cur[-2].f_back, ("Bad return", self._local.cur[-3])
            self.trace_dispatch_return(self._local.cur[-2], 0)

        # Prefix "r" means part of the Returning or exiting frame.
        # Prefix "p" means part of the Previous or Parent or older frame.

        rpt, rit, ret, rfn, frame, rcur = self._local.cur
        rit = rit + t
        frame_total = rit + ret
        
        if rcur is not None:
            ppt, pit, pet, pfn, pframe, pcur = rcur
            self._local.cur = ppt, pit + rpt, pet + frame_total, pfn, pframe, pcur
        else:
            print "returning in ", self._local.cur
            self._local.cur = (0,0,0,("profile", 0, "<After last return>"), self.fake_frame(self.fake_code('profile', 0, "<After last return>"), None), None)
            pfn = ("profile", 0, "<After last return>")

        timings = self.timings
        cc, ns, tt, ct, callers = timings[rfn]
        ns = self._local.stack_func_counts[rfn]
        
        if not ns:
            # This is the only occurrence of the function on the stack.
            # Else this is a (directly or indirectly) recursive call, and
            # its cumulative time will get updated when the topmost call to
            # it returns.
            ct = ct + frame_total
            cc = cc + 1
        
        if pfn != ("profile", 0, "<After last return>"):
            if pfn in callers:
                callers[pfn] = callers[pfn] + 1  # hack: gather more
                # stats such as the amount of time added to ct courtesy
                # of this specific call, and the contribution to cc
                # courtesy of this call.
            else:
                callers[pfn] = 1

        timings[rfn] = cc, 0, tt + rit, ct, callers
        self._local.stack_func_counts[rfn] -= 1

        return 1


    dispatch = {
        "call": trace_dispatch_call,
        "exception": trace_dispatch_exception,
        "return": trace_dispatch_return,
        "c_call": trace_dispatch_c_call,
        "c_exception": trace_dispatch_exception,
        "c_return": trace_dispatch_return,
        }

    # The next few functions play with self.cmd. By carefully preloading
    # our parallel stack, we can force the profiled result to include
    # an arbitrary string as the name of the calling function.
    # We use self.cmd as that string, and the resulting stats look
    # very nice :-).

    def set_cmd(self, cmd):
        if self._local.cur[-1]: return   # already set
        self.cmd = cmd
        self.simulate_call(cmd)

    def simulate_call(self, name):
        code = self.fake_code('profile', 0, name)
        
        if not hasattr( self._local, "cur" ):
            self._local.cur = None
        
        if self._local.cur:
            pframe = self._local.cur[-2]
        else:
            pframe = None
        frame = self.fake_frame(code, pframe)
        self.dispatch['call'](self, frame, 0)

    # collect stats from pending stack, including getting final
    # timings for self.cmd frame.

    def simulate_cmd_complete(self):
        get_time = self.get_time
        t = get_time() - self._local.t
        while self._local.cur[-1]:
            # We *can* cause assertion errors here if
            # dispatch_trace_return checks for a frame match!
            self.dispatch['return'](self, self._local.cur[-2], t)
            t = 0
        self._local.t = get_time() - t

    def runctx(self, cmd, globals, locals):
        self.set_cmd(cmd)
        threading.setprofile(self.dispatcher)
        sys.setprofile(self.dispatcher)
        try:
            exec cmd in globals, locals
        finally:
            sys.setprofile(None)
            threading.setprofile(None)
        return self

    # This method is more useful to profile a single function call.
    def runcall(self, func, *args, **kw):
        self.set_cmd(repr(func))
        threading.setprofile(self.dispatcher)
        sys.setprofile(self.dispatcher)
        try:
            return func(*args, **kw)
        finally:
            sys.setprofile(None)
            threading.setprofile(None)

    def calibrate(self, m, verbose=0):
        saved_bias = self.bias
        self.bias = 0
        try:
            return self._calibrate_inner(m, verbose)
        finally:
            self.bias = saved_bias
    
    def _calibrate_inner(self, m, verbose):
        get_time = self.get_time

        # Set up a test case to be run with and without profiling.  Include
        # lots of calls, because we're trying to quantify stopwatch overhead.
        # Do not raise any exceptions, though, because we want to know
        # exactly how many profile events are generated (one call event, +
        # one return event, per Python-level call).

        def f1(n):
            for i in range(n):
                x = 1

        def f(m, f1=f1):
            for i in range(m):
                f1(100)

        f(m)    # warm up the cache

        # elapsed_noprofile <- time f(m) takes without profiling.
        t0 = get_time()
        f(m)
        t1 = get_time()
        elapsed_noprofile = t1 - t0
        if verbose:
            print "elapsed time without profiling =", elapsed_noprofile

        # elapsed_profile <- time f(m) takes with profiling.  The difference
        # is profiling overhead, only some of which the profiler subtracts
        # out on its own.
        p = ThreadProfile()
        t0 = get_time()
        p.runctx('f(m)', globals(), locals())
        t1 = get_time()
        elapsed_profile = t1 - t0
        if verbose:
            print "elapsed time with profiling =", elapsed_profile

        # reported_time <- "CPU seconds" the profiler charged to f and f1.
        total_calls = 0.0
        reported_time = 0.0
        for (filename, line, funcname), (cc, ns, tt, ct, callers) in \
                p.timings.items():
            if funcname in ("f", "f1"):
                total_calls += cc
                reported_time += tt

        if verbose:
            print "'CPU seconds' profiler reported =", reported_time
            print "total # calls =", total_calls
        if total_calls != m + 1:
            raise ValueError("internal error: total calls = %d" % total_calls)

        # reported_time - elapsed_noprofile = overhead the profiler wasn't
        # able to measure.  Divide by twice the number of calls (since there
        # are two profiler events per call in this test) to get the hidden
        # overhead per event.
        mean = (reported_time - elapsed_noprofile) / 2.0 / total_calls
        if verbose:
            print "mean stopwatch overhead per profile event =", mean
        return mean

if __name__ == "__main__":
    
    import time
    prof = ThreadProfile(time.time)
    print prof.calibrate(20000)
    print prof.calibrate(20000)
    print prof.calibrate(20000)
    print prof.calibrate(20000)
    
    #### EXAMPLE ##################################################################
    
    from time import sleep
    from threading import Thread
    import random
    
    def test_function():
        pass
    
    class T(Thread):
        def __init__(self):
            Thread.__init__(self)
        def run(self):                  # takes about 5 seconds
            for i in xrange(100):
                #self.test_method()
                test_function()
        def test_method(self):
            pass

    def test_start():
        #######################
        threads = [T() for i in xrange(3)]
        for t in threads:
            t.start()
        for i in xrange(100):
            test_function()
        for t in threads:
            t.join()
        #######################
    
    prof = ThreadProfile(time.time)
    prof.bias = 2e-06
    prof.runcall( test_start )
    prof.dump_stats('calltest.out')
    prof.print_stats()
        
    #from pstats import Stats
    
    #import pdb; pdb.set_trace()
    #Stats("profile.out").strip_dirs().sort_stats("calls").print_stats()
