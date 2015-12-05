import copy

import game
import humanAgent, maxN, dummyAgent

gm = game.Game([humanAgent.HumanAgent] + [maxN.MaxNAgent for i in xrange(3)])
origHands = [copy.deepcopy(agent.hand) for agent in gm.agents]
print 'Your hand:', origHands[0]
print gm.playGame(verbose=True)
print 'Original hands and strengths:'
for hand in origHands:
    print sum(k*v for k, v in hand.items()),
    print hand
