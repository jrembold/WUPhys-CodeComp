#===================================================
#
# File Name: server.py
# 
# Purpose: To server as the server and game master 
#
# Creation Date: 13-06-2017
#
# Last Modified: Thu 15 Jun 2017 05:39:28 PM PDT
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
PLAYERS = {}
MAPSIZE = 10

class Bot:
    def __init__(self, ucode):
        self.ID = int(ucode)
        print('New contender checks in! Player #{}.'.format(self.ID))

    def place( self, Map ):
        self.x = random.randrange(1,MAPSIZE-2)
        self.y = random.randrange(1,MAPSIZE-2)
        while Map[x,y] != 0:
            self.x = random.randrange(1,MAPSIZE-2)
            self.y = random.randrange(1,MAPSIZE-2)
        Map[self.x,self.y] = self.ID
        self.direction = random.randrange(1,4)

    def remove( self, Map ):
        loc = tuple(np.argwhere(Map==self.ID)[0])
        Map[loc] = 0

    def forward( self, Map ):
        if self.direction == 1:
            nextloc = (self.x, self.y-1)
        elif self.direction == 2:
            nextloc = (self.x+1, self.y)
        elif self.direction == 3:
            nextloc = (self.x, self.y+1)
        elif self.direction == 4:
            nextloc = (self.x-1, self.y)

        if Map[nextloc] == 0:
            Map[nextloc] = self.ID
            Map[(self.x,self.y)] = 0
            (self.x,self.y) = nextloc


def bindAndListen( sock, host, port ):
    '''Function to initialize listening on a
    server and particular port'''

    print('Starting server up on {} on port {}'.format(host,port))
    sock.bind((host,port))
    sock.listen(1)
    CONNECTION_LIST.append(sock)

def playerChecksIn(sock, Map):
    global PLAYERID, PLAYERS

    PLAYERID += 1
    ucode = str(PLAYERID).zfill(2)
    PLAYERS[ucode] = Bot(ucode)
    PLAYERS[ucode].place(Map)
    print(Map)
    scmds.sendReply(sock, ucode.zfill(4))


def playerLeaves( sock, ucode, Map ):
    global CONNECTION_LIST, PLAYERS
    sock.close()
    CONNECTION_LIST.remove(sock)

    #Find and remove player on map
    PLAYERS[ucode].remove(Map)
    del PLAYERS[ucode]
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
