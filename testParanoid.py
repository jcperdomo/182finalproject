import game, paranoid, dummyAgent
import operator

numGames = 20
numPlayers = 4
gm = game.Game([dummyAgent.DummyAgent, paranoid.ParanoidAgent] + [dummyAgent.DummyAgent for i in xrange(numPlayers - 2)])
#for agent in gm.agents:
#    print sum(k*v for k, v in agent.hand.items()),
#    print agent.hand
#print gm.playGame(verbose=True)
#print gm.agents[0].nodeList
res = gm.playMultGames(verbose=True, n=numGames)
print '-------------------------------------------'
#print 'Average nodes expanded after {0} games: {1:.5}'.format(numGames, sum(gm.agents[0].nodeList) / float(numGames))
rankings = [sum(r.index(p) for r in res) for p in xrange(numPlayers)]
print '--------------------------------'
print 'Average rankings after {0} games'.format(numGames)
print '--------------------------------'
for player in xrange(numPlayers):
    print 'Player {0}: {1:.5}'.format(player, rankings[player]/float(numGames)),

