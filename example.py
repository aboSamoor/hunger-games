# Run the following in an interactive session.

from lib import *
from bots import *
from analyzers import *

from collections import defaultdict
from urllib import urlopen, urlencode
from base64 import b64encode
import json
import logging
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

def analyze(game):
  stats = defaultdict(lambda: 0)
  for round in game.history['food']:
    ordered = enumerate(sorted(enumerate(round), key=lambda(x,y):y, reverse=True))
    for rank, (index, food) in ordered:
      stats[index] += rank

  players, ranks = zip(*[(game.players[index].name, rank) for index, rank in stats.iteritems()])
  fig = plt.figure()
  ax = plt.subplot(111)
  ax.bar(range(len(ranks)), ranks, width=10)
  upload(plt)

def upload(plt):
  tmp_name = "tmp_to_upload.png"
  plt.savefig(tmp_name)
  postdata = {}
  postdata['image'] = b64encode(open(tmp_name, 'rb').read())
  postdata['key'] = 'b3625162d3418ac51a9ee805b1840452'
  data = urlencode(postdata)
  response = urlopen("http://imgur.com/api/upload.json", data)
  total_response = response.read()
  result = json.loads(total_response)
  if result['rsp']['stat'] == 'ok':
    logging.info("imgur link: \n%s", result['rsp']['image']['original_image'])
    print("imgur link: \n{0}".format(result['rsp']['image']['original_image']))
  else:
    logging.error("%s", total_response)

ps = [Pushover(), Freeloader(), Alternator(), MaxRepHunter(), Random(0.2), Random(0.8), FairHunter(), AverageHunter()]
g = Game(ps)
a = FoodAnalyzer(g)
g.step(100)
analyze(g)
#a.plot()
