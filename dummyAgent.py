import agent
import operator as op

class DummyAgent(agent.Agent):

    """An agent that simply plays as many cards as it can while playing the
    lowest possible value within that number of cards being played."""

    def __init__(self, idx, hand):
        """Initialization for the Dummy Agent."""
        super(DummyAgent, self).__init__(idx, hand)

    def makeMove(self, state):
        """Chooses a move by first figuring out the most possible moves it
        could play, then picking the one wth the smallest number.

        :state: The current state from which we make a move.
        :returns: The (numCards, whichCard) action pair.
        """
        if state.isInitialState():
            return self.firstMove()
        allActions = self.getAllActions(state)
        mostPossible = max(map(op.itemgetter(0), allActions))
        choices = filter(lambda (n,c): n == mostPossible, allActions)
        return min(choices, key=op.itemgetter(1))
