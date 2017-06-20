#===================================================
#
# File Name: socket_cmds.py
# 
# Purpose: To be a library of common shared socket cmds 
#
# Creation Date: 14-06-2017
#
# Last Modified: Tue 20 Jun 2017 02:29:59 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import pickle

CMDS = {}
CMDS['checkin'] = 'aa'
CMDS['leave'] = 'ab'
CMDS['forward'] = 'ac'
CMDS['rotCW'] = 'ad'
CMDS['rotCCW'] = 'ae'

CMDS['bvision'] = 'ba'
CMDS['bspears'] = 'bb'

def createMessage( msgtype, msg, needs_reply=False ):
    ba = bytearray()
    # Message Initialize
    ba.extend(b'!!')
    # Needs reply?
    if needs_reply:
        ba.extend(b'01')
    else:
        ba.extend(b'00')
    # Message Type
    ba.extend(bytes(msgtype, 'UTF-8'))

    if isinstance(msg, str):
        bytemsg = bytes(msg, 'UTF-8')
    else:
        bytemsg = msg
    msglen = len(bytemsg)
    # Add 2 byte message length
    ba.extend(bytes(str(msglen).zfill(3), 'UTF-8'))
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
        buf.extend(inc_bytes)

        # Get msg type
        inc_bytes = socket_conn.recv(2)
        buf.extend(inc_bytes)

        # Get msg length
        inc_bytes = socket_conn.recv(3)
        msglen = int(str(inc_bytes, 'UTF-8'))
        buf.extend(inc_bytes)

        # Read in byte message
        inc_bytes = socket_conn.recv(msglen)
        buf.extend(inc_bytes)

        # Check to ensure message ends with terminator
        last_bytes = socket_conn.recv(2)
        if last_bytes != b'@@':
            print(buf)
            raise RuntimeError('Error in sent message')
        else:
            buf.extend(last_bytes)

        return buf
    else:
        print(socket_conn, buf)

def parseMessage( buf ):
    if buf[:2] != b'!!' or buf[-2:] != b'@@':
        print('Unknown message sent')
    else:
        if buf[2:4] == b'00':
            reply = False
        else:
            reply = True
        msgtype = str(buf[4:6], 'UTF-8')
        msglen = int(str(buf[6:9], 'UTF-8'))
        msg = str(buf[9:9+msglen], 'UTF-8')
        return [msgtype, msg, reply]
    return [None, None, None]

def parseMapState( buf ):
    if buf[:2] != b'!!' or buf[-2:] != b'@@':
        print('Unknown message sent')
    else:
        if buf[2:4] == b'00':
            reply = False
        else:
            reply = True
        msgtype = str(buf[4:6], 'UTF-8')
        msglen = int(str(buf[6:9], 'UTF-8'))
        msg = pickle.loads(buf[9:9+msglen])
        return [msgtype, msg, reply]
    return [None, None, None]

def sendReply( socket_conn, msgtype, msg ):
    buf = createMessage( msgtype, msg, False )
    socket_conn.sendall(buf)
