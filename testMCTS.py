import mcts
import cards
import state
import dummyAgent
import game
import operator

"""
hands = [{0: 1, 1: 0, 2: 1, 3: 1, 4: 0, 5: 1, 6: 0, 7: 0, 8: 2, 9: 0, 10: 1, 11: 0, 12: 3},
{0: 0, 1: 0, 2: 1, 3: 0, 4: 0, 5: 1, 6: 2, 7: 2, 8: 2, 9: 1, 10: 0, 11: 0, 12: 1},
{0: 1, 1: 0, 2: 1, 3: 1, 4: 3, 5: 1, 6: 1, 7: 0, 8: 0, 9: 0, 10: 0, 11: 2, 12: 0},
{0: 2, 1: 1, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 2, 8: 0, 9: 2, 10: 2, 11: 1, 12: 0},
{0: 0, 1: 3, 2: 1, 3: 2, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0, 9: 1, 10: 1, 11: 1, 12: 0}]

gm = game.Game([mcts.mctsAgent] + [dummyAgent.DummyAgent for i in xrange(4)])
for agent in gm.agents:
    print sum(k*v for k, v in agent.hand.items()),
    print agent.hand
print gm.playGame(verbose = True)
"""
numGames = 30
numPlayers = 4
gm = game.Game([mcts.mctsAgent] + [dummyAgent.DummyAgent for i in xrange(numPlayers - 1)])
res = gm.playMultGames(verbose=False, n=numGames)
print '-------------------------------------------'
#print 'Average nodes expanded after {0} games: {1:.5}'.format(numGames, sum(gm.agents[0].nodeList) / float(numGames))
rankings = [sum(r.index(p) for r in res) for p in xrange(numPlayers)]
print '--------------------------------'
print 'Average rankings after {0} games'.format(numGames)
print '--------------------------------'
for player in xrange(numPlayers):
    print 'Player {0}: {1:.5}'.format(player, rankings[player]/float(numGames)),
