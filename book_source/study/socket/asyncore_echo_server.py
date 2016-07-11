#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann All rights reserved.
#
"""
"""

import network_programming.asyncore
from network_programming import socket, asyncore


class EchoServer(asyncore.dispatcher):
    """Receives connections and establishes handlers for each client.
    """
    
    def __init__(self, host, port):
        print 'EchoServer'
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        self.bind((host, port))
        self.address = self.socket.getsockname()
        print "binding to %s" % (str(self.address))
        self.listen(1)
        return

    def handle_accept(self):
        # Called when a client connects to the socket

        client_info = self.accept()
        if client_info is not None:
            sock, addr = client_info
            print 'handle_accept() -> %s' % str(addr)
            EchoHandler(sock=sock)
        # Only deal with one client at a time,
        # so close as soon as the handler is set up.
        # Under normal conditions, the server
        # would run forever or until it received
        # instructions to stop.
        #self.handle_close()
        return

    def handle_close(self):
        self.close()
        return
    

class EchoHandler(asyncore.dispatcher):
    """Handles echoing messages from a single client.
    """
    
    def __init__(self, sock, chunk_size=256):
        self.chunk_size = chunk_size
        print 'init EchoHandler'
        asyncore.dispatcher.__init__(self, sock=sock)
        self.data_to_write = []
        return
    
    def writable(self):
        """Write if data has been received."""
        response = bool(self.data_to_write)
        #print 'writable() -> %s' % response
        return response
    
    def handle_write(self):
        """Write as much as possible of the
        most recent message received.
        """
        data = self.data_to_write.pop()
        sent = self.send(data[:self.chunk_size])
        if sent < len(data):
            remaining = data[sent:]
            self.data.to_write.append(remaining)
        #print 'handle_write() -> (%d) %r' % (sent, data[:sent])
        if not self.writable():
            self.handle_close()

    def handle_read(self):
        """Read an incoming message from the client
        and put it into the outgoing queue.
        """
        data = self.recv(self.chunk_size)
        #print 'handle_read() -> (%d) %r' % (len(data), data)
        self.data_to_write.insert(0, data)
    
    def handle_close(self):
        print('handle_close()')
        self.close()

        

if __name__ == '__main__':
    import pdb
    pdb.set_trace()
    #address = ('localhost', 9090) # let the kernel assign a port
    server = EchoServer('localhost', 9090)
    asyncore.loop()
