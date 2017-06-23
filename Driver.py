#===================================================
#
# File Name: Driver.py
# 
# Purpose: A custom bot to allow for user interaction
#
# Creation Date: 20-06-2017
#
# Last Modified: Thu 22 Jun 2017 10:42:08 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import library as lib

def getMove(sel ):
    if sel == '1':
        return 'forward'
    if sel == '2':
        return 'rotCW'
    if sel == '3':
        return 'rotCCW'
    if sel == '4':
        return 'spear'
    else:
        return 'leave'

def getSelection():
    menu = {}
    menu['1'] = ' - Move Forward'
    menu['2'] = ' - Rotate CW'
    menu['3'] = ' - Rotate CCW'
    menu['4'] = ' - Throw Spear'
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


bot = lib.CBot('Driver')

while bot.active:
    bot.getMapState()

    if bot.active:
        move = getMove(getSelection())
        bot.sendMessage( move )
