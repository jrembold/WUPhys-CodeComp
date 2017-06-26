#===================================================
#
# File Name: viewer.py
# 
# Purpose: To replay bot save files 
#
# Creation Date: 25-06-2017
#
# Last Modified: Mon 26 Jun 2017 12:21:09 AM PDT
#
# Created by: Jed Rembold
#
#===================================================

import pickle, time
import numpy as np
import matplotlib.pyplot as plt

with open('lastgame.pickle', 'rb') as f:
    mapstate = pickle.load(f)

def getPlayerDirSym(player):
    if player['face'] == 0: return '^'
    if player['face'] == 1: return '>'
    if player['face'] == 2: return 'v'
    if player['face'] == 3: return '<'
    return 'o'

def getSpearDirSym(spear):
    if spear[2] == 0: return '$↑$'
    if spear[2] == 1: return '$→$'
    if spear[2] == 2: return '$↓$'
    if spear[2] == 3: return '$←$'

def getSpearColor(spear):
    if spear[3]: return 'red'
    return 'gray'

width, height = mapstate['Map'].shape
fig = plt.figure()
ax = fig.add_axes((0.05,0.05,0.9,0.9), aspect='equal', xlim=(0,width), ylim=(0,height))
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)


numrounds = max([x for x in mapstate.keys() if isinstance(x,int)])
for rnd in range(numrounds+1):
    ax.cla()
    ax.imshow(mapstate['Map'], cmap='gray_r')
    for p in mapstate[rnd]['players']:
        player = mapstate[rnd]['players'][p]
        ax.scatter(player['x'], player['y'], marker=getPlayerDirSym(player), label=player['name'])
    for s in mapstate[rnd]['spears']:
        ax.scatter(s[0], s[1], marker=getSpearDirSym(s), color=getSpearColor(s))
    ax.legend(loc='center left', bbox_to_anchor=(1,0.5))
    plt.pause(0.05)

time.sleep(5)
