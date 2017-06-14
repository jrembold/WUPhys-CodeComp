#===================================================
#
# File Name: server.py
# 
# Purpose: To server as the server and game master 
#
# Creation Date: 13-06-2017
#
# Last Modified: Tue 13 Jun 2017 07:01:01 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import socket, select

CONNECTION_LIST = []
PORT = 10000

def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_sock and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)

def strToBytes( string ):
    return str.encode(string, 'UTF-8')

def bytesToStr( byte ):
    return str( byte, 'UTF-8')

class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.connection_list = []

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def receive(self, MSGLEN):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

    def bindAndListen(self, host, port):
        print('Starting server up on {} port {}'.format(host, port))
        self.sock.bind((host,port))
        self.sock.listen(1)
        self.connection_list.append(self.sock)

    def close(self):
        self.sock.close()


# Create the Socket
# server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock = MySocket()
server_sock.bindAndListen('localhost', 10000)



while True:
    # Wait for a connection
    read_sockets, write_sockets, error_sockets = select.select(server_sock.connection_list, [], [])

    for sock in read_sockets:
        # A New connection
        if sock == server_sock.sock:
            sockfd, addr = server_sock.sock.accept()
            server_sock.connection_list.append(sockfd)
            print('Client ({}, {}) connected'.format(addr[0], addr[1]))

        #Incoming client message
        else:
            msg = sock.recv(16)
            if msg:
                print('Message was: {}'.format(msg))
                sock.send


server_sock.close()
