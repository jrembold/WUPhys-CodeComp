#===================================================
#
# File Name: client.py
# 
# Purpose: To serve as the bot and talk to the game master
#
# Creation Date: 13-06-2017
#
# Last Modified: Fri 16 Jun 2017 02:30:38 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import socket, struct
import socket_cmds as scmds

HOST = 'localhost'
PORT = 10000
UCODE= ''

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

def checkin(sock):
    global UCODE
    msg = scmds.createMessage( scmds.CMDS['checkin'], True )
    sock.sendall(msg)
    buf, reply, msg = scmds.receiveMessage( sock )
    print('You are contenter #{}'.format(msg[2:]))
    UCODE = msg[2:]

def leave( sock ):
    msg = scmds.createMessage( scmds.CMDS['leave'] + UCODE )
    sock.sendall(msg)

if __name__ == '__main__':

    sock = socket.create_connection((HOST,PORT))
    checkin(sock)

    while True:
        sel = getSelection()
        if sel == '1':
            msg = scmds.createMessage( scmds.CMDS['forward'] + UCODE )
            sock.sendall(msg)
        if sel == '2':
            msg = scmds.createMessage( scmds.CMDS['rotCW'] + UCODE )
            sock.sendall(msg)
        if sel == '3':
            msg = scmds.createMessage( scmds.CMDS['rotCCW'] + UCODE )
            sock.sendall(msg)
        if sel == 'q':
            leave( sock )
            break

    print('Closing socket')
    sock.close()
