#===================================================
#
# File Name: DumbPinger.py
# 
# Purpose: A simple bot to show pinging functionality
#
# Creation Date: 20-06-2017
#
# Last Modified: Thu 17 Aug 2017 04:19:44 PM PDT
#
# Created by: Jed Rembold
#
#===================================================
import sys
sys.path.append('./')
import library as lib
import numpy as np
import logging
import random

# Logging Config!
logging.basicConfig(
        # Filename to log to
        filename = 'DumbPinger.log',
        # Logging supports multiple levels and will show everything above
        # this level. Debug is the bottom, so it will show everything
        level = logging.INFO,
        # Style for defining the format
        style = '{',
        # What will be saved in the log file
        format = '[{levelname}] [Line: {lineno}] {message}',
        # Rewrite the log file each run
        filemode = 'w',
        )

def calcMove( bot):
    return random.choice(['ping','forward','rotCW'])


bot = lib.CBot('Anita Pinger')

while bot.active:
    bot.getMapState()
    logging.debug(bot.msg)

    if bot.active:
        move = calcMove(bot)
        bot.sendMessage( move )
        logging.debug(bot.msg)
        logging.info(bot.lastping)

