import agent
import cards

class HumanAgent(agent.Agent):

    """An agent that asks the user for input from the command line each time it
    is his/her turn."""

    def __init__(self, idx, hand):
        """Initialization for the human agent, which requires nothing more than
        the agent.Agent base class."""
        super(HumanAgent, self).__init__(idx, hand)

    def makeMove(self, node):
        """The makeMove method that overrides the agent base class's makeMove;
        simply asks the user to input a valid action.

        :node: The current state at which we're moving.
        :returns: A (numCards, whichCard) tuple representing the action.
        """
        if self.idx in node.finished:
            print ('Congratulations, you\'re out of cards and were number {} '
                   'to finish!'.format(node.finished.index(self.idx)+1))
            return (0, -1)

        print 'Cards left for each player: {}'.format(node.numRemaining)
        print 'Your hand: {}'.format(
            map(lambda c: cards.cardRepr[c], cards.cardDictToList(self.hand))
        )
        if node.topCard:
            topN, topC = node.topCard
            topStr = '{} {}'.format(topN, cards.cardRepr[topC])
        else:
            topStr = 'Empty'
        print 'Top card: {}'.format(topStr)
        legalActions = self.getAllActions(node)
        print 'Valid actions: {}'.format(
            ['{} {}'.format(n, cards.cardRepr[c]) for n, c in legalActions]
        )
        action = None
        while action not in legalActions:
            actStr = raw_input(
                'Your move. Input as a space-separated tuple of numCards and '
                'whichCard representing the action (that is, '
                '"numCards whichCard" without the quotes). To pass, enter '
                '"0 P", "P", or "pass". So, what\'s your move? '
            )
            if actStr.lower() in ('pass', 'p', '0p'):
                action = (0, -1)
            else:
                try:
                    numStr, cardStr = actStr.split()
                    numCards = int(numStr)
                    encodedNum = cards.cardRepr.index(cardStr.upper())
                except Exception:
                    continue
                # if number not valid, continue the loop again
                if encodedNum == -1:
                    continue
                whichCard = int(encodedNum)
                action = (numCards, whichCard)
        return action
