#===================================================
#
# File Name: client.py
# 
# Purpose: To serve as the bot and talk to the game master
#
# Creation Date: 13-06-2017
#
# Last Modified: Tue 13 Jun 2017 04:25:13 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import socket

def strToBytes( string ):
    return str.encode(string, 'UTF-8')

def bytesToStr( byte ):
    return str( byte, 'UTF-8')


message = ''
while message != 'q':
    sock = socket.create_connection(('localhost',10000))

    message = input('Enter your message:')

    try:
        print('Sending {}'.format(message))

        sock.sendall(strToBytes(message))

        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(64)
            amount_received += len(data)
            print('Received {}'.format(data))

    finally:
        print('Closing socket')
        sock.close()
