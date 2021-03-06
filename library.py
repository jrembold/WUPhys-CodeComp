#===================================================
#
# File Name: library.py
# 
# Purpose: To be a library of common shared socket cmds 
#
# Creation Date: 14-06-2017
#
# Last Modified: Sat 26 Aug 2017 03:16:29 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import pickle, socket, time

CMDS = {}
CMDS['checkin'] = 'aa'
CMDS['leave'] = 'ab'
CMDS['forward'] = 'ac'
CMDS['rotCW'] = 'ad'
CMDS['rotCCW'] = 'ae'
CMDS['ball'] = 'af'
CMDS['ping'] = 'ag'
CMDS['botfname'] = 'ah'

CMDS['mapstate'] = 'ba'
CMDS['retping'] = 'bg'


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
    # Add 3 byte message length
    ba.extend(bytes(str(msglen).zfill(4), 'UTF-8'))
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
        inc_bytes = socket_conn.recv(4)
        msglen = int(str(inc_bytes, 'UTF-8'))
        buf.extend(inc_bytes)

        # Read in byte message
        inc_bytes = socket_conn.recv(msglen)
        buf.extend(inc_bytes)

        # Check to ensure message ends with terminator
        last_bytes = socket_conn.recv(2)
        if last_bytes != b'@@':
            print(buf)
            print('Message supposed to be {} bytes long'.format(msglen))
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
        msglen = int(str(buf[6:10], 'UTF-8'))
        msg = str(buf[10:10+msglen], 'UTF-8')
        return [msgtype, msg, reply]
    return [None, None, None]

def parseMapState( buf ):
    if buf == b'':
        print('Server is sending nonsense. It probably went down.')
        return None
    elif buf[:2] != b'!!' or buf[-2:] != b'@@':
        print('Unknown message sent')
        return None
    else:
        if buf[2:4] == b'00':
            reply = False
        else:
            reply = True
        msgtype = str(buf[4:6], 'UTF-8')
        msglen = int(str(buf[6:10], 'UTF-8'))
        msg = pickle.loads(buf[10:10+msglen])
        return msg

def sendReply( socket_conn, msgtype, msg ):
    buf = createMessage( msgtype, msg, False )
    socket_conn.sendall(buf)




class CBot:
    def __init__(self, name):
        self.name = name[5:]
        self.HOST = 'localhost'
        self.PORT = 10000
        self.UCODE = ''
        self.alive = True
        self.playercount = 1
        self.vision = []
        self.ballcount = 2
        self.active = True
        self.lastping = {'Terrain':[], 'ASpear':[], 'DSpear':[], 'Enemy':[]}
        self.msg = ''
        self.SOCK = socket.create_connection((self.HOST,self.PORT))
        self.checkin()

    def checkin(self):
        msg = createMessage( CMDS['checkin'], self.name, True )
        self.SOCK.sendall(msg)
        reply = receiveMessage( self.SOCK )
        [msgtype, msg, needsreply] = parseMessage( reply )
        # print('You are contenter #{}'.format(msg))
        self.UCODE = msg
        # msg = createMessage(CMDS['botfname'], self.UCODE + self.fname)
        # self.SOCK.sendall(msg)

    def sendMessage( self, cmdstr ):
        msg = createMessage( CMDS[cmdstr], self.UCODE )
        self.SOCK.sendall(msg)

    def getMapState( self ):
        mapstate = receiveMessage( self.SOCK )
        self.msg = mapstate
        state = parseMapState( mapstate )
        self.alive = state['alive']
        self.ballcount = state['balls']
        self.playercount = state['pcount']
        self.vision = state['vision']
        self.lastping = state['lastping']

        if not self.alive:
            # print('You have been killed!')
            self.active = False
            self.sendMessage('leave')
            self.SOCK.close()

        if self.playercount == 1:
            # print('You are victorious!')
            self.active = False
            self.sendMessage('leave')
            self.SOCK.close()

