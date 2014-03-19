#!/usr/bin/python
# -*- coding: utf8 -*-

import os


# 지정한 특정 환경변수 출력
s = os.environ['PATH']
print s




# 모든 환경변수 출력
keys = os.environ.keys()
keys.sort()

for item in keys:
  print "%s=%s" % (item, os.environ[item])
