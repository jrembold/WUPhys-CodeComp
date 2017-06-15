#===================================================
#
# File Name: server.py
# 
# Purpose: To server as the server and game master 
#
# Creation Date: 13-06-2017
#
# Last Modified: Thu 15 Jun 2017 04:57:13 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import socket, select, random
import numpy as np
import socket_cmds as scmds

CONNECTION_LIST = []
PLAYERID = 50
PORT = 10000
PLAYERS = []
MAPSIZE = 10

def bindAndListen( sock, host, port ):
    '''Function to initialize listening on a
    server and particular port'''

    print('Starting server up on {} on port {}'.format(host,port))
    sock.bind((host,port))
    sock.listen(1)
    CONNECTION_LIST.append(sock)

def playerChecksIn(sock, Map):
    global PLAYERID, PLAYERS

    def placePlayer( ID, Map ):
        x = random.randrange(1,MAPSIZE-2)
        y = random.randrange(1,MAPSIZE-2)
        while Map[x,y] != 0:
            x = random.randrange(1,MAPSIZE-2)
            y = random.randrange(1,MAPSIZE-2)
        Map[x,y] = ID

    PLAYERID += 1
    PLAYERS.append(PLAYERID)
    ucode = str(PLAYERID).zfill(2)
    print('New contender checks in! Given code {}.'.format(ucode))
    scmds.sendReply(sock, ucode.zfill(4))
    placePlayer(PLAYERID, Map)

def playerLeaves( sock, ucode, Map ):
    global CONNECTION_LIST, PLAYERS
    sock.close()
    CONNECTION_LIST.remove(sock)
    PLAYERS.remove(int(ucode))

    #Find and remove player on map
    idx = tuple(np.argwhere(Map==int(ucode))[0])
    Map[idx] = 0
    print(Map)

def createMap( size ):
    Map = np.ones((size,size))
    Map[1:size-1, 1:size-1] = np.zeros((size-2,size-2))
    return Map



if __name__ == '__main__':

    # Create the Socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Start listening
    bindAndListen( server_sock, 'localhost', 10000 )
    Map = createMap(MAPSIZE)
    print(Map)

    while True:
        # Wait for a connection
        read_socks, write_socks, error_socks = select.select(CONNECTION_LIST, [], [])

        for sock in read_socks:
            # A New connection
            if sock == server_sock:
                sockfd, addr = server_sock.accept()
                CONNECTION_LIST.append(sockfd)
                print('Client ({}, {}) connected'.format(addr[0], addr[1]))

            #Incoming client message
            else:
                try:
                    buf, reply, msg = scmds.receiveMessage( sock )
                    # if buf != b'':
                        # print(buf)
                    if msg == 'aaaa':
                        playerChecksIn(sock, Map)
                        print(Map)
                    if msg[:2] == 'ab':
                        print('Player {} has left!'.format(msg[2:]))
                        playerLeaves( sock, msg[2:], Map )
                # if no good message, a client must have disconnected and returned b''
                except:
                    print('A client most likely did not disconnect successfully')


    server_sock.close()
