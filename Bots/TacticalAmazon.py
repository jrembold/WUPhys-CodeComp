#===================================================
#
# File Name: TacticalAmazon.py
# 
# Purpose: A more complex bot with better throwing logic
#
# Created by: Jed Rembold
#
#===================================================

# -- Importing Modules --
# These are largely the same as in the past examples
import sys
sys.path.append('./')
import library as lib
import numpy as np
from math import floor

# The Logging module can be handy to troubleshoot, since
# printing everything to the screen when there are multiple
# bots gets real ugly real fast
import logging

# Logging Config. Beyond the filename, you could keep the rest of this the same
logging.basicConfig(
        # Filename to log to
        filename = 'Logs/TacticalAmazon.log',
        # Logging supports multiple levels and will show everything above
        # this level. Debug is the bottom, so it will show everything
        level = logging.DEBUG,
        # Style for defining the below format
        style = '{',
        # What will be saved in the log file
        format = '[{levelname}] [Line: {lineno}] {message}',
        # Rewrite the log file each run
        filemode = 'w',
        )


# -- Decision Logic Functions --

def getObjDir( obj ):
    '''Function to determine what direction
    something is facing based off its decimal'''
    d = round(obj % 1, 1)           # Remainder when divided by 1
    # Assign directions as explained in the readme
    if d == 0.0: return 'North'
    if d == 0.1: return 'East'
    if d == 0.2: return 'South'
    if d == 0.3: return 'West'
    return None #if all else fails then something is very wrong...

def opposite( direction ):
    '''Function to return the opposite of a direction
    Done mainly for convenience'''
    if direction=='North': return 'South'
    if direction=='South': return 'North'
    if direction=='East': return 'West'
    if direction=='West': return 'East'

def calcMove( bot):
    '''Main function to determine the decision of the bot'''
    global tcount
    v = np.array(bot.vision[1:])

    #Get the bots facing direction. Vision starts at the bot
    #itself so vision[0] is the bots actual position
    botdir = getObjDir(bot.vision[0])

    #Do I see a bot ahead of me?
    if any(v>10):
        #I do! Is there empty space in front of me?
        if v[0] == 0:
            #There is! Do I still have ammunition availabe?
            if bot.spearcount>0:
                #I do! Is there a spear coming toward me from this direction?
                #If so, I better throw one to save myself
                if any([opposite(getObjDir(i))==botdir for i in v if floor(i)==2]):
                    return 'spear'
                #If not, is there a spear I already threw moving away from me
                #No sense wasting spears if I already threw one. Rotate.
                elif any([floor(i)==2 for i in v]):
                    return 'rotCW'
                #No spears between me and target. Throw!!
                else:
                    return 'spear'
    # No enemies seen. Any fallen spears lying around?
    # If so, move forward to grab them
    if any(v==3) and not any(v>10):
        tcount = 0
        return 'forward'
    #if stationary too long, move
    if tcount > 3 and len(v)>0:
        tcount = 0
        return 'forward'
    else:
        #Otherwise, turn clockwise
        tcount += 1
        return 'rotCW'



# -- Initialize --
bot = lib.CBot('Ariel the Amazon')  #Cooler name
tcount = 0                          #Turns without moving
roundnum = 0                        #Game round

# -- Main Loop --
while bot.active:
    bot.getMapState()
    # This is how you can log things. In this came I'm logging at the info
    # level, but you can also log at the debug, warning, or error levels
    # I just pass it a string with the normal formatting rules
    # Here, I'm logging both the round number and what I see in front of me
    logging.info('[Round: {:^2}]: I see: {}'.format(roundnum, bot.vision))

    if bot.active:
        move = calcMove(bot)
        #Here, I log the round number and what move I chose to make
        logging.info('[Round: {:^2}]: Sent move: {}'.format(roundnum,move))
        bot.sendMessage( move )

    roundnum += 1   #incrementing the round number
