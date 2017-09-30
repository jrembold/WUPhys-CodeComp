#===================================================
# Bot Name:
# Author:
#===================================================

# -- Imports --
import sys              #importing sys for the below command
sys.path.append('./')   #this lets us keep the bots in a separate directory
import library as lib   #importing the main library functions

# -- Initialze Bot --
bot = lib.CBot(__file__)  #this initializes the bot with the same name as your filename

# -- Main Code --
while bot.active:           #for as long as the bot is alive, do the following
    bot.getMapState()       #get an update on the current mapstate, see readme for details

    if bot.active:
        # ----- Enter Logic code here (or in a separate function if you want) ------
        # See readme for how to interpret mapstates







        bot.sendMessage( '''enter desired move here''' )
