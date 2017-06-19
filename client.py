#===================================================
#
# File Name: client.py
# 
# Purpose: To serve as the bot and talk to the game master
#
# Creation Date: 13-06-2017
#
# Last Modified: Mon 19 Jun 2017 04:30:17 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import socket, struct, random
import socket_cmds as scmds
import time

HOST = 'localhost'
PORT = 10000
UCODE= ''
SOCK = ''


def getSelection():
    menu = {}
    menu['1'] = ' - Move Forward'
    menu['2'] = ' - Rotate CW'
    menu['3'] = ' - Rotate CCW'
    menu['q'] = ' - Suicide'

    options=menu.keys()
    for entry in options:
        print(entry, menu[entry])
    selection = input('Please select: ')
    return selection

def checkin():
    global UCODE
    msg = scmds.createMessage( scmds.CMDS['checkin'], '', True )
    SOCK.sendall(msg)
    reply = scmds.receiveMessage( SOCK )
    print(reply)
    [msgtype, msg, needsreply] = scmds.parseMessage( reply )
    print('You are contenter #{}'.format(msg))
    UCODE = msg

def leave():
    msg = scmds.createMessage( scmds.CMDS['leave'], UCODE )
    SOCK.sendall(msg)

def sendMessage( cmdstr ):
    msg = scmds.createMessage( scmds.CMDS[cmdstr], UCODE )
    SOCK.sendall(msg)

if __name__ == '__main__':

    SOCK = socket.create_connection((HOST,PORT))
    checkin()

    while True:
        # Selection Testing ----------
        # sel = getSelection()
        # if sel == '1':
            # sendMessage('forward' )
        # if sel == '2':
            # sendMessage('rotCW' )
        # if sel == '3':
            # sendMessage('rotCCW')
        # if sel == 'q':
            # sendMessage('leave')
            # # leave()
            # break

        # Automatic Movement Testing ---
        for i in range(30):
            move = random.choice(['forward', 'rotCW', 'rotCCW', 'forward'])
            sendMessage( move )
            time.sleep(0.5)
        sendMessage('leave')
        break

    print('Closing socket')
    SOCK.close()
