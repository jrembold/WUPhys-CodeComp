#===================================================
#
# File Name: server.py
#
# Purpose: To server as the server and game master 
#
# Creation Date: 13-06-2017
#
# Last Modified: Sat 24 Jun 2017 07:49:50 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import socket, select, random, pickle, time, math, subprocess, sys, argparse
import numpy as np
import library as lib

np.set_printoptions(formatter={'float': ' {:4.1f} '.format})

CONNECTION_LIST = []
PLAYERID = 50
PORT = 10000
PLAYERS = {}
MAPSIZE = 10
NUMPLAYERS = 0
WINNER = ''
SPEARS = []

class Bot:
    def __init__(self, ucode, sock, name):
        self.name = name
        self.ID = int(ucode)
        self.sock = sock
        self.vision = []
        self.msgrecv = False
        self.spearcount = 2
        self.alive = True
        print('New contender checks in! Player #{}.'.format(self.ID))

    def place( self, Map ):
        '''Randomly place bot somewhere on map'''
        # self.x = random.randrange(1,MAPSIZE-2)
        # self.y = random.randrange(1,MAPSIZE-2)
        acceptable = False
        while not acceptable:
            self.x = random.randrange(0,MAPSIZE-1)
            self.y = random.randrange(0,MAPSIZE-1)
            self.direction = random.randrange(0,3)

            nbs = [Map[loc] for loc in self.getNeighbors(Map)]
            # Make sure no starting next to another bot or in a wall
            if not any(np.array(nbs)>10) and Map[self.y,self.x] == 0:
                acceptable = True

        Map[self.y,self.x] = self.ID + self.direction/10
        # print('Player {} placed'.format(self.ID))

    def getNeighbors( self, Map ):
        neighbors = []
        for i in [-1,1]:
            neighbors.append((self.y+i,self.x))
            neighbors.append((self.y,self.x+i))
        return neighbors


    def remove( self, Map ):
        '''Delete bot from map'''
        try:
            loc = tuple(np.argwhere(Map==self.ID+self.direction/10)[0])
            Map[loc] = 0
        # if it isn't on the map, something must have already overwritten it
        # no worries then, proceed
        except:
            pass

    def forward( self, Map ):
        ''' Move bot in direction it is facing if
        nothing is there '''
        if self.direction == 0:
            nextloc = (self.y-1, self.x)
        elif self.direction == 1:
            nextloc = (self.y, self.x+1)
        elif self.direction == 2:
            nextloc = (self.y+1, self.x)
        else:
            nextloc = (self.y, self.x-1)

        #Only move into empty spaces
        if Map[nextloc] == 0:
            Map[nextloc] = self.ID + self.direction/10
            Map[(self.y,self.x)] = 0
            (self.y,self.x) = nextloc

        #If moving onto moving spear, die!
        if math.floor(Map[nextloc]) == 2:
            self.alive = False
            Map[nextloc] = 3

        if Map[nextloc] == 3:
            self.spearcount += 1
            Map[nextloc] = self.ID + self.direction/10
            Map[(self.y,self.x)] = 0
            (self.y,self.x) = nextloc

        self.computeVision( Map )


    def rotCW( self, Map ):
        ''' Rotates bot clockwise'''
        self.direction = (self.direction+1) % 4
        Map[(self.y, self.x)] = self.ID + self.direction/10
        self.computeVision( Map )


    def rotCCW( self, Map ):
        ''' Rotates bot CCW '''
        self.direction = (self.direction-1) % 4
        Map[(self.y, self.x)] = self.ID + self.direction/10
        self.computeVision( Map )


    def computeVision( self, Map ):
        ''' Gets list of values straight ahead of
        bot until it encounters a wall. '''
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


    def checkStab( self, Map ):
        ''' Check if adjacent cell has another bot.
        If so, end it's life. '''
        if len(self.vision)>1:
            adj = self.vision[1]
            if adj > 10:
                ucode = str(math.floor(adj)).zfill(2)
                PLAYERS[ucode].alive = False

class Spear:
    def __init__(self, bot, Map):
        self.direction = bot.direction
        self.x = bot.x
        self.y = bot.y
        # bot.spearcount -= 1
        self.moving = True
        # self.getInitPosition(bot)
        # self.draw(Map)
        self.placeSpear(Map,bot)

    def getFacingLoc(self):
        d = self.direction
        if d == 0:
            return (self.y-1,self.x)
        if d == 1:
            return (self.y, self.x+1)
        if d == 2:
            return (self.y+1,self.x)
        return (self.y, self.x-1)

    def placeSpear(self, Map, bot):
        loc = self.getFacingLoc()
        if Map[loc] == 0:
            bot.spearcount -= 1
            (self.y, self.x) = loc
            Map[loc] = 2 + self.direction/10
        else:
            self.moving = False

    def checkKill( self, Map ):
        spearloc = Map(self.y,self.x)
        if spearloc > 10:
            ucode = str(math.floor(spearloc).zfill(2))
            PLAYERS[ucode].alive = False
            Map[self.y,self.x] = 3
            self.moving = False

    def move( self, Map ):
        nextloc = self.getFacingLoc()

        #Only move into empty spaces
        if Map[nextloc] == 0:
            Map[nextloc] = 2+self.direction/10
            Map[(self.y,self.x)] = 0
            (self.y,self.x) = nextloc

        #Hitting a wall, or any other spear
        elif Map[nextloc] == 1 or Map[nextloc] == 3 or math.floor(Map[nextloc]) == 2:
            self.moving = False
            Map[self.y,self.x] = 3

        #If moving onto bot, kill it!
        elif Map[nextloc] > 10:
            ucode = str(math.floor(Map[nextloc])).zfill(2)
            PLAYERS[ucode].alive = False
            Map[self.y,self.x] = 0
            Map[nextloc] = 3
            (self.y,self.x) = nextloc
            self.moving = False




