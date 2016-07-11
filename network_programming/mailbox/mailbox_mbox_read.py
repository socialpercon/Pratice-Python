#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id$"
#end_pymotw_header

from network_programming import mailbox

mbox = mailbox.mbox('example.mbox')
for message in mbox:
    print message['subject']
