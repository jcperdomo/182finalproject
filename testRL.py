import game, dummyAgent, rl
import operator
import matplotlib.pyplot as plt

numGames = 200
numEpisodes = 300
numPlayers = 4
gm = game.Game([rl.RLAgent] + [dummyAgent.DummyAgent for i in xrange(numPlayers - 1)])
#for agent in gm.agents:
    #print sum(k*v for k, v in agent.hand.items()),
    #print agent.hand
#print gm.playGame(verbose=True)
res = []
scores = []
for i in xrange(numEpisodes):
    curr = gm.playMultGames(superVerbose=False, n=numGames)
    scores.append(round(sum([r.index(0) for r in curr]) / float(numGames), 5))
    res += curr
    print 'Finishing episode {0} with scores of {1}'.format(gm.agents[0].episodes, map(lambda x: round(x/float(numGames), 3), [sum(r.index(p) for r in curr) for p in xrange(numPlayers)]))
    gm.agents[0].episodes += 1
rankings = [sum(r.index(p) for r in res) for p in xrange(numPlayers)]
print '--------------------------------'
print 'Average rankings after {0} episodes of {1} games'.format(numEpisodes, numGames)
print '--------------------------------'
for player in xrange(numPlayers):
        print 'Player {0}: {1:.5}'.format(player, rankings[player]/float(numGames * numEpisodes)),
print ""
#print gm.agents[0].q
lastEpisodes = 10
print '--------------------------------------------------'
print 'Average rankings in last {0} episodes of {1} games'.format(lastEpisodes, numGames)
print '--------------------------------------------------'
last = [sum(res[i].index(p) for i in range(len(res) - 1, len(res) - numGames * lastEpisodes - 1, -1)) for p in xrange(numPlayers)]
for player in xrange(numPlayers):
        print 'Player {0}: {1:.5}'.format(player, last[player]/float(numGames * lastEpisodes)),

plt.plot(scores)
plt.show()
