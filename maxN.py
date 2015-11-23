import agent
import operator as op

class MaxNAgent(agent.Agent):

    """An agent that plays according to the Max-N algorithm for multiplayer
    games. (TODO: explain max-n more, as well as how we sampling cards)"""

    def __init__(self, hand):
        """Initialization for the Dummy Agent."""
        super(MaxNAgent, self).__init__(hand)

    def makeMove(self, state):
        """Chooses a move by (TODO: explain max-n)

        :state: The current state from which we make a move.
        :returns: The (numCards, whichCard) action pair.
        """
        allActions = self.getAllActions(state)
        raise 'Not yet implemented'
