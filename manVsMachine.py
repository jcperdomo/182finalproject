import copy

import game
import humanAgent, maxN, dummyAgent

gm = game.Game([humanAgent.HumanAgent] +
               [maxN.MaxNAgent for i in xrange(3)], verbose=True)
origHands = [copy.deepcopy(agent.hand) for agent in gm.agents]
print gm.playGame()
print 'Original hands and strengths:'
for hand in origHands:
    print sum(k*v for k, v in hand.items()),
    print hand
