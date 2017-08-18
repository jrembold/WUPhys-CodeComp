#===================================================
#
# File Name: Simpleman.py
# 
# Purpose: A simple bot for charging at things
#
# Created by: Jed Rembold
#
#===================================================

# -- Importing Stuff --
import sys              #Grabbing sys for the below command
sys.path.append('./')   #This lets us keep the bots in a sep folder
import library as lib   #Importing the main library


'''This time I broke the bot decision logic out into its
own function. This makes it a bit easier for me to keep
track of everything, but is totally not necessary!'''

# This function decides what the bot will do
def calcMove( bot ):
    #Anything in my vision that is non-zero is either
    #an enemy or a spear. So if I see one, go forwards!
    if any(bot.vision[1:]):     #any means if any of the values I see are >0, then go
        return 'forward'
    #If I see only zeros (air) then I'll turn looking for something else
    else:
        return 'rotCW'


# -- Initializing the Bot --
bot = lib.CBot('Simple Simon')  #Giving it a cool (not really) name!

# -- Main Loop --
while bot.active:               #while alive,
    bot.getMapState()           #get the current map state

    if bot.active:              #if still alive
        move = calcMove(bot)    #calculate our best move
        bot.sendMessage( move ) #send best move to server