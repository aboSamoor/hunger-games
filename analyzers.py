#import matplotlib
#matplotlib.use('tkagg')
#import matplotlib.pyplot
#matplotlib.pyplot.ion()
from pylab import *

class FoodAnalyzer():

  def __init__(self, game):
    self.game = game

  def plot(self, meta = False):
    figure()
    plot(self.game.history['food'])
    if meta:
      legend([p.name for p in self.game.unshuffled])
    else:
      legend(['' for p in self.game.unshuffled])
