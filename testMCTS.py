import mcts
import cards
import state
import dummyAgent
import game
"""
NP = 5

hands  = cards.dealHands(cards.allCards(), [5 for i in xrange(NP)])

print
testState  = state.State([cards.noCards() for i in xrange(NP)], 0)
agent  = mcts.mctsAgent(0, hands[0])
printHand = cards.cardDictToList(agent.hand)
printHand = map(lambda c: cards.cardRepr[c], printHand)
#print "Agent Hand:", printHand

print "Chosen Move: ", agent.makeMove(testState)"""

gm = game.Game([mcts.mctsAgent] + [dummyAgent.DummyAgent for i in xrange(4)])
for agent in gm.agents:
    print sum(k*v for k, v in agent.hand.items()),
    print agent.hand
print gm.playGame(verbose = True)