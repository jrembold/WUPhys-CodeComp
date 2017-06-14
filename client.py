#===================================================
#
# File Name: client.py
# 
# Purpose: To serve as the bot and talk to the game master
#
# Creation Date: 13-06-2017
#
# Last Modified: Wed 14 Jun 2017 04:36:29 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import socket, struct

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

message = ''
while message != 'q':
    sock = socket.create_connection(('localhost',10000))
    message = input('Enter your 4 character message: ')

    try:
        print('Sending {}'.format(message))
        msg = createMessage( message )

        sock.sendall(msg)

    finally:
        print('Closing socket')
        sock.close()
