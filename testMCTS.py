import mcts
import cards
import state

hands  = cards.dealHands(cards.allCards(), [5]* 5)

print "Agent Hand: ", hands[0]

print
testState  = state.State([cards.noCards()] * 5, 0)
agent  = mcts.mctsAgent(0, hands[0])
#print agent.hand

print "Chosen Move: ", agent.makeMove(testState)
