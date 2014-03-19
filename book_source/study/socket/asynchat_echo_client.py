#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2009 Doug Hellmann All rights reserved.
#
"""
"""
#end_pymotw_header

import asynchat
import socket


class EchoClient(asynchat.async_chat):
    """Sends messages to the server and receives responses.
    """

    # Artificially reduce buffer sizes to show
    # sending and receiving partial messages.
    ac_in_buffer_size = 128
    ac_out_buffer_size = 128
    
    def __init__(self, host, port, message):
        self.message = message
        self.received_data = []
        print('EchoClient')
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'connecting to %s %s' % (host, port)
        self.connect((host, port))
        return
        
    def handle_connect(self):
        print('handle_connect()')
        # Send the command
        self.push('ECHO %d\n' % len(self.message))
        # Send the data
        self.push_with_producer(
            EchoProducer(self.message,
                         buffer_size=self.ac_out_buffer_size)
            )
        # We expect the data to come back as-is, 
        # so set a length-based terminator
        self.set_terminator(len(self.message))
    
    def collect_incoming_data(self, data):
        """Read an incoming message from the client
        and add it to the outgoing queue.
        """
        print 'collect_incoming_data() -> (%d) %r' % (len(data), data)
        self.received_data.append(data)

    def found_terminator(self):
        print('found_terminator()')
        received_message = ''.join(self.received_data)
        if received_message == self.message:
            print('RECEIVED COPY OF MESSAGE')
        else:
            print('ERROR IN TRANSMISSION')
            print 'EXPECTED %r' % self.message
            print 'RECEIVED %r' % received_message
        return

class EchoProducer(asynchat.simple_producer):


    def more(self):
        response = asynchat.simple_producer.more(self)
        print "more() -> (%s bytes) %r" % (len(response), response)
        return response


if __name__ == "__main__":
    import asyncore
    client = EchoClient('localhost', 9777, message="test1")
    client = EchoClient('localhost', 9777, message="test2")
    client = EchoClient('localhost', 9777, message="test3")
    asyncore.loop()
