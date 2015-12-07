import collections
import numpy as np
import time

import agent
import cards
import state

class Game(object):

    """The class for the actual game, which is responsible for getting moves
    from players and organizing play."""

    def __init__(self, agents, hands=None, playedCards=None, whosTurn=None,
                 topCard=None, lastPlayed=None, finished=[]):
        """Initializes the game with the agents listed as the players.

        :agents: Either a list of agent objects or a list of agent
        constructors. If constructors, the dealing and ID assignment will be
        done here; if objects, we simply assign the list to self.agents.
        :hands: list of hand dicts; if supplied, will be used as the hands for
        the agents.
        :playedCards: list of played card dicts; if supplied, will be used for
        the playedCards for the initialState.
        :whosTurn: index of agent whose turn it is; if supplied, the game will
        start with this player.

        topCard, lastPlayed, and finished are all parameters passed on to the
        initial state; for more information, see state.State's __init__.
        """
        self.numPlayers = len(agents)
        if hands is None:
            deck = cards.allCards()
            hands = cards.dealHands(deck, 52/self.numPlayers)

        # if agents is a list of agent objects, set that to self.agents
        if all(isinstance(a, agent.Agent) for a in agents):
            self.agents = agents
        # otherwise, construct the agents from the list of agent constructors
        else:
            self.agents = [agentConstructor(i, hand)
                      for i, (agentConstructor,hand) in
                      enumerate(zip(agents, hands))]

        if whosTurn is None:
            # randomly choose a player with a 3 to start
            # (proportional to how many 3's they have)
            threes = collections.Counter()
            for p, hand in enumerate(hands):
                threes[p] += hand[0]
            whosTurn = np.random.choice(cards.cardDictToList(threes))

        if playedCards is None:
            playedCards = [cards.noCards() for i in xrange(self.numPlayers)]

        self.initialState = state.State(playedCards, whosTurn, topCard,
                                        lastPlayed, finished)

    def newGame(self, ordering):
        deck = cards.allCards()
        hands = cards.dealHands(deck, 52/self.numPlayers)
        for i in xrange(self.numPlayers):
            self.agents[i].hand = hands[i]
        # swap cards
        for i in xrange(2):
            high = ordering.index(i)
            low = ordering.index(self.numPlayers - i - 1)
            cards.swapCards(hands[high], hands[low], 2 - i)

        threes = collections.Counter()
        for p, hand in enumerate(hands):
            threes[p] += hand[0]
        whosTurn = np.random.choice(cards.cardDictToList(threes))
        playedCards = [cards.noCards() for i in xrange(self.numPlayers)]
        self.initialState = state.State(playedCards, whosTurn, None, None, [])

    def playGame(self, verbose=False, maxDepth=None, evalFunc=None):
        """Plays through the game, getting an action at each turn for each player.

        :verbose: If True, playGame will print each move made by each player.
        :maxDepth: depth to which (i.e., number of turns) the game will be
        played; if None, play whole game.
        :evalFunc: see :returns:.

        :returns: A ranking of the agent indices from president to asshole. If
        the game is terminated early by the depth parameter, returns ranking of
        agent indices based on evalFunc, which takes in an agent object and
        returns a number (for which *higher* is better).
        """
        curState = self.initialState

        # play out the game
        curDepth = 0
        maxDepth = float('inf') if maxDepth is None else maxDepth
        while not curState.isFinalState() and curDepth < maxDepth:
            curDepth += 1
            # figure out whose turn it is
            whosTurn = curState.whosTurn
            agentToMove = self.agents[whosTurn]
            # get the move - ask agent for move
            (numCards, whichCard) = agentToMove.makeMove(curState)
            if verbose:
                print whosTurn, numCards, cards.cardRepr[whichCard]
            # make the move by taking cards out of hand, if not a pass
            if numCards > 0:
                agentToMove.hand[whichCard] -= numCards
            # update the state
            curState = curState.getChild((numCards, whichCard))

        # if whole game is played, return order of agent IDs from president to asshole
        if curState.isFinalState():
            results = list(curState.finished)
        else:
            results = sorted(
                range(self.numPlayers),
                key=lambda idx: evalFunc(self.agents[idx]),
                reverse=True
            )

        return results

    def playMultGames(self, verbose=False, maxDepth=None, evalFunc=None, n=1):
        """Plays n full games
        """
        results = []
        for i in xrange(n):
           res = self.playGame(verbose, maxDepth, evalFunc)
           results.append(res)
           print res
           self.newGame(res)
        return results
