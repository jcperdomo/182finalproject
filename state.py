from copy import deepcopy

class State(object):

    """Docstring for State. """

    def __init__(self, playedCards, whosTurn,
                 topCard=None, lastPlayed=None, finished=[]):
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
        self.finished = finished

        # compute numRemaining
        initHandSize = 52 / self.numPlayers
        self.numRemaining = [initHandSize - sum(played.itervalues())
                             for played in playedCards]

    def getChild(self, action):
        """Gets the next state given an action.

        :action: The action taken, represented as (numCards, whichCard).
        :returns: The next state.
        """
        numCards, whichCard = action
        # set defaults
        nextPlayedCards = deepcopy(self.playedCards)
        nextWhosTurn = (self.whosTurn + 1) % self.numPlayers
        nextTopCard = self.topCard
        nextLastPlayed = self.lastPlayed
        nextFinished = self.finished
        # if a real move was made, update next state
        if numCards:
            nextPlayedCards[self.whosTurn][whichCard] += numCards
            nextTopCard = action
            nextLastPlayed = self.whosTurn
        # if no move was made and it's gone all the way around, clear deck
        elif nextWhosTurn == nextLastPlayed:
            nextTopCard = None
            nextLastPlayed = None
        # if player ran out of cards at this transition, add to finished list
        initHandSize = 52 / self.numPlayers
        if sum(nextPlayedCards[self.whosTurn].itervalues()) == initHandSize:
            nextFinished.append(self.whosTurn)
        nextState = State(nextPlayedCards, nextWhosTurn,
                          nextTopCard, nextLastPlayed, nextFinished)
        return nextState

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
        :returns: List of player indices who are out of cards.
        """
        initHandSize = 52 / self.numPlayers
        usedAll = [sum(played.values()) == initHandSize
                     for played in self.playedCards]
        return [i for i, ua in enumerate(usedAll) if ua]
