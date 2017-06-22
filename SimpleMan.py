#===================================================
#
# File Name: client2.py
# 
# Purpose: A client using the class definition 
#
# Creation Date: 20-06-2017
#
# Last Modified: Thu 22 Jun 2017 03:03:08 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import library as lib

def calcMove( bot ):
    #If anything non-zero in front to me, go forwards!
    if any(bot.vision[1:]):
        return 'forward'
    #Otherwise, turn clockwise
    else:
        return 'rotCW'



bot = lib.CBot('Simple Simon')

while bot.active:
    bot.getMapState()

    if bot.active:
        move = calcMove(bot)
        bot.sendMessage( move )
