from network_programming.socket import *
import socket
from socket import AF_INET, SOCK_STREAM

def socket_bind():
    HOST = '0.0.0.0'
    PORT = 5000
    BUFSIZE = 1024
    ADDR = (HOST, PORT)

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(ADDR)
    serverSocket.listen(10)
    conn, addr = serverSocket.accept()
    print "connect client {0}".format(addr)
    while True:
        data = conn.recv(BUFSIZE)
        #data = serverSocket.recvfrom(BUFSIZE)
        print data
    conn.close()

if __name__ == "__main__":
    socket_bind()
