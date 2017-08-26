'''
Script to auto-create and execute competitions
to determine a leaderboard for all the digital
dodgeball bots in the Bots folder
'''

import library
import os
import server
import random
import numpy as np
import json

initval = 1000

def diffalg(diff):
    return max(1,0.1*diff+50)

for i in range(200):
    # Read in records
    if os.path.isfile('scores.json'):
        with open('scores.json', 'r') as f:
            ratings = json.load(f)
    else:
        ratings = {}

    # Get random list of bots
    bots = np.random.choice(
            os.listdir('Bots'),
            replace=False,
            size=np.random.randint(2,5)
            )
    print(bots)

    # If a new bot, initialize its rating
    for bot in bots:
        if bot not in ratings.keys():
            ratings[bot] = [initval]

    # Get all bots ratings
    botRatings = [ratings[bot][-1] for bot in bots]

    # Average Rating
    avgRating = np.mean(botRatings)

    # Subtract buyins from ratings
    buyinpool = 0
    for bot in bots:
        # Get rating difference
        diff = ratings[bot][-1] - avgRating
        # Calculate Buyin
        buyin = diffalg(diff)
        buyinpool += buyin
        ratings[bot].append(ratings[bot][-1] - buyin)

    victornum = server.main(bots, 20, 10, False, 1, replaysave=False)
    if victornum != '':
        victoridx = int(victornum) - 51
        ratings[bots[victoridx]].append(float(ratings[bots[victoridx]][-1]) + buyinpool)
    else:
        for bot in bots:
            ratings[bot].append(ratings[bot][-1] + buyinpool/len(bots))

    with open('scores.json', 'w') as f:
        json.dump(ratings, f)
   
import matplotlib
import matplotlib.pyplot as plt

for key in ratings:
    plt.plot(ratings[key], label=key)
plt.legend()
plt.xlabel('Games')
plt.ylabel('Rating')
plt.show()

