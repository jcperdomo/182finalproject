import game, paranoid, dummyAgent
import operator

numGames = 10
numPlayers = 4
playerIndex = 1
gm = game.Game([dummyAgent.DummyAgent, paranoid.ParanoidAgent] + [dummyAgent.DummyAgent for i in xrange(numPlayers - 2)])
#for agent in gm.agents:
#    print sum(k*v for k, v in agent.hand.items()),
#    print agent.hand
#print gm.playGame(verbose=True)
#print gm.agents[0].nodeList
res = gm.playMultGames(verbose=True, restarts = 10, n=numGames)
print '-------------------------------------------'
#print 'Average nodes expanded after {0} games: {1:.5}'.format(numGames, sum(gm.agents[0].nodeList) / float(numGames))
rankings = [sum(r.index(p) for r in res) for p in xrange(numPlayers)]
scores = [r.index(playerIndex) for r in res]
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
plt.plot(moving_average(scores))
plt.show()
