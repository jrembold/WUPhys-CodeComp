#===================================================
#
# File Name: SimpleAmazon.py
# 
# Purpose: A simple bot for stabbing and throwing spears!
#
# Creation Date: 20-06-2017
#
# Last Modified: Mon 26 Jun 2017 12:34:15 AM PDT
#
# Created by: Jed Rembold
#
#===================================================

import library as lib
import numpy as np
from math import floor


def calcMove( bot ):
    global tcount
    v = np.array(bot.vision[1:])
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

while bot.active:
    bot.getMapState()

    if bot.active:
        move = calcMove(bot)
        bot.sendMessage( move )
