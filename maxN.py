from collections import Counter
import operator as op

import agent
import cards

class MaxNAgent(agent.Agent):

    """An agent that plays according to the Max-N algorithm for multiplayer
    games. (TODO: explain max-n more, as well as how we sampling cards)"""

    def __init__(self, idx, hand):
        """Initialization for the Dummy Agent."""
        super(MaxNAgent, self).__init__(idx, hand)

    def makeMove(self, state):
        """Chooses a move by (TODO: explain max-n)

        :state: The current state from which we make a move.
        :returns: The (numCards, whichCard) action pair.
        """
        bestAction = Counter()
        allActions = self.getAllActions(state)
        cardsLeft = cards.allCards()
        for played in state.playedCards:
            cardsLeft = cards.diff(cardsLeft, played)
        cardsLeft = cards.diff(cardsLeft, self.hand)
        initHandSize = 52 / state.numPlayers
        for trial in xrange(100):
            hands = cards.dealHands(
                cardsLeft, 
                [ 
                    initHandSize - sum(played.itervalues())
                    for i, played in enumerate(state.playedCards) 
                    if i != self.idx
                ]
            )
            hands.insert(self.idx, self.hand)
            # now `hands` holds the current players' hands; do the trial now
            # using perfect information max-N
            # ...
            best = allActions[-1]
            bestAction[best] += 1
        
        # get most frequent best action and return
        allBest = max(bestAction, key=bestAction.get)
        return allBest
