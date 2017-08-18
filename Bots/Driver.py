#===================================================
#
# File Name: Driver.py
# 
# Purpose: A specal bot to allow for user interaction
#
# Created by: Jed Rembold
#
#===================================================

# -- Importing Modules --
# Just grabbing the basics here
import sys
sys.path.append('./')
import library as lib

# -- Movement Decision Functions --
def getMove(sel ):
    '''Function to take menu selection and
    return the bot movement command'''
    if sel == '1':
        return 'forward'
    if sel == '2':
        return 'rotCW'
    if sel == '3':
        return 'rotCCW'
    if sel == '4':
        return 'spear'
    if sel == '5':
        return 'ping'
    else:
        return 'leave'

def getSelection():
    '''Function to create an options menu and
    prompt user for their choice'''
    menu = {}
    menu['1'] = ' - Move Forward'
    menu['2'] = ' - Rotate CW'
    menu['3'] = ' - Rotate CCW'
    menu['4'] = ' - Throw Spear'
    menu['5'] = ' - Ping'
    menu['q'] = ' - Suicide'

    options=menu.keys()
    print('You are player {}'.format(bot.UCODE))
    print('You have {} spears.'.format(bot.spearcount))
    for entry in options:
        print(entry, menu[entry])
    selection = ''
    while selection == '':
        selection = input('Please select: ')
    return selection



# -- Initialize Bot --
bot = lib.CBot('Driver')    #give boring name


# -- Main Loop --
while bot.active:                       #while bot active
    bot.getMapState()                   #get map state

    if bot.active:                      #if still alive
        move = getMove(getSelection())  #prompt player for move option
        bot.sendMessage( move )         #send picked option to server
