#===================================================
#
# File Name: SimpleAmazon.py
# 
# Purpose: A simple bot for stabbing and throwing spears!
#
# Creation Date: 20-06-2017
#
# Last Modified: Fri 23 Jun 2017 03:13:28 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import library as lib
import numpy as np
import random as rnd

def calcMove( bot ):
    v = np.array(bot.vision[1:])
    #If anything non-zero in front to me and I have spears, throw one!
    if any(v>10) and bot.spearcount>0:
        return 'spear'
    elif any(v==3):
        return 'forward'
    #Otherwise, turn clockwise
    else:
        return rnd.choice(['rotCW', 'forward'])



bot = lib.CBot('Amy the Amazon')

while bot.active:
    bot.getMapState()

    if bot.active:
        move = calcMove(bot)
        bot.sendMessage( move )
