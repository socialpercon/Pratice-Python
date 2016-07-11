#!/usr/bin/env python
# encoding: utf-8
from network_programming import socket

if __name__ == '__main__':
    try:
        import ssl
    except ImportError:
        pass
    host = 'localhost'
    port = 7474
    context = ssl.create_default_context()
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations("mycertfile")
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)
    conn.connect((host, port))
    conn.sendall("ping")
    print conn.recv(1024)
