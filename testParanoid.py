import game, paranoid, dummyAgent
import operator
import matplotlib.pyplot as plt

numGames = 50
numPlayers = 4
playerIndex = 0
scores = []
for i in xrange(3):
    gm = game.Game([paranoid.ParanoidAgent] + [dummyAgent.DummyAgent for i in xrange(numPlayers - 1)])
    res = gm.playMultGames(verbose=False, restarts = 10, n=numGames)
    rankings = [sum(r.index(p) for r in res) for p in xrange(numPlayers)]
    scores += [r.index(playerIndex) for r in res]
    print '--------------------------------'
    print 'Average rankings after {0} games'.format(numGames)
    print '--------------------------------'
    for player in xrange(numPlayers):
        print 'Player {0}: {1:.5}'.format(player, rankings[player]/float(numGames)),

def moving_average(a, n=10):
    ret = sum(a)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / float(n)

plt.plot(scores)
plt.show()
