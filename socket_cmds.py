#===================================================
#
# File Name: socket_cmds.py
# 
# Purpose: To be a library of common shared socket cmds 
#
# Creation Date: 14-06-2017
#
# Last Modified: Mon 19 Jun 2017 03:21:57 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

CMDS = {}
CMDS['checkin'] = 'aaaa'
CMDS['leave'] = 'ab'
CMDS['forward'] = 'ac'
CMDS['rotCW'] = 'ad'
CMDS['rotCCW'] = 'ae'

def createMessage( msg, needs_reply=False ):
    ba = bytearray()
    # Message Initialize
    ba.extend(b'!!')
    # Needs reply?
    if needs_reply:
        ba.extend(b'01')
    else:
        ba.extend(b'00')
    bytemsg = bytes(msg, 'UTF-8')
    msglen = len(bytemsg)
    # Add 2 byte message length
    ba.extend(bytes(str(msglen).zfill(2), 'UTF-8'))
    # Add actual message
    ba.extend(bytemsg)
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

        # Get msg length
        inc_bytes = socket_conn.recv(2)
        msglen = int(str(inc_bytes, 'UTF-8'))

        # Read in 4 byte message
        inc_bytes = socket_conn.recv(msglen)
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
