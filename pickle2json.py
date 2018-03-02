# Quick script to test converting pickle replay files to JSON

import pickle, json, numpy

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


with open('lastgame.pickle', 'rb') as f:
    data = pickle.load(f)

with open('lastgame.json', 'w') as f:
    f.write(json.dumps(data, indent=4, cls=MyEncoder))
