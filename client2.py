#===================================================
#
# File Name: client2.py
# 
# Purpose: A client using the class definition 
#
# Creation Date: 20-06-2017
#
# Last Modified: Tue 20 Jun 2017 05:57:15 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import library as lib
import time, random

bot = lib.CBot()

while bot.active:
    bot.getMapState()

    if bot.active:
        move = random.choice(['forward', 'rotCW', 'rotCCW', 'forward'])
        bot.sendMessage( move )
        time.sleep(0.15)

        print('I see {}'.format(bot.vision))
