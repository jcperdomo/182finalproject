import cards, dummyAgent, maxN, paranoid, mcts, state
from collections import Counter

cs = cards.allCards()

hand = Counter({0: 1, 5: 1, 7: 1, 10: 1, 12: 1})
playedCards = [
    {c: 1 for c in xrange(13)} for i in xrange(3)
] + [cards.noCards() for i in xrange(0)]

node = state.State(
    whosTurn=0,
    playedCards=playedCards,
    topCard = (1, 4),
)

dummy = dummyAgent.DummyAgent(0, hand)
maxn = maxN.MaxNAgent(0, hand)
para = paranoid.ParanoidAgent(0, hand)
mct = mcts.mctsAgent(0, hand)

readablehand = Counter({cards.cardRepr[k]: v for k, v in hand.iteritems()})
print 'Given hand:', readablehand
dumMove = list(dummy.makeMove(node))
dumMove[1] = cards.cardRepr[dumMove[1]]
movestr = lambda m: 'Play {} {}'.format(m[0], m[1])
print 'Initial move chosen by dummy:', movestr(dumMove)
maxMove = list(maxn.makeMove(node))
maxMove[1] = cards.cardRepr[maxMove[1]]
print 'Initial move chosen by max^n:', movestr(maxMove)
paraMove = list(para.makeMove(node))
paraMove[1] = cards.cardRepr[paraMove[1]]
print 'Initial move chosen by paranoid:', movestr(paraMove)
