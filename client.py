#===================================================
#
# File Name: client.py
# 
# Purpose: To serve as the bot and talk to the game master
#
# Creation Date: 13-06-2017
#
# Last Modified: Wed 14 Jun 2017 05:35:22 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import socket, struct
import socket_cmds as scmds

HOST = 'localhost'
PORT = 10000

def checkin(sock):
    msg = scmds.createMessage( scmds.CMDS['checkin'], True )
    sock.sendall(msg)
    buf, reply, msg = scmds.receiveMessage( sock )
    print(msg)

if __name__ == '__main__':

    sock = socket.create_connection((HOST,PORT))
    checkin(sock)

    while True:
        sock = socket.create_connection((HOST,PORT))
        message = input('Enter your 4 character message: ')
        if message == 'q':
            break

        try:
            print('Sending {}'.format(message))
            msg = scmds.createMessage( message )

            sock.sendall(msg)
        except:
            print('Error occured. Closing socket')
            sock.close()

    print('Closing socket')
    sock.close()
