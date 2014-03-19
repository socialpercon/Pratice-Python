#!/usr/bin/env python
# encoding: utf-8
#

__version__ = "$Id$"
#end_pymotw_header

import asyncore
import logging


class EchoClient(asyncore.dispatcher):
    """Sends messages to the server and receives responses.
    """
    
    def __init__(self, host, port, message, chunk_size=128):
        self.message = message
        self.to_send = message
        self.received_data = []
        self.chunk_size = chunk_size
        self.logger = logging.getLogger('EchoClient')
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.debug('connecting to %s', (host, port))
        self.connect((host, port))
        return
        
    def handle_connect(self):
        self.logger.debug('handle_connect()')
    
    def handle_close(self):
        self.logger.debug('handle_close()')
        self.close()
        received_message = ''.join(self.received_data)
        if received_message == self.message:
            self.logger.debug('RECEIVED COPY OF MESSAGE')
        else:
            self.logger.debug('ERROR IN TRANSMISSION')
            self.logger.debug('EXPECTED "%s"', self.message)
            self.logger.debug('RECEIVED "%s"', received_message)
        return
    
    def writable(self):
        self.logger.debug('writable() -> %s', bool(self.to_send))
        return bool(self.to_send)
    
    def readable(self):
        self.logger.debug('readable() -> True')
        return True

    def handle_write(self):
        sent = self.send(self.to_send[:self.chunk_size])
        self.logger.debug('handle_write() -> (%d) %r',
                          sent, self.to_send[:sent])
        self.to_send = self.to_send[sent:]

    def handle_read(self):
        data = self.recv(self.chunk_size)
        self.logger.debug('handle_read() -> (%d) %r',
                          len(data), data)
        self.received_data.append(data)

if __name__ == "__main__":
    import socket

    message = open('lorem.txt', 'r').read()
    logging.info('Total message length: %d bytes', len(message))
    client = EchoClient("localhost", 9090, message=message)
    #client = [EchoClient("localhost", 9090, message="1"), EchoClient("localhost", 9090, message="2"), EchoClient("localhost", 9090, message="3")]

    asyncore.loop()
