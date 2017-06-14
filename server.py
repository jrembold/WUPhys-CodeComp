#===================================================
#
# File Name: server.py
# 
# Purpose: To server as the server and game master 
#
# Creation Date: 13-06-2017
#
# Last Modified: Wed 14 Jun 2017 04:37:10 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import socket, select

CONNECTION_LIST = []
PORT = 10000

def bindAndListen( sock, host, port ):
    '''Function to initialize listening on a
    server and particular port'''

    print('Starting server up on {} on port {}'.format(host,port))
    sock.bind((host,port))
    sock.listen(1)
    CONNECTION_LIST.append(sock)

def receiveMessage( socket_conn ):
    '''Reads in the formatted bytearray message'''

    buf = bytearray()
    inc_bytes = socket_conn.recv(2)
    # Check is new message starting
    if inc_bytes == b'!!':
        print('Incoming Message!')
        buf.extend(inc_bytes)

        # Get reply status
        buf.extend(socket_conn.recv(2))

        # Read in 4 byte message
        buf.extend(socket_conn.recv(4))

        # Check to ensure message ends with terminator
        last_bytes = socket_conn.recv(2)
        if last_bytes != b'@@':
            raise RuntimeError('Error in send message')
        else:
            buf.extend(last_bytes)
    return buf



# Create the Socket
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Start listening
bindAndListen( server_sock, 'localhost', 10000 )

while True:
    # Wait for a connection
    read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

    for sock in read_sockets:
        # A New connection
        if sock == server_sock:
            sockfd, addr = server_sock.accept()
            CONNECTION_LIST.append(sockfd)
            print('Client ({}, {}) connected'.format(addr[0], addr[1]))

        #Incoming client message
        else:
            msg = receiveMessage( sock )
            if msg != b'':
                print(msg)


server_sock.close()
