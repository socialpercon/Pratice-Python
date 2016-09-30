#!/usr/bin/env python

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 25826))

print 'socket created'
print 'connection wait...'

while True:
        message, client = sock.recvfrom(1024)
        out = ""
        for i in list(message):
            if ord(i) >= 0 and ord(i) <= 31:
                out = out + str(ord(i)) + ','
            else:
                out = out + i
        print out + '\n'

sock.close()