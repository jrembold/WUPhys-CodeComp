# ===================================================
#
# File Name: server.py
#
# Purpose: To server as the server and game master
#
# Creation Date: 13-06-2017
#
# Last Modified: Sat 26 Aug 2017 03:17:47 PM PDT
#
# Created by: Jed Rembold
#
# ===================================================

import socket
import select
import random
import pickle
import time
import math
import subprocess
import sys
import argparse
import numpy as np
import library as lib

np.set_printoptions(formatter={"float": " {:4.1f} ".format})

CONNECTION_LIST = []
PLAYERID = 50
PORT = 10000
PLAYERS = {}
MAPSIZE = 20
NUMPLAYERS = 0
WINNER = ""
BALLS = []
MAPSTATE = {}
ROUNDCAP = 2000
PLAYERORDER = {}
PRINTOUT = True


class Bot:
    def __init__(self, ucode, sock, name):
        self.name = name
        self.fname = ""
        self.ID = int(ucode)
        self.sock = sock
        self.vision = []
        self.msgrecv = False
        self.ballcount = 2
        self.alive = True
        self.timebomb = 0
        self.ping = {}
        self.pinging = False
        self.oldloc = (0, 0)
        if PRINTOUT:
            print("{} checks in! Player #{}.".format(self.name, self.ID))

    def place(self, Map):
        """Randomly place bot somewhere on map"""
        # self.x = random.randrange(1,MAPSIZE-2)
        # self.y = random.randrange(1,MAPSIZE-2)
        acceptable = False
        while not acceptable:
            self.x = random.randrange(0, MAPSIZE - 1)
            self.y = random.randrange(0, MAPSIZE - 1)
            self.direction = random.randrange(0, 3)

            nbs = [Map[loc] for loc in self.getNeighbors(Map)]
            # Make sure no starting next to another bot or in a wall
            if not any(np.array(nbs) > 10) and Map[self.y, self.x] == 0:
                acceptable = True

        Map[self.y, self.x] = self.ID + self.direction / 10
        self.oldloc = (self.y, self.x)
        # print('Player {} placed'.format(self.ID))

    def getNeighbors(self, Map):
        """Determine neighboring indices about a point"""
        ymax, xmax = Map.shape
        check_dist = 5
        neighbors = []
        for i in np.arange(-check_dist, check_dist, 1):
            for j in np.arange(-check_dist, check_dist, 1):
                if 0 < self.y + i < ymax and 0 < self.x + j < xmax:
                    neighbors.append((self.y + i, self.x + j))
        return neighbors

    def remove(self, Map):
        """Delete bot from map"""
        try:
            loc = tuple(np.argwhere(Map == self.ID + self.direction / 10)[0])
            Map[loc] = 0
        # if it isn't on the map, something must have already overwritten it
        # no worries then, proceed
        except:
            pass

    def forward(self, Map):
        """ Move bot in direction it is facing if
        nothing is there """
        self.oldloc = (self.y, self.x)
        if self.direction == 0:
            nextloc = (self.y - 1, self.x)
        elif self.direction == 1:
            nextloc = (self.y, self.x + 1)
        elif self.direction == 2:
            nextloc = (self.y + 1, self.x)
        else:
            nextloc = (self.y, self.x - 1)

        # Only move into empty spaces
        if Map[nextloc] == 0:
            Map[nextloc] = self.ID + self.direction / 10
            Map[(self.y, self.x)] = 0
            (self.y, self.x) = nextloc

        # If moving onto moving ball, die!
        if math.floor(Map[nextloc]) == 2:
            self.alive = False
            Map[nextloc] = 3

        if Map[nextloc] == 3:
            self.ballcount += 1
            Map[nextloc] = self.ID + self.direction / 10
            Map[(self.y, self.x)] = 0
            (self.y, self.x) = nextloc
            # Remove ball
            for s in BALLS:
                if (s.y, s.x) == nextloc:
                    BALLS.remove(s)

        self.computeVision(Map)

    def rotCW(self, Map):
        """ Rotates bot clockwise"""
        self.oldloc = (self.y, self.x)
        self.direction = (self.direction + 1) % 4
        Map[(self.y, self.x)] = self.ID + self.direction / 10
        self.computeVision(Map)

    def rotCCW(self, Map):
        """ Rotates bot CCW """
        self.oldloc = (self.y, self.x)
        self.direction = (self.direction - 1) % 4
        Map[(self.y, self.x)] = self.ID + self.direction / 10
        self.computeVision(Map)

    def computeVision(self, Map):
        """ Gets list of values straight ahead of
        bot until it encounters a wall. """
        self.vision = []
        targety = self.y
        targetx = self.x
        while Map[targety, targetx] != 1:
            self.vision.append(Map[targety, targetx])
            if self.direction == 0:
                targety -= 1
            elif self.direction == 1:
                targetx += 1
            elif self.direction == 2:
                targety += 1
            else:
                targetx -= 1

    def computePingVision(self, Map):
        pingrng = 8
        maxval = Map.shape[0]

        def circ_pts(center, radius):
            (x, y) = center
            pts = []
            for i in range(x - radius, x + radius):
                for j in range(y - radius, y + radius):
                    if (i - x) ** 2 + (j - y) ** 2 < radius ** 2:
                        pts.append((i, j))
            return pts

        pts = circ_pts((self.y, self.x), pingrng)
        fpts = list(
            filter(
                lambda x: x[0] > 0 and x[0] < maxval and x[1] > 0 and x[1] < maxval, pts
            )
        )

        pinginfo = {"Terrain": [], "ABall": [], "DBall": [], "Enemy": []}
        for p in fpts:
            p2 = tuple(map(sum, zip(p, (-self.y, -self.x))))
            if Map[p] == 1:
                pinginfo["Terrain"].append(p2)
            elif round(Map[p]) == 2:
                pinginfo["ABall"].append(p2)
            elif Map[p] == 3:
                pinginfo["DBall"].append(p2)
            elif Map[p] != 0 and Map[p] != Map[(self.y, self.x)]:
                pinginfo["Enemy"].append(p2)

        return pinginfo

    def handlePing(self, Map):
        self.oldloc = (self.y, self.x)
        info = self.computePingVision(Map)
        # lib.sendReply( self.sock, lib.CMDS['retping'], pickle.dump(info) )
        self.pinging = True
        self.ping = info

    def checkStab(self, Map):
        """ Check if adjacent cell has another bot.
        If so, end it's life. """
        if len(self.vision) > 1:
            adj = self.vision[1]
            if adj > 10:
                ucode = str(math.floor(adj)).zfill(2)
                PLAYERS[ucode].alive = False

    def checkIfMoved(self):
        """ Check to see if bot has moved this round.
        If not, increment time bomb"""
        if (self.y, self.x) == self.oldloc:
            self.timebomb += 1
            if self.timebomb > 120:
                self.alive = False
        else:
            self.timebomb = 0

    def dropballs(self, Map):
        """ Drop all dodgeballs in inventory if bot
        dies in an area around it """
        while self.ballcount > 0:
            Ball(self, Map, thrown=False)