def bindAndListen( sock, host, port ):
    '''Function to initialize listening on a
    server and particular port'''

    print('Starting server up on {} on port {}'.format(host,port))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host,port))
    sock.listen(1)
    CONNECTION_LIST.append(sock)

def playerChecksIn(sock, name, Map):
    global PLAYERID, PLAYERS

    PLAYERID += 1
    ucode = str(PLAYERID).zfill(2)
    PLAYERS[ucode] = Bot(ucode, sock, name)
    PLAYERS[ucode].place(Map)
    lib.sendReply(sock, lib.CMDS['checkin'], ucode.zfill(2))

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs = '*', help='List of python bots to compete')
    parser.add_argument('-s', '--size', default=10, help='Square size of arena')
    parser.add_argument('-d', '--delay', default=0, help='Time to delay between turns')
    botnames = parser.parse_args()

    NUMPLAYERS = len(botnames.input)
    MAPSIZE = int(botnames.size)
    DELAYTIME = float(botnames.delay)

    # Create the Socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Start listening
    bindAndListen( server_sock, 'localhost', 10000 )
    Map = createMap(MAPSIZE)
    print(Map)

    # ------------------------------------------
    # Receive initial bot check-ins
    # ------------------------------------------
    for i in botnames.input:
        subprocess.Popen([sys.executable, i])

    while len(PLAYERS)<NUMPLAYERS:
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
                    inc_msg = lib.receiveMessage( sock )
                    [msgtype, msg, needsreply] = lib.parseMessage(inc_msg)
                    # if buf != b'':
                        # print(buf)
                    if msgtype == lib.CMDS['checkin']:
                        playerChecksIn(sock, msg, Map)
                except:
                    print('A client most likely did not disconnect successfully.')
                    print('Closing and removing it')
                    sock.close()
                    CONNECTION_LIST.remove(sock)


    # ---------------------------------------
    # Now start the main loop
    # ---------------------------------------

    # Pause a moment to make sure all check-ins complete
    time.sleep(0.5)

    # As long as a player is alive
    while len(PLAYERS)>0:
        # Show current Map
        print(Map)

        # Delay
        time.sleep(DELAYTIME)

        # Reset all the message received flags to false
        # Update latest vision and check stabs
        for p in PLAYERS:
            PLAYERS[p].msgrecv = False
            PLAYERS[p].computeVision(Map)
            PLAYERS[p].checkStab(Map)

        for s in SPEARS:
            for i in range(2):
                if s.moving:
                    s.move(Map)
            if not s.moving:
                SPEARS.remove(s)


        if len(PLAYERS) == 1:
            for key in PLAYERS:
                WINNER = key
                WINNERNAME = PLAYERS[key].name
                # print('Player {} is victorious!'.format(key))

        # Send map data to all bots
        for p in PLAYERS:
            send_dict = {'vision':PLAYERS[p].vision,
                         'spears':PLAYERS[p].spearcount,
                         'alive': PLAYERS[p].alive,
                         'pcount':len(PLAYERS)
                         }
            lib.sendReply( PLAYERS[p].sock, lib.CMDS['mapstate'], pickle.dumps(send_dict))



        # -------------------------------------
        # Wait for and process bot responses
        # -------------------------------------
        while not all([PLAYERS[i].msgrecv for i in PLAYERS]):
            # Wait for a connection
            read_socks, write_s, err_s = select.select(CONNECTION_LIST, [], [])

            for sock in read_socks:
                # A New connection
                if sock == server_sock:
                    print('Unregistered contender tried to connect')

                #Incoming client message
                else:
                    try:
                        inc_msg = lib.receiveMessage( sock )
                        [msgtype, msg, needsreply] = lib.parseMessage(inc_msg)
                        # if buf != b'':
                            # print(buf)
                        if msgtype == lib.CMDS['leave']:
                            PLAYERS[msg].msgrecv = True
                            playerLeaves( sock, msg, Map )
                            # print('Player {} has left!'.format(msg))
                        if msgtype == lib.CMDS['forward']:
                            PLAYERS[msg].forward(Map)
                            PLAYERS[msg].computeVision(Map)
                            PLAYERS[msg].msgrecv = True
                        if msgtype == lib.CMDS['rotCW']:
                            PLAYERS[msg].rotCW(Map)
                            PLAYERS[msg].msgrecv = True
                        if msgtype == lib.CMDS['rotCCW']:
                            PLAYERS[msg].rotCCW(Map)
                            PLAYERS[msg].msgrecv = True
                        if msgtype == lib.CMDS['spear']:
                            if PLAYERS[msg].spearcount > 0:
                                SPEARS.append(Spear(PLAYERS[msg],Map))
                            PLAYERS[msg].msgrecv = True
                    # if no good message, a client must have disconnected unexpectedly
                    except:
                        print('A client most likely did not disconnect properly.')
                        print('Closing and removing it')
                        sock.close()
                        CONNECTION_LIST.remove(sock)

    # for sock in CONNECTION_LIST:
        # sock.close()
    server_sock.close()

    # Winner text!
    if WINNER != '':
        print('{} (#{}) was victorious!'.format(WINNERNAME, WINNER))
    else:
        print('There were no winners. Life is tough.')
