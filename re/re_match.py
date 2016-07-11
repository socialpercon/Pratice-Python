#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Matching vs. searching
"""
#end_pymotw_header

import re

text = 'This is some text -- with punctuation.'
pattern = '.+ is.*'

print 'Text   :', text
print 'Pattern:', pattern

m = re.match(pattern, text)
print dir(m)
print 'Match  :', m
s = re.search(pattern, text)
print 'Search :', s


text = "id integer default 'abc'"
pattern = ".+ DEFAULT\\s+(.+)"
if re.matches(".+ DEFAULT\\s+.+", text):
    # if re.matches(".+ DEFAULT\\s+\".+\""):
    pass

    # else:

query_pattern = re.compile(pattern)
findall = query_pattern.findall(text.upper())
print str(findall[0])