class Ball:
    def __init__(self, bot, Map, thrown=True):
        self.direction = bot.direction
        self.x = bot.x
        self.y = bot.y
        # bot.ballcount -= 1
        self.moving = thrown
        # self.getInitPosition(bot)
        # self.draw(Map)
        if self.moving:
            self.placeBall(Map, bot)
        else:
            self.placeDeadBall(Map, bot)

    def getFacingLoc(self):
        d = self.direction
        if d == 0:
            return (self.y - 1, self.x)
        if d == 1:
            return (self.y, self.x + 1)
        if d == 2:
            return (self.y + 1, self.x)
        return (self.y, self.x - 1)

    def placeBall(self, Map, bot):
        loc = self.getFacingLoc()
        if Map[loc] == 0:
            bot.ballcount -= 1
            (self.y, self.x) = loc
            Map[loc] = 2 + self.direction / 10
            BALLS.append(self)
        else:
            self.moving = False

    def placeDeadBall(self, Map, bot):
        def gen_locs(self):
            locs = [
                (y + self.y, x + self.x)
                for y in np.arange(-4, 5)
                for x in np.arange(-4, 5)
                if 0 < y + self.y < Map.shape[0] and 0 < x + self.x < Map.shape[1]
            ]
            locs.sort(key=lambda p: (p[0] - self.y) ** 2 + (p[1] - self.x) ** 2)
            return locs

        pot_locs = gen_locs(self)
        for loc in pot_locs:
            if Map[loc] == 0:
                Map[loc] = 3
                (self.y, self.x) = loc
                BALLS.append(self)
                bot.ballcount -= 1
                return
        bot.ballcount -= 1

    def checkKill(self, Map):
        ballloc = Map(self.y, self.x)
        if ballloc > 10:
            ucode = str(math.floor(ballloc).zfill(2))
            PLAYERS[ucode].alive = False
            Map[self.y, self.x] = 3
            self.moving = False

    def move(self, Map):
        nextloc = self.getFacingLoc()

        # Only move into empty spaces
        if Map[nextloc] == 0:
            Map[nextloc] = 2 + self.direction / 10
            Map[(self.y, self.x)] = 0
            (self.y, self.x) = nextloc

        # Hitting a wall, or any other ball
        elif Map[nextloc] == 1 or Map[nextloc] == 3 or math.floor(Map[nextloc]) == 2:
            self.moving = False
            Map[self.y, self.x] = 3

        # If moving onto bot, kill it!
        elif Map[nextloc] > 10:
            ucode = str(math.floor(Map[nextloc])).zfill(2)
            PLAYERS[ucode].alive = False
            Map[self.y, self.x] = 0
            Map[nextloc] = 3
            (self.y, self.x) = nextloc
            self.moving = False


