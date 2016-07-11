#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2010 Doug Hellmann.  All rights reserved.
#
"""Server half of echo example.
"""
#end_pymotw_header

from network_programming import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10002)
print "starting up on %s port %s" % server_address
sock.bind(server_address)

#set to non-blocking operation
#sock.setblocking(0)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print 'connection from', client_address

        #set to non-blocking operation
        #connection.setblocking(0)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print 'received "%s"' % data
            if data:
                print 'sending data back to the client'
                connection.sendall(data)
            else:
                print 'no data from', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()
