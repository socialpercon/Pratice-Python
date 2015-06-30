#!/usr/bin/env python
# encoding: utf-8

import socket, ssl
import os


def deal_with_client(connstream):
    data = connstream.read()
    # null data means the client is finished with us
    while data:
        if not do_something(connstream, data):
            break
        data = connstream.read()

def do_something(connstream, data):
    print data
    connstream.write('pong')

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 7474

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    mycertfile=os.path.join(os.path.dirname(__file__),'mycertfile')
    mykeyfile=os.path.join(os.path.dirname(__file__),'mykeyfile')
    context.load_cert_chain(certfile=mycertfile, keyfile=mykeyfile)
    bindsocket = socket.socket()
    bindsocket.bind((host, port))
    bindsocket.listen(5)
    while True:
        newsocket, fromaddr = bindsocket.accept()
        connstream = ssl.wrap_socket(newsocket, server_side=True, certfile=mycertfile, keyfile=mykeyfile)
        try:
            deal_with_client(connstream)
        finally:
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()