def bindAndListen(sock, host, port):
    """Function to initialize listening on a
    server and particular port"""

    if PRINTOUT:
        print("Starting server up on {} on port {}".format(host, port))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    CONNECTION_LIST.append(sock)


def playerChecksIn(sock, name, Map):
    global PLAYERID, PLAYERS

    PLAYERID += 1
    ucode = str(PLAYERID).zfill(2)
    PLAYERS[ucode] = Bot(ucode, sock, name)
    PLAYERS[ucode].place(Map)
    lib.sendReply(sock, lib.CMDS["checkin"], ucode.zfill(2))


def playerLeaves(sock, ucode, Map, ROUND):
    global CONNECTION_LIST, PLAYERS
    sock.close()
    try:
        CONNECTION_LIST.remove(sock)
    except ValueError:
        pass
    PLAYERORDER[PLAYERS[ucode].name] = ROUND

    # Find and remove player on map
    PLAYERS[ucode].remove(Map)
    PLAYERS[ucode].dropballs(Map)
    del PLAYERS[ucode]


def createMap(size, obstacles):
    Map = np.ones((size, size))
    Map[1 : size - 1, 1 : size - 1] = np.zeros((size - 2, size - 2))
    obs = random.randint(0, int(obstacles))
    for o in range(obs):
        x = random.randint(1, size - 1)
        y = random.randint(1, size - 1)
        Map[y, x] = 1
    return Map


def shrinkMap(Map, turn_counter):

    limit = turn_counter ** 2
    if random.randint(0, 250000) < limit:
        # Then shrink in the map
        mlen = Map.shape[0]
        starting_point = random.randint(0, mlen - 1)
        side = np.random.choice(["N", "S", "E", "W"])
        placed = False

        # What follows is ugly as hell, but I couldn't
        # figure out how to compact it nicely given
        # the need for the different rows and columns
        if side == "N":
            start = 0
            direct = 1
            while not placed:
                check = Map[start, starting_point]
                if not check:
                    Map[start, starting_point] = 1
                    placed = True
                elif check > 1:
                    break
                if start < mlen - 1:
                    start += direct
                else:
                    break
        elif side == "S":
            start = mlen - 1
            direct = -1
            while not placed:
                check = Map[start, starting_point]
                if not check:
                    Map[start, starting_point] = 1
                    placed = True
                elif check > 1:
                    break
                if start > 0:
                    start += direct
                else:
                    break
        elif side == "W":
            start = 0
            direct = 1
            while not placed:
                check = Map[starting_point, start]
                if not check:
                    Map[starting_point, start] = 1
                    placed = True
                elif check > 1:
                    break
                if start < mlen - 1:
                    start += direct
                else:
                    break
        else:
            start = mlen - 1
            direct = -1
            while not placed:
                check = Map[starting_point, start]
                if not check:
                    Map[starting_point, start] = 1
                    placed = True
                elif check > 1:
                    break
                if start > 0:
                    start += direct
                else:
                    break

    return Map


