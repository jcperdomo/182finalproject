from copy import deepcopy

class State(object):

    """Docstring for State. """

    def __init__(self, playedCards, whosTurn, topCard, lastPlayed):
        """Initialization for State.

        :playedCards: list of card count dictionaries representing how many of
        each card each player has played.
        :whosTurn: Index of player whose turn it is.
        :topCard: (numPlayed, whichCard) of the last play (None if empty deck).
        :lastPlayed: Last player who played on this deck (None if empty deck).
        """
        self.playedCards = playedCards
        self.numPlayers = len(self.playedCards)
        self.whosTurn = whosTurn
        self.topCard = topCard
        self.lastPlayed = lastPlayed

    def getChild(self, action):
        """Gets the next state given an action.

        :action: The action taken, represented as (numCards, whichCard).
        :returns: The next state.
        """
        numCards, whichCard = action
        nextPlayedCards = deepcopy(self.playedCards)
        nextWhosTurn = (self.whosTurn + 1) % self.numPlayers
        nextTopCard = self.topCard
        nextLastPlayed = self.lastPlayed
        if numCards:
            # a real move was made
            nextPlayedCards[self.whosTurn][whichCard] += numCards
            nextTopCard = action
            nextLastPlayed = self.whosTurn
        elif nextWhosTurn == nextLastPlayed:
            nextTopCard = None
            nextLastPlayed = None
        return State(nextPlayedCards, nextWhosTurn,
                     nextTopCard, nextLastPlayed)
