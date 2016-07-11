#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Look up the name of the current host
"""
#end_pymotw_header

from network_programming import socket

print socket.gethostname()
