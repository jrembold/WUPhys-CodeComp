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

records = {'Amy the Amazon': 1000}

winners = []
for i in range(10):
    # Get random list of bots
    bots = np.random.choice(
            os.listdir('Bots'),
            replace=False,
            size=np.random.randint(2,5)
            )

    winners.append(server.main(bots, 20, 10, False, 1, replaysave=False))

print(winners)

with open('scores.json', 'w') as f:
    json.dump(records, f)
    
