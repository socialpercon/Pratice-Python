#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

import hotshot, hotshot.stats

def test_func2(i):
    result = i * 10
    return result

def test_func1(i):
    test_func2(i)
    result = 1 * i
    return result

profile_filename = "prof.result"
prof = hotshot.Profile(profile_filename)
prof.start()

sum = 0
for i in range(10000):
    sum = sum + i
    test_func1(i)
print sum

prof.stop()
prof.close()
stats = hotshot.stats.load(profile_filename)
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats()


