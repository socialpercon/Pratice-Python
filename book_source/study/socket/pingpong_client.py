#!/usr/bin/env python
import socket
import time

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost',9090))
    csock_fd = sock.makefile()
    while True:
        try:
            line = csock_fd.readline() 
            count = int(line.strip("\r\n"))
            print "recv : %d" % count
            
            time.sleep(1)
            csock_fd.write("%d\n" % (count+1))
            print "send : %d" % (count+1)
            csock_fd.flush()
        except IOError:
            print "error"

if __name__ == "__main__":
    main()
