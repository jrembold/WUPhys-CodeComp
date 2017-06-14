#===================================================
#
# File Name: client.py
# 
# Purpose: To serve as the bot and talk to the game master
#
# Creation Date: 13-06-2017
#
# Last Modified: Wed 14 Jun 2017 04:47:15 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import socket, struct

HOST = 'localhost'
PORT = 10000
CMDS = {}
CMDS['checkin'] = 'aaaa'

def createMessage( msg, needs_reply=False ):
    ba = bytearray()
    # Message Initialize
    ba.extend(b'!!')
    # Needs reply?
    if needs_reply:
        ba.extend(b'01')
    else:
        ba.extend(b'00')
    # 4 byte message
    if len(msg)>4:
        raise RuntimeError('Msg too long!')
    ba.extend(bytes(msg, 'UTF-8'))
    # End Message
    ba.extend(b'@@')
    return ba

def checkin(sock):
    msg = createMessage( CMDS['checkin'], True )
    sock.sendall(msg)

if __name__ == '__main__':

    message = ''
    while message != 'q':
        sock = socket.create_connection((HOST,PORT))

        checkin(sock)

        message = input('Enter your 4 character message: ')

        try:
            print('Sending {}'.format(message))
            msg = createMessage( message )

            sock.sendall(msg)

        finally:
            print('Closing socket')
            sock.close()
