#===================================================
#
# File Name: server.py
# 
# Purpose: To server as the server and game master 
#
# Creation Date: 13-06-2017
#
# Last Modified: Wed 14 Jun 2017 06:12:03 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import socket, select, random
import socket_cmds as scmds

CONNECTION_LIST = []
PLAYERCOUNT = 0
PORT = 10000
PLAYERS = []

def bindAndListen( sock, host, port ):
    '''Function to initialize listening on a
    server and particular port'''

    print('Starting server up on {} on port {}'.format(host,port))
    sock.bind((host,port))
    sock.listen(1)
    CONNECTION_LIST.append(sock)

if __name__ == '__main__':

    # Create the Socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Start listening
    bindAndListen( server_sock, 'localhost', 10000 )

    while True:
        # Wait for a connection
        read_socks, write_socks, error_socks = select.select(CONNECTION_LIST, [], [])

        for sock in read_socks:
            # A New connection
            if sock == server_sock:
                sockfd, addr = server_sock.accept()
                CONNECTION_LIST.append(sockfd)
                # print('Client ({}, {}) connected'.format(addr[0], addr[1]))

            #Incoming client message
            else:
                try:
                    buf, reply, msg = scmds.receiveMessage( sock )
                    # if buf != b'':
                        # print(buf)
                    if msg == 'aaaa':
                        PLAYERCOUNT +=1
                        PLAYERS.append(PLAYERCOUNT)
                        ucode = str(PLAYERCOUNT).zfill(2)
                        print('New contender checks in! Given code {}.'.format(ucode))
                        scmds.sendReply(sock, ucode.zfill(4))
                # if no good message, a client must have disconnected and returned b''
                except:
                    sock.close()
                    CONNECTION_LIST.remove(sock)


    server_sock.close()
