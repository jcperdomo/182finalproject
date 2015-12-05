import operator as op

PASS = (0, -1)

class Agent(object):

    """The Agent base class to be overridden with each algorithm."""

    def __init__(self, idx, hand):
        """Initializes an agent with its starting hand."""
        self.idx = idx
        self.hand = hand

    def firstMove(self):
        """Plays all 3's (0's in the card encoding) for the first move of the
        game.
        :returns: (numThrees, 0)

        """
        numThrees = self.hand[0]
        return (numThrees, 0)

    def makeMove(self, node):
        """Returns the action to be made given a node.

        :node: The node from which the agent is making the move.
        :returns: A (numCards, whichCard) action. numCards == 0 represents no
        action (i.e., a pass).

        """
        raise "not yet defined"

    def numCardsLeft(self):
        """Returns number of cards remaining in the hand.
        :returns: Number of cards left to be played.

        """
        return sum(self.hand.itervalues())

    def getAllActions(self, node):
        """Returns list of all legal actions given a node.

        :node: The node from which we are considering actions. Must have
        whosTurn of the current agent.
        :returns: A list of (numCards, whichCard) actions.

        """
        # corner case: player is out of cards, so return a pass
        if self.numCardsLeft() == 0:
            return [PASS]
        # corner case: if it's the initial state, return all 3's
        if node.isInitialState():
            return [self.firstMove()]

        allPossiblePlays = {
            (numCards, card)
            for card, num in self.hand.iteritems()
            for numCards in xrange(1, num+1)
        }
        allPossiblePlays = sorted(allPossiblePlays, key=lambda (n,c): (c,-n))
        filterFunc = lambda (n,c): (n == node.topCard[0] and
                                    c > node.topCard[1])
        if node.topCard is None:
            return allPossiblePlays
        else:
            return  [PASS] + filter(filterFunc, allPossiblePlays)
