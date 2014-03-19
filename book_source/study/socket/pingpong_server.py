#!/usr/bin/env python
import socket
import time

def ping(csock_fd):
    csock_fd.write("0\n")
    csock_fd.flush()

    while True:
        try:
            line = csock_fd.readline()
        except:
            break

        try:
            count = int(line.strip("\r\n"))
            print "recv : %d" % count
        except:
            count = 0
        time.sleep(1)

        try:
            csock_fd.write("%d\n" % (count+1))
            print "send : %d" % (count+1)
            csock_fd.flush()
        except:
            break    

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 9090))
    sock.listen(5)

    while True:
        (client, addr) = sock.accept()
        csock_fd = client.makefile()
        ping(csock_fd)

if __name__== '__main__':
    main()
