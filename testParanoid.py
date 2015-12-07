import game, paranoid, dummyAgent
import operator

numGames = 3
numPlayers = 4
gm = game.Game([paranoid.ParanoidAgent] + [dummyAgent.DummyAgent for i in xrange(numPlayers - 1)])
for agent in gm.agents:
    print sum(k*v for k, v in agent.hand.items()),
    print agent.hand
#print gm.playGame(verbose=True)
#print gm.agents[0].nodeList
res = gm.playMultGames(verbose=True, n=numGames)
rankings = reduce(lambda x, y: map(operator.add, x, y), res)
print '--------------------------------'
print 'Average rankings after {0} games'.format(numGames)
print '--------------------------------'
for player in xrange(numPlayers):
    print 'Player {0}: {1:.3}'.format(player, rankings[player]/float(numGames)),
