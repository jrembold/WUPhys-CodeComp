#===================================================
#
# File Name: client.py
# 
# Purpose: To serve as the bot and talk to the game master
#
# Creation Date: 13-06-2017
#
# Last Modified: Fri 16 Jun 2017 02:56:56 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import socket, struct
import socket_cmds as scmds

HOST = 'localhost'
PORT = 10000
UCODE= ''
SOCK = ''

menu = {}
menu['1'] = ' - Move Forward'
menu['2'] = ' - Rotate CW'
menu['3'] = ' - Rotate CCW'
menu['q'] = ' - Suicide'

def getSelection():
    options=menu.keys()
    for entry in options:
        print(entry, menu[entry])
    selection = input('Please select: ')
    return selection

def checkin():
    global UCODE
    msg = scmds.createMessage( scmds.CMDS['checkin'], True )
    SOCK.sendall(msg)
    buf, reply, msg = scmds.receiveMessage( SOCK )
    print('You are contenter #{}'.format(msg[2:]))
    UCODE = msg[2:]

def leave():
    msg = scmds.createMessage( scmds.CMDS['leave'] + UCODE )
    SOCK.sendall(msg)

def sendMessage( cmd ):
    msg = scmds.createMessage( cmd + UCODE )
    SOCK.sendall(msg)

if __name__ == '__main__':

    SOCK = socket.create_connection((HOST,PORT))
    checkin()

    while True:
        sel = getSelection()
        if sel == '1':
            sendMessage( scmds.CMDS['forward'] )
        if sel == '2':
            sendMessage( scmds.CMDS['rotCW'] )
        if sel == '3':
            sendMessage( scmds.CMDS['rotCCW'] )
        if sel == 'q':
            leave()
            break

    print('Closing socket')
    SOCK.close()
