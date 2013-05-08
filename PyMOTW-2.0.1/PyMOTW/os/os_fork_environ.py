#!/usr/bin/python
# -*- coding: utf8 -*-

__module_id__ = "$Id$"
import os


# 지정한 특정 환경변수 출력
s = os.environ['PYTHONPATH']="~usr/home"
print s
pid = os.fork()

if pid:
    print 'Child process id:', pid
else:
    print 'I am the child'
    p = os.environ['PYTHONPATH']
    print p
