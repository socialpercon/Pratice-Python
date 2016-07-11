#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Look up the fully qualified domain name for a host.
"""
#end_pymotw_header

from network_programming import socket

for host in [ 'homer', 'www' ]:
    print '%6s : %s' % (host, socket.getfqdn(host))
