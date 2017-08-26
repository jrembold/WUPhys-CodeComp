#===================================================
#
# File Name: lb2.py
# 
# Purpose: To test an ELO rating system for Digital Dodgeball 
#
# Creation Date: 26-08-2017
#
# Last Modified: Sat 26 Aug 2017 03:18:25 PM PDT
#
# Created by: Jed Rembold
#
#===================================================

import library
import os
import server
import random
import numpy as np
import json

initval = 1000
desgames = 20


def calcnew(currbot, results, bots, ratings):
    '''
    Function to use pairwise elo ratings to update a bots
    rating based on the results of a match
    '''
    # K factor. Higher = faster adjustments
    k=32

    # Calculate actual points earned
    act_points = 0
    other_bots = [bot for bot in bots if bot != currbot]
    for bot in other_bots:
        if results[currbot] > results[bot]:
            act_points += 1
        elif results[currbot] == results[bot]:
            act_points += 0.5
        else:
            act_points += 0

    # Calculate estimated points earned
    est_points = 0
    for bot in other_bots:
        est_points += 1/(1+10**((ratings[bot][-1]-ratings[currbot][-1])/400))
    print('For {}: A-E = {} - {}'.format(currbot, act_points,est_points))

    # Calculate score update
    return ratings[currbot][-1] + k*(act_points-est_points)

for i in range(desgames):
    # Read in the ratings if they exist
    if os.path.isfile('scores.json'):
        with open('scores.json', 'r') as f:
            ratings = json.load(f)
    else:
        ratings = {}

    # Choose a random subset of the Bots
    bots = np.random.choice(
            os.listdir('Bots'),
            size = np.random.randint(2,5),
            replace = False,
            )

    # If a new bot, initialize its rating
    for bot in bots:
        if bot not in ratings.keys():
            ratings[bot] = [initval]

    # Play competition
    results = server.main(bots, size=20, obstacles=10, viewer=False, delay=1, replaysave=False)

    # Calculate new bot ratings
    newrating = {currbot: calcnew(currbot, results, bots, ratings) for currbot in bots}

    # Append new ratings to ratings
    for bot in bots:
        ratings[bot].append(newrating[bot])

    # Save ratings
    with open('scores.json', 'w') as f:
        f.write(json.dumps(ratings, indent=4, sort_keys=True))

