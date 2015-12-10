import game, dummyAgent, rl
import operator

numGames = 200
numEpisodes = 500
numPlayers = 4
gm = game.Game([rl.RLAgent] + [dummyAgent.DummyAgent for i in xrange(numPlayers - 1)])
#for agent in gm.agents:
    #print sum(k*v for k, v in agent.hand.items()),
    #print agent.hand
#print gm.playGame(verbose=True)
res = []
for i in xrange(numEpisodes):
    curr = gm.playMultGames(superVerbose=False, n=numGames)
    res += curr
    print 'Finishing episode {0} with scores of {1}'.format(gm.agents[0].episodes, map(lambda x: round(x/float(numGames), 3), reduce(lambda x, y: map(operator.add, x, y), curr)))
    gm.agents[0].episodes += 1
rankings = reduce(lambda x, y: map(operator.add, x, y), res)
print '--------------------------------'
print 'Average rankings after {0} episodes of {1} games'.format(numEpisodes, numGames)
print '--------------------------------'
for player in xrange(numPlayers):
        print 'Player {0}: {1:.5}'.format(player, rankings[player]/float(numGames * numEpisodes)),
print ""
print gm.agents[0].q
lastEpisodes = 10
print '--------------------------------------------------'
print 'Average rankings in last {0} episodes of {1} games'.format(lastEpisodes, numGames)
print '--------------------------------------------------'
last = [0] * numPlayers
for i in range(len(res) - 1, len(res) - numGames * lastEpisodes - 1, -1):
    last = map(operator.add, res[i], last)
for player in xrange(numPlayers):
        print 'Player {0}: {1:.5}'.format(player, last[player]/float(numGames * lastEpisodes)),

