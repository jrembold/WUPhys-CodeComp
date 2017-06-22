#===================================================
#
# File Name: RandomMap.py
# 
# Purpose: A bot moving in random directions
#
# Creation Date: 20-06-2017
#
# Last Modified: Thu 22 Jun 2017 02:42:40 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import library as lib
import random

bot = lib.CBot('Ia Rando')

while bot.active:
    bot.getMapState()

    if bot.active:
        move = random.choice(['forward', 'rotCW', 'rotCCW', 'forward'])
        bot.sendMessage( move )
