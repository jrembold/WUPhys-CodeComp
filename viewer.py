#===================================================
#
# File Name: viewer.py
# 
# Purpose: To replay bot save files 
#
# Creation Date: 25-06-2017
#
# Last Modified: Thu 17 Aug 2017 04:41:58 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import pickle, time, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

pingrng = 8

p = argparse.ArgumentParser()
p.add_argument('-i', '--input', default='lastgame.pickle', help='Saved replay file to load')
p.add_argument('-d', '--delay', default=1, help='Delay scaling factor. >1 speeds up')
args = p.parse_args()


with open(args.input, 'rb') as f:
    mapstate = pickle.load(f)

def getPlayerDirSym(player):
    if player['face'] == 0: return '^'
    if player['face'] == 1: return '>'
    if player['face'] == 2: return 'v'
    if player['face'] == 3: return '<'
    return 'o'

# def getBallDirSym(ball):
    # if ball[2] == 0: return '$↑$'
    # if ball[2] == 1: return '$→$'
    # if ball[2] == 2: return '$↓$'
    # if ball[2] == 3: return '$←$'

def getBallDirSym(ball):
    return '.'

def getBallColor(ball):
    if ball[3]: return 'red'
    return 'gray'

def getPlayerColor(player):
    return player_colors[player%50]

width, height = mapstate['Map'].shape
fig = plt.figure()
# ax = fig.add_axes((0.05,0.05,0.9,0.9), aspect='equal', xlim=(0,width), ylim=(0,height))
ax = fig.add_subplot(111, aspect='equal')
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
fig.subplots_adjust(left=.05, right=.65)

player_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']


numrounds = max([x for x in mapstate.keys() if isinstance(x,int)])
for rnd in range(numrounds+1):
    ax.cla()
    ax.imshow(mapstate[rnd]['map'], cmap='gray_r')
    fig.suptitle('Round {}'.format(rnd))
    for s in mapstate[rnd]['balls']:
        ax.scatter(s[0], s[1], marker=getBallDirSym(s), color=getBallColor(s))
    # New method for generating legend since new versions
    # of matplotlib don't like identical legend entries
    playersym = []
    playerstatus = []
    for p in mapstate[rnd]['players']:
        player = mapstate[rnd]['players'][p]
        playersym.append(ax.scatter(player['x'], player['y'], marker=getPlayerDirSym(player), color=getPlayerColor(p)))
        playerstatus.append(player['name']+' - '+str(player['balls']))
    for p in mapstate[rnd]['players']:
        player = mapstate[rnd]['players'][p]
        if player['pinging']:
            ax.add_patch(patches.CirclePolygon((player['x'],player['y']), pingrng, alpha=0.15, color=getPlayerColor(p)))
    ax.legend(playersym, playerstatus,loc='center left', bbox_to_anchor=(1,0.5))
    # fig.savefig('Temp/ForGif_{:03d}.png'.format(rnd))
    plt.pause(0.05/float(args.delay))

time.sleep(5)
