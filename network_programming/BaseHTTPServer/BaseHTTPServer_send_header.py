#!/usr/bin/env python
#
# Copyright 2007 Doug Hellmann.
#
"""Simple GET handler with BaseHTTPServer
"""

#end_pymotw_header

import time
import urlparse
from network_programming.BaseHTTPServer import BaseHTTPRequestHandler


class GetHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Last-Modified',
                         self.date_time_string(time.time()))
        self.end_headers()
        self.wfile.write('Response body\n')
        return

if __name__ == '__main__':
    from network_programming.BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', 8080), GetHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()

