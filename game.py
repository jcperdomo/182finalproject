import collections
import numpy as np
import time

import agent
import cards
import state

class Game(object):

    """The class for the actual game, which is responsible for getting moves
    from players and organizing play."""

    def __init__(self, agents, hands=None, cardsPlayed=None, whosTurn=None):
        """Initializes the game with the agents listed as the players.

        :agents: Either a list of agent objects or a list of agent
        constructors. If constructors, the dealing and ID assignment will be
        done here; if objects, we simply assign the list to self.agents.
        :hands: list of hand dicts; if supplied, will be used as the hands for
        the agents.
        :cardsPlayed: list of played card dicts; if supplied, will be used for
        the cardsPlayed for the initialState.
        :whosTurn: index of agent whose turn it is; if supplied, the game will
        start with this player.
        """
        self.numPlayers = len(agents)
        if hands is None:
            deck = cards.allCards()
            hands = cards.dealHands(deck, 52/self.numPlayers)

        # if agents is a list of agent objects, set that to self.agents
        if isinstance(agents[0], agent.Agent):
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

        if cardsPlayed is None:
            cardsPlayed = [cards.noCards() for i in xrange(self.numPlayers)]

        self.initialState = state.State(cardsPlayed, whosTurn)

    def playGame(self, maxDepth=None, evalFunc=None):
        """Plays through the game, getting an action at each turn for each player.

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
            # make the move - take cards out of hand, update the state
            agentToMove.hand[whichCard] -= numCards
            # print state for inspection (DEBUGGING)
            #print curState.topCard, whosTurn, numCards, whichCard, map(lambda a: a.numCardsLeft(), self.agents)
            time.sleep(.2)
            # END DEBUGGING
            curState = curState.getChild((numCards, whichCard))

        # if whole game is played, return order of agent IDs from president to asshole
        if curState.isFinalState():
            results = list(curState.finished)
            # the game is over, append the asshole and return the results
            for p in xrange(self.numPlayers):
                if p not in results:
                    results.append(p)
                    break
        else:
            results = sorted(
                range(self.numPlayers),
                key=lambda idx: evalFunc(self.agents[idx]),
                reverse=True
            )

        return results
