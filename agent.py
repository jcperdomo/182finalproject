import abc

class Agent(object):
    __metaclass__ = abc.ABCMeta

    """The Agent base class to be overridden with each algorithm."""

    def __init__(self, hand):
        """Initializes an agent with its starting hand."""
        self.hand = hand

    @abc.abstractmethod
    def makeMove(self, state):
        """Returns the action to be made given a state.

        :state: The state from which the agent is making the move.
        :returns: A (numCards, whichCard) action. numCards == 0 represents no
        action (i.e., a pass).

        """
        actions = self.getAllActions(state)
        return actions[-1]

    def numCardsLeft(self):
        """Returns number of cards remaining in the hand.
        :returns: Number of cards left to be played.

        """
        return sum(self.hand.itervalues())

    def getAllActions(self, state):
        """Returns list of all legal actions given a state.

        :state: The state from which we are considering actions. Must have
        whosTurn of the current agent.
        :returns: A list of (numCards, whichCard) actions.

        """
        # corner case: player is out of cards, so return a pass
        if self.numCardsLeft() == 0:
            return [(0, 0)]

        allPossiblePlays = [
            (numCards, card)
            for card, num in self.hand.iteritems()
            for numCards in xrange(1, num+1)
        ]
        filterFunc = lambda (n,c): (n == state.topCard[0] and
                                    c > state.topCard[1])
        if state.topCard is None:
            return allPossiblePlays
        else:
            return  [(0, 0)] + filter(filterFunc, allPossiblePlays)
