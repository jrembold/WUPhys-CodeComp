#===================================================
#
# File Name: client.py
# 
# Purpose: To serve as the bot and talk to the game master
#
# Creation Date: 13-06-2017
#
# Last Modified: Thu 15 Jun 2017 03:12:34 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import socket, struct
import socket_cmds as scmds

HOST = 'localhost'
PORT = 10000
UCODE= ''

def checkin(sock):
    global UCODE
    msg = scmds.createMessage( scmds.CMDS['checkin'], True )
    sock.sendall(msg)
    buf, reply, msg = scmds.receiveMessage( sock )
    print('You are contented #{}'.format(msg[2:]))
    UCODE = msg[2:]

def leave( sock ):
    msg = scmds.createMessage( scmds.CMDS['leave'] + UCODE )
    sock.sendall(msg)

if __name__ == '__main__':

    sock = socket.create_connection((HOST,PORT))
    checkin(sock)

    while True:
        message = input('Enter your 4 character message: ')
        if message == 'q':
            leave( sock )
            break
        else:
            try:
                print('Sending {}'.format(message))
                msg = scmds.createMessage( message )

                sock.sendall(msg)
            except:
                print('Error occured. Closing socket')
                sock.close()

    print('Closing socket')
    sock.close()
