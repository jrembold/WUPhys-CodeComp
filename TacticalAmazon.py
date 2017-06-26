#===================================================
#
# File Name: SimpleAmazon.py
# 
# Purpose: A simple bot for stabbing and throwing spears!
#
# Creation Date: 20-06-2017
#
# Last Modified: Mon 26 Jun 2017 03:23:01 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import library as lib
import numpy as np
import logging
from math import floor

logging.basicConfig(
        filename = 'TacticalAmazon.log',
        level = logging.DEBUG,
        style = '{',
        format = '[{levelname}] [Line: {lineno}] {message}',
        filemode = 'w',
        )

def getObjDir( obj ):
    d = round(obj % 1, 1)
    if d == 0.0: return 'North'
    if d == 0.1: return 'East'
    if d == 0.2: return 'South'
    if d == 0.3: return 'West'
    return None

def calcMove( bot ):
    global tcount
    v = np.array(bot.vision[1:])

    #Get facing direction
    botdir = getObjDir(bot.vision[0])

    #If anything non-zero in front to me and I have spears, throw one!
    if any(v>10) and bot.spearcount>0 and not any([floor(i)==2 for i in v]):
        return 'spear'
    elif any(v==3):
        tcount = 0
        return 'forward'
    #if stationary too long, move
    elif tcount > 3 and len(v)>0:
        tcount = 0
        return 'forward'
    #Otherwise, turn clockwise
    else:
        tcount += 1
        return 'rotCW'



bot = lib.CBot('Ariel the Amazon')
tcount = 0
roundnum = 0

while bot.active:
    bot.getMapState()
    logging.info('[Round: {:^2}]: I see: {}'.format(roundnum, bot.vision))

    if bot.active:
        move = calcMove(bot)
        logging.info('[Round: {:^2}]: Sent move: {}'.format(roundnum,move))
        bot.sendMessage( move )

    roundnum += 1
