#===================================================
#
# Filename: PingMan.py
#
# Purpose: To showcase use of the ping command
#
# Author: Jed Rembold
#
#===================================================

# -- Importing Modules --
# Same imports as previously here
import sys
sys.path.append('./')
import library as lib
import numpy as np


# -- Decision Making Functions --

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

def calcMove(bot):
    '''Function to determine best decision emphasizing
    reading from the last ping dictionary'''

    vis = np.array(bot.vision[1:])      #getting my vision straight ahead
    mydir = getObjDir(bot.vision[0])    #getting my personal facing direction

    #If we just pinged:
    if rcnt % 5 == 0:
        #Check Ping Vision
        #Was an active ball seen?
        if len(bot.lastping['ABall']):
            #Yes?! Could it hit us?
            for s in bot.lastping['ABall']:
                if s[0] == 0 or s[1] == 0:
                    #Take evasive action!
                    return 'rotCW'
        #Was a fallen ball seen?
        if len(bot.lastping['DBall']):
            #Yes? Can we get it easily?
            if any(vis[0:3]==3):
                return 'forward'
        #Was an enemy seen?
        if len(bot.lastping['Enemy']):
            #Yes? Are we facing them?
            if any(vis[0:3]>10):
                return 'ball'
            else:
                return 'rotCCW'
    if rcnt % 4 == 0:
        return 'ping'
    if len(vis):
        return 'forward'
    return 'rotCW'


# -- Initialize Bot --
bot1 = lib.CBot(__file__)       #initialize and let server know script name
rcnt = 1                        #round counter

# -- Main Loop --
while bot1.active:
    bot1.getMapState()

    if bot1.active:
        bot1.sendMessage( calcMove(bot1) )

    rcnt += 1                   #increment round counter

