#===================================================
#
# File Name: server.py
# 
# Purpose: To server as the server and game master 
#
# Creation Date: 13-06-2017
#
# Last Modified: Tue 20 Jun 2017 02:29:56 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import socket, select, random, pickle, time
import numpy as np
import socket_cmds as scmds

CONNECTION_LIST = []
PLAYERID = 50
PORT = 10000
PLAYERS = {}
MAPSIZE = 10
NUMPLAYERS = 3

class Bot:
    def __init__(self, ucode, sock):
        self.ID = int(ucode)
        self.sock = sock
        self.vision = []
        self.msgrecv = False
        print('New contender checks in! Player #{}.'.format(self.ID))

    def place( self, Map ):
        self.x = random.randrange(1,MAPSIZE-2)
        self.y = random.randrange(1,MAPSIZE-2)
        self.direction = random.randrange(0,3)
        while Map[self.y,self.x] != 0:
            self.x = random.randrange(1,MAPSIZE-2)
            self.y = random.randrange(1,MAPSIZE-2)
        Map[self.y,self.x] = self.ID + self.direction/10
        print('Player {} placed'.format(self.ID))

    def remove( self, Map ):
        loc = tuple(np.argwhere(Map==self.ID+self.direction/10)[0])
        Map[loc] = 0

    def forward( self, Map ):
        # print(self.direction)
        if self.direction == 0:
            nextloc = (self.y-1, self.x)
        elif self.direction == 1:
            nextloc = (self.y, self.x+1)
        elif self.direction == 2:
            nextloc = (self.y+1, self.x)
        else:
            nextloc = (self.y, self.x-1)

        if Map[nextloc] == 0:
            Map[nextloc] = self.ID + self.direction/10
            Map[(self.y,self.x)] = 0
            (self.y,self.x) = nextloc

    def rotCW( self, Map ):
        self.direction = (self.direction+1) % 4
        Map[(self.y, self.x)] = self.ID + self.direction/10
        # print(self.direction)

    def rotCCW( self, Map ):
        self.direction = (self.direction-1) % 4
        Map[(self.y, self.x)] = self.ID + self.direction/10
        # print(self.direction)

    def computeVision( self, Map ):
        self.vision = []
        targety = self.y
        targetx = self.x
        while Map[targety, targetx] != 1:
            self.vision.append(Map[targety,targetx])
            if self.direction == 0:
                targety -= 1
            elif self.direction == 1:
                targetx += 1
            elif self.direction == 2:
                targety += 1
            else:
                targetx -= 1
        


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
    PLAYERS[ucode] = Bot(ucode, sock)
    PLAYERS[ucode].place(Map)
    scmds.sendReply(sock, scmds.CMDS['checkin'], ucode.zfill(2))


def playerLeaves( sock, ucode, Map ):
    global CONNECTION_LIST, PLAYERS
    sock.close()
    CONNECTION_LIST.remove(sock)

    #Find and remove player on map
    PLAYERS[ucode].remove(Map)
    del PLAYERS[ucode]

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


    # Get initial bots
    while len(PLAYERS)<NUMPLAYERS:
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
                    inc_msg = scmds.receiveMessage( sock )
                    [msgtype, msg, needsreply] = scmds.parseMessage(inc_msg)
                    # if buf != b'':
                        # print(buf)
                    if msgtype == scmds.CMDS['checkin']:
                        playerChecksIn(sock, Map)
                        print(Map)
                except:
                    print('A client most likely did not disconnect successfully.')
                    print('Closing and removing it')
                    sock.close()
                    CONNECTION_LIST.remove(sock)

    # While we still have players alive
    time.sleep(1)
    while len(PLAYERS)>0:
        # Show current Map
        print(Map)

        # Reset all the message flags to false
        for p in PLAYERS:
            PLAYERS[p].msgrecv = False

        # Send vision data
        for p in PLAYERS:
            PLAYERS[p].computeVision(Map)
            scmds.sendReply( PLAYERS[p].sock, 'ba', pickle.dumps({'vision':PLAYERS[p].vision}))

        # Get bot responses
        while not all([PLAYERS[i].msgrecv for i in PLAYERS]):
            # Wait for a connection
            read_socks, write_socks, error_socks = select.select(CONNECTION_LIST, [], [])

            for sock in read_socks:
                # A New connection
                if sock == server_sock:
                    print('Unregistered contender tried to connect')

                #Incoming client message
                else:
                    try:
                        inc_msg = scmds.receiveMessage( sock )
                        [msgtype, msg, needsreply] = scmds.parseMessage(inc_msg)
                        # if buf != b'':
                            # print(buf)
                        if msgtype == scmds.CMDS['leave']:
                            PLAYERS[msg].msgrecv = True
                            playerLeaves( sock, msg, Map )
                            print('Player {} has left!'.format(msg[2:]))
                        if msgtype == scmds.CMDS['forward']:
                            PLAYERS[msg].forward(Map)
                            PLAYERS[msg].computeVision(Map)
                            PLAYERS[msg].msgrecv = True
                        if msgtype == scmds.CMDS['rotCW']:
                            PLAYERS[msg].rotCW(Map)
                            PLAYERS[msg].msgrecv = True
                        if msgtype == scmds.CMDS['rotCCW']:
                            PLAYERS[msg].rotCCW(Map)
                            PLAYERS[msg].msgrecv = True
                    # if no good message, a client must have disconnected and returned b''
                    except:
                        print('A client most likely did not disconnect successfully.')
                        print('Closing and removing it')
                        sock.close()
                        CONNECTION_LIST.remove(sock)

    for sock in CONNECTION_LIST:
        sock.close()
    server_sock.close()
