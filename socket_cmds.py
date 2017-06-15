#===================================================
#
# File Name: socket_cmds.py
# 
# Purpose: To be a library of common shared socket cmds 
#
# Creation Date: 14-06-2017
#
# Last Modified: Thu 15 Jun 2017 03:12:30 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

CMDS = {}
CMDS['checkin'] = 'aaaa'
CMDS['leave'] = 'ab'

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

def receiveMessage( socket_conn ):
    '''Reads in the formatted bytearray message'''

    buf = bytearray()
    inc_bytes = socket_conn.recv(2)
    # Check is new message starting
    if inc_bytes == b'!!':
        # print('Incoming Message!')
        buf.extend(inc_bytes)

        # Get reply status
        inc_bytes = socket_conn.recv(2)
        if inc_bytes == b'00':
            reply = False
        else:
            reply = True
        buf.extend(inc_bytes)

        # Read in 4 byte message
        inc_bytes = socket_conn.recv(4)
        msg = str(inc_bytes, 'UTF-8')
        buf.extend(inc_bytes)

        # Check to ensure message ends with terminator
        last_bytes = socket_conn.recv(2)
        if last_bytes != b'@@':
            raise RuntimeError('Error in sent message')
        else:
            buf.extend(last_bytes)

        return buf, reply, msg
    else:
        print(socket_conn, buf)

def sendReply( socket_conn, msg ):
    buf = createMessage( msg, False )
    socket_conn.sendall(buf)
