import mcts
import cards
import state

hands  = cards.dealHands(cards.allCards(), [5]* 5)

print
testState  = state.State([cards.noCards()] * 5, 0)
agent  = mcts.mctsAgent(0, hands[0])
printHand = cards.cardDictToList(agent.hand)
printHand = map(lambda c: cards.cardRepr[c], printHand)
print "Agent Hand:", printHand

print "Chosen Move: ", agent.makeMove(testState)
