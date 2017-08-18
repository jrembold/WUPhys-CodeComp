#===================================================
#
# File Name: SimpleAmazon.py
# 
# Purpose: A simple bot for stabbing and throwing spears!
#
# Creation Date: 20-06-2017
#
# Last Modified: Fri 23 Jun 2017 05:27:51 PM PDT
#
# Created by: Jed Rembold
#
#===================================================
import sys
sys.path.append('./')
import library as lib
import numpy as np

def calcMove( bot ):
    global tcount
    v = np.array(bot.vision[1:])
    #If anything non-zero in front to me and I have spears, throw one!
    if any(v>10) and bot.spearcount>0:
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



bot = lib.CBot('Amy the Amazon')
tcount = 0

while bot.active:
    bot.getMapState()

    if bot.active:
        move = calcMove(bot)
        bot.sendMessage( move )
