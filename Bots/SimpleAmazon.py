#===================================================
#
# File Name: SimpleAmazon.py
# 
# Purpose: A simple bot for charging and throwing
#
# Created by: Jed Rembold
#
#===================================================

import sys              #Grabbing the sys library
sys.path.append('./')   #Making sure we can access the library module
import library as lib   #Loading library module
import numpy as np      #And I want numpy too in this case


# Again, I separated out the decision logic into its own function
def calcMove( bot ):
    global tcount                       #utilize global tcount
    v = np.array(bot.vision[1:])        #convert vision list to numpy array
    #If any enemy in front to me and I have balls, throw one!
    if any(v>10) and bot.ballcount>0:
        return 'ball'
    #or, if there is a grounded ball in front of me, go grab it!
    elif any(v==3):
        tcount = 0                      #I moved, so return to 0
        return 'forward'
    #if stationary too long, move
    elif tcount > 3 and len(v)>0:       #Tcount is too big and no wall in front of me
        tcount = 0                      #Return to zero, I'm about to move
        return 'forward'
    #Otherwise, turn clockwise
    else:
        tcount += 1                     #I didn't move, so increment tcount
        return 'rotCW'



# -- Initializing Bot --
bot = lib.CBot('Amy the Amazon')    #Cool name granted

#In an effort to keep from dying because of inactivity
#I create a counter that increments each time I do NOT
# move forward. So we'll start it at zero
tcount = 0

# -- Main Loop --
while bot.active:                   #while alive:
    bot.getMapState()               #get the map state

    if bot.active:                  #if still alive
        move = calcMove(bot)        #calculate best move
        bot.sendMessage( move )     #send move to server