def genMapState(PLAYERS, BALLS, Map):
    players = {}
    for p in PLAYERS:
        players[PLAYERS[p].ID] = {
            "x": PLAYERS[p].x,
            "y": PLAYERS[p].y,
            "face": PLAYERS[p].direction,
            "balls": PLAYERS[p].ballcount,
            "name": PLAYERS[p].name,
            "pinging": PLAYERS[p].pinging,
        }
    balls = []
    for s in BALLS:
        balls.append([s.x, s.y, s.direction, s.moving])
    M2 = Map.copy()
    M2[M2 > 1] = 0
    return {"players": players, "balls": balls, "map": M2}


def main(
    inputs,
    size,
    obstacles,
    viewer,
    delay,
    replaysave=True,
    noprint=False,
    replaysample=False,
):
    global CONNECTION_LIST, PLAYERS, PLAYERID, PORT, MAPSIZE, PRINTOUT
    global NUMPLAYERS, WINNER, BALLS, MAPSTATE, ROUNDCAP, PLAYERORDER

    if noprint:
        PRINTOUT = False

    MAPSTATE = {}
    BALLS = []
    CONNECTION_LIST = []
    PLAYERORDER = {}
    PLAYERID = 50
    WINNER = ""

    MAPSIZE = int(size)
    NUMPLAYERS = len(inputs)

    # Create the Socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Start listening
    bindAndListen(server_sock, "localhost", 10000)
    Map = createMap(MAPSIZE, obstacles)
    MAPSTATE["Map"] = Map.copy()
    # Pause a moment to make sure server up and running before starting bots
    time.sleep(0.5)

    # ------------------------------------------
    # Receive initial bot check-ins
    # ------------------------------------------
    for i in inputs:
        subprocess.Popen([sys.executable, "Bots/" + i])

    while len(PLAYERS) < NUMPLAYERS:
        read_socks, write_socks, error_socks = select.select(CONNECTION_LIST, [], [])

        for sock in read_socks:
            # A New connection
            if sock == server_sock:
                sockfd, addr = server_sock.accept()
                CONNECTION_LIST.append(sockfd)

            # Incoming client message
            else:
                try:
                    inc_msg = lib.receiveMessage(sock)
                    [msgtype, msg, needsreply] = lib.parseMessage(inc_msg)
                    if msgtype == lib.CMDS["checkin"]:
                        playerChecksIn(sock, msg, Map)
                except:
                    print(
                        "A client most likely did\
                            not disconnect successfully."
                    )
                    print("Closing and removing it.")
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    NUMPLAYERS -= 1
                    print(
                        "Currently have {}/{} players".format(len(PLAYERS), NUMPLAYERS)
                    )

    # ---------------------------------------
    # Now start the main loop
    # ---------------------------------------

    # Pause a moment to make sure all check-ins complete
    # time.sleep(0.5)

    # Round counter
    ROUND = 0

    # As long as a player is alive
    while len(PLAYERS) > 0:
        Map = shrinkMap(Map, ROUND)
        MAPSTATE[ROUND] = genMapState(PLAYERS, BALLS, Map)
        ROUND += 1

        # Check roundcap:
        if ROUND >= ROUNDCAP:
            for p in PLAYERS:
                PLAYERS[p].alive = False

        # Reset all the message received flags to false
        # Update latest vision and check stabs
        for p in PLAYERS:
            PLAYERS[p].msgrecv = False
            PLAYERS[p].computeVision(Map)
            PLAYERS[p].checkStab(Map)
            PLAYERS[p].checkIfMoved()

        for s in BALLS:
            for i in range(2):
                if s.moving:
                    s.move(Map)

        if len(PLAYERS) == 1:
            for key in PLAYERS:
                WINNER = key
                WINNERNAME = PLAYERS[key].name

        # Send map data to all bots
        for p in PLAYERS:
            send_dict = {
                "vision": PLAYERS[p].vision,
                "balls": PLAYERS[p].ballcount,
                "alive": PLAYERS[p].alive,
                "pcount": len(PLAYERS),
                "lastping": PLAYERS[p].ping,
            }
            lib.sendReply(
                PLAYERS[p].sock, lib.CMDS["mapstate"], pickle.dumps(send_dict)
            )
            PLAYERS[p].pinging = False

        # -------------------------------------
        # Wait for and process bot responses
        # -------------------------------------
        while not all([PLAYERS[i].msgrecv for i in PLAYERS]):
            # Wait for a connection
            read_socks, write_s, err_s = select.select(CONNECTION_LIST, [], [])

            for sock in read_socks:
                # A New connection
                if sock == server_sock:
                    print("Unregistered contender tried to connect")

                # Incoming client message
                else:
                    try:
                        inc_msg = lib.receiveMessage(sock)
                        [msgtype, msg, needsreply] = lib.parseMessage(inc_msg)
                        if msgtype == lib.CMDS["leave"]:
                            PLAYERS[msg].msgrecv = True
                            playerLeaves(sock, msg, Map, ROUND)
                        if msgtype == lib.CMDS["forward"]:
                            PLAYERS[msg].forward(Map)
                            PLAYERS[msg].computeVision(Map)
                            PLAYERS[msg].msgrecv = True
                        if msgtype == lib.CMDS["rotCW"]:
                            PLAYERS[msg].rotCW(Map)
                            PLAYERS[msg].msgrecv = True
                        if msgtype == lib.CMDS["rotCCW"]:
                            PLAYERS[msg].rotCCW(Map)
                            PLAYERS[msg].msgrecv = True
                        if msgtype == lib.CMDS["ball"]:
                            if PLAYERS[msg].ballcount > 0:
                                Ball(PLAYERS[msg], Map)
                            PLAYERS[msg].msgrecv = True
                        if msgtype == lib.CMDS["ping"]:
                            PLAYERS[msg].handlePing(Map)
                            PLAYERS[msg].msgrecv = True
                    # if no good message, a client must have
                    # disconnected unexpectedly
                    except:
                        # print('A client most likely did not
                        # disconnect properly.')
                        # print('Closing and removing it.')
                        for p in PLAYERS:
                            if PLAYERS[p].sock == sock:
                                ucode = str(PLAYERS[p].ID)
                        print("{} crashed and loses.".format(PLAYERS[ucode].name))
                        playerLeaves(sock, ucode, Map, ROUND)

    server_sock.close()

    # Winner text!
    if WINNER != "":
        if PRINTOUT:
            print(
                "{} (#{}) was victorious in {} rounds!".format(
                    WINNERNAME, WINNER, ROUND - 1
                )
            )
    else:
        if PRINTOUT:
            print("There were no winners. Life is tough.")
        WINNERNAME = None

    # Save MAPSTATE
    if replaysave:
        with open("lastgame.pickle", "wb") as f:
            pickle.dump(MAPSTATE, f)

    # Save sample replays
    if replaysample:
        if WINNERNAME:
            victor = WINNERNAME[:-3]
        else:
            victor = "Tie"
        rep_name = "Replays/{}_{}.pickle".format(victor, random.randint(1, 10))
        with open(rep_name, "wb") as f:
            pickle.dump(MAPSTATE, f)

    if viewer.lower() == 'mpl':
        subprocess.Popen([sys.executable, "viewer.py", "-d", str(delay)])
    elif viewer.lower() == 'tk':
        subprocess.Popen([sys.executable, "viewer_tkinter.py"])

    return PLAYERORDER


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", nargs="*", help="List of python bots to compete"
    )
    parser.add_argument("-s", "--size", default=MAPSIZE, help="Square size of arena")
    parser.add_argument(
        "-d", "--delay", default=1, help="Speed multiplier for viewer playback"
    )
    parser.add_argument("-o", "--obs", default=10, help="Maximum number of obstacles")
    parser.add_argument(
        "-v",
        "--view",
        default='MPL',
        help="Viewer to show after match completion. None to suppress."
    )
    parser.add_argument(
        "--noprint",
        default=False,
        action="store_true",
        help="Suppress all printed output to screen",
    )
    botnames = parser.parse_args()

    main(
        botnames.input,
        botnames.size,
        botnames.obs,
        botnames.view,
        botnames.delay,
        noprint=botnames.noprint,
    )
