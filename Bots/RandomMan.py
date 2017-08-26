#===================================================
#
# File Name: RandomMan.py
# 
# Purpose: A bot moving in random directions
#
# Created by: Jed Rembold
#
#===================================================

# -- Imports --
import sys              #importing sys for the below command
sys.path.append('./')   #this lets us keep the bots in a separate directory
import library as lib   #importing the main library functions
import random           #This bot needs the random library

# -- Initial Bot --
bot = lib.CBot(__file__)  #this initializes our bot and gives it a name: "Ia Rando"

# -- Main Code --
while bot.active:           #for as long as the bot is alive, do the following
    bot.getMapState()       #get an update on the current mapstate, see readme for details

    # It is possible the map just notified you that you are dead
    # So we check once more before sending anything back as the
    # server doesn't like dead bots trying to talk to it :)
    if bot.active:         

        #Now we choose randomly from a list of our available moves
        move = random.choice(['forward', 'rotCW', 'rotCCW', 'ball', 'ping'])

        #And then we send the move to server
        bot.sendMessage( move )
