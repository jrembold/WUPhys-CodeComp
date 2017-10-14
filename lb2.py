#===================================================
#
# File Name: lb2.py
# 
# Purpose: To test an ELO rating system for Digital Dodgeball 
#
# Creation Date: 26-08-2017
#
# Last Modified: Sun 27 Aug 2017 01:28:33 AM PDT
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

import matplotlib
import matplotlib.pyplot as plt

from tqdm import tqdm

initval = 1000
desgames = 250


def calcnew(currbot, results, bots, ratings, history):
    '''
    Function to use pairwise elo ratings to update a bots
    rating based on the results of a match
    '''
    # K factor. Higher = faster adjustments
    k=max(32-.1*history[currbot], 10)

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
        est_points += 1/(1+10**((ratings[bot]-ratings[currbot])/400))
    print('For {}: A-E = {} - {}'.format(currbot, act_points,est_points))

    # Calculate score update
    return ratings[currbot] + k*(act_points-est_points)

for i in tqdm(range(desgames)):
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
    rating_now = {currbot: ratings[currbot][-1] for currbot in bots}
    history = {currbot: len(ratings[currbot]) for currbot in bots}
    newrating = {currbot: calcnew(currbot, results, bots, rating_now, history) for currbot in bots}

    # Append new ratings to ratings
    for bot in bots:
        ratings[bot].append(newrating[bot])

    # Save ratings
    with open('scores.json', 'w') as f:
        f.write(json.dumps(ratings, indent=4, sort_keys=True))

for i in ratings.keys():
    plt.plot(ratings[i], label=i)

plt.legend()
plt.show()

