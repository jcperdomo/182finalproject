import game, dummyAgent
import operator

numGames = 200
numPlayers = 4
gm = game.Game([dummyAgent.DummyAgent for i in xrange(numPlayers)])
#for agent in gm.agents:
    #print sum(k*v for k, v in agent.hand.items()),
    #print agent.hand
#print gm.playGame(verbose=True)
res = gm.playMultGames(verbose=False, n=numGames)
rankings = [sum(r.index(p) for r in res) for p in xrange(numPlayers)]
print '--------------------------------'
print 'Average rankings after {0} games'.format(numGames)
print '--------------------------------'
for player in xrange(numPlayers):
        print 'Player {0}: {1:.5}'.format(player, rankings[player]/float(numGames)),
