#===================================================
#
# File Name: Simpleman.py
# 
# Purpose: A simple bot for stabbing things
#
# Creation Date: 20-06-2017
#
# Last Modified: Fri 23 Jun 2017 03:04:13 PM PDT
#
# Created by: Jed Rembold
#
#===================================================
import sys
sys.path.append('./')
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
