#===================================================
#
# File Name: DumbPinger.py
# 
# Purpose: A simple bot to show pinging functionality
#
# Creation Date: 20-06-2017
#
# Last Modified: Tue 18 Jul 2017 07:08:40 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import library as lib
import numpy as np
import logging
from math import floor

# Logging Config!
logging.basicConfig(
        # Filename to log to
        filename = 'DumbPinger.log',
        # Logging supports multiple levels and will show everything above
        # this level. Debug is the bottom, so it will show everything
        level = logging.DEBUG,
        # Style for defining the format
        style = '{',
        # What will be saved in the log file
        format = '[{levelname}] [Line: {lineno}] {message}',
        # Rewrite the log file each run
        filemode = 'w',
        )

def getObjDir( obj ):
    d = round(obj % 1, 1)
    if d == 0.0: return 'North'
    if d == 0.1: return 'East'
    if d == 0.2: return 'South'
    if d == 0.3: return 'West'
    return None

def opposite( direction ):
    if direction=='North': return 'South'
    if direction=='South': return 'North'
    if direction=='East': return 'West'
    if direction=='West': return 'East'

def calcMove( bot):
    global tcount
    #v = np.array(bot.vision[1:])

    #Get facing direction
    #botdir = getObjDir(bot.vision[0])

    return 'ping'

    # #Do I see a bot?
    # if any(v>10):
        # #Empty space in front?
        # if v[0] == 0:
            # #Have spear onhand?
            # if bot.spearcount>0:
                # #Already spear enroute?
                # if any([opposite(getObjDir(i))==botdir for i in v if floor(i)==2]):
                    # return 'spear'
                # elif any([floor(i)==2 for i in v]):
                    # return 'rotCW'
                # else:
                    # return 'spear'
    # if any(v==3) and not any(v>10):
        # tcount = 0
        # return 'forward'
    # #if stationary too long, move
    # if tcount > 3 and len(v)>0:
        # tcount = 0
        # return 'forward'
    # else:
        # #Otherwise, turn clockwise
        # tcount += 1
        # return 'rotCW'



bot = lib.CBot('Anita Pinger')
tcount = 0
roundnum = 0

while bot.active:
    bot.getMapState()
    logging.debug(bot.msg)
    logging.info('[Round: {:^2}]: I see: {}'.format(roundnum, bot.vision))

    if bot.active:
        move = calcMove(bot)
        logging.info('[Round: {:^2}]: Sent move: {}'.format(roundnum,move))
        bot.sendMessage( move )

    roundnum += 1
