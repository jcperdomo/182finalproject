from copy import deepcopy
import cards

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
        :finished: list of player indices who have played all their cards in
        order from president to asshole.
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
        nextFinished = deepcopy(self.finished)
        # if a real move was made, update next state
        if numCards > 0:
            nextPlayedCards[self.whosTurn][whichCard] += numCards
            nextTopCard = action
            nextLastPlayed = self.whosTurn
        # if no move was made and it's gone all the way around, clear deck
        elif nextWhosTurn == nextLastPlayed:
            nextTopCard = None
            nextLastPlayed = None
        # create next state
        nextState = State(nextPlayedCards, nextWhosTurn,
                          nextTopCard, nextLastPlayed, nextFinished)
        # if player ran out of cards at this transition, add to finished list
        if (self.numRemaining[self.whosTurn] > 0 and
                nextState.numRemaining[self.whosTurn] == 0):
            nextState.finished.append(self.whosTurn)
        return nextState

    def isFinalState(self):
        """Returns True if all but the final player has finished, otherwise False.
        :returns: True if the game is over, False otherwise.
        """
        numDone = len(self.finished)
        # if all but one have used all their cards, the game is over
        if numDone >= self.numPlayers:
            return True
        else:
            return False

    def isInitialState(self):
        """Returns True if this is the first play of the game, i.e., all
        playedCards entries are empty.
        :returns: True if it's the first play of the game, False otherwise.

        """
        return all(cards.empty(played) for played in self.playedCards)
