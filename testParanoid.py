import game, paranoid, dummyAgent
import operator

numGames = 50
numPlayers = 4
gm = game.Game([paranoid.ParanoidAgent] + [dummyAgent.DummyAgent for i in xrange(numPlayers - 1)])
#for agent in gm.agents:
#    print sum(k*v for k, v in agent.hand.items()),
#    print agent.hand
#print gm.playGame(verbose=True)
#print gm.agents[0].nodeList
res = gm.playMultGames(verbose=True, n=numGames)
print '-------------------------------------------'
print 'Average nodes expanded after {0} games: {1:.5}'.format(numGames, sum(gm.agents[0].nodeList) / float(numGames))
rankings = reduce(lambda x, y: map(operator.add, x, y), res)
print '--------------------------------'
print 'Average rankings after {0} games'.format(numGames)
print '--------------------------------'
for player in xrange(numPlayers):
    print 'Player {0}: {1:.5}'.format(player, rankings[player]/float(numGames)),

