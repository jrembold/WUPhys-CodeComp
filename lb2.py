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
desgames = 1000


def calcnew(currbot, results, bots, ratings, history):
    '''
    Function to use pairwise elo ratings to update a bots
    rating based on the results of a match
    '''
    # K factor. Higher = faster adjustments
    k=max(16-.015*history[currbot], 1)

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
    # print('For {}: A-E = {} - {}'.format(currbot, act_points,est_points))

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
    # bots = np.random.choice(
            # os.listdir('Bots'),
            # size = np.random.randint(2,5),
            # replace = False,
            # )

    def botchooser(ratings):
        # Choose a random subset of Bots with matchmaking
        bots = []
        botlist = os.listdir('Bots')
        for tbot in botlist:
            if tbot not in ratings.keys():
                ratings[tbot] = [initval]
        matchesplayed = {currbot: len(ratings[currbot]) for currbot in botlist}
        leastplayed = min(matchesplayed, key=matchesplayed.get)
        bots.append(leastplayed)
        botlist.remove(leastplayed)
        random.shuffle(botlist)
        # bots.append(botlist.pop(0))
        target = 50
        while len(bots) < random.randint(2,5):
            for i in range(len(botlist)-1):
                tbot = botlist[i]
                diff = abs(ratings[tbot][-1]-ratings[bots[0]][-1])
                if diff < target:
                    bots.append(botlist.pop(i))
                    target = 50
                    break
            target += 50
        #print('Competing bots: {}'.format(bots))
        return bots

    bots = botchooser(ratings)


    # If a new bot, initialize its rating
    # for bot in bots:
        # if bot not in ratings.keys():
            # ratings[bot] = [initval]

    # Play competition
    results = server.main(bots, size=20, obstacles=10, viewer=False, delay=1, replaysave=False, noprint=True)

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

# Format and output final table of results
results = {currbot[:-3]: ratings[currbot][-1] for currbot in ratings.keys()}
sorted_results = sorted(results, key=results.get)
sorted_results.reverse()
output = {bot: results[bot] for bot in sorted_results}
with open('results.json', 'w') as f:
    for entry in output:
        f.write('{}, {:0.0f}\n'.format(entry, output[entry]))

plt.legend()
plt.show()

