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

    def isFinalState(self):
        """Returns True if all but the final player has finished, otherwise False.
        :returns: True if the game is over, False otherwise.
        """
        numDone = len(self.getDonePlayers())
        # if all but one have used all their cards, the game is over
        if numDone == self.numPlayers - 1:
            return True
        else:
            return False

    def getDonePlayers(self):
        """Returns list of player indices who have played all their cards.
        :returns: List of booleans corresponding to whether the player has
        cards remaining.
        """
        initHandSize = 52 / self.numPlayers
        cardsUsed = [sum(played.values()) == initHandSize
                     for played in self.playedCards]
        return [cu == initHandSize for cu in cardsUsed]
