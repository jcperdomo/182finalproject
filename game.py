import collections
import numpy as np
import time

import cards
import state

class Game(object):

    """The class for the actual game, which is responsible for getting moves
    from players and organizing play."""

    def __init__(self, agentFuncs):
        """Initializes the game with the agents listed as the players.

        :agentFuncs: List of agent constructors that will be used to construct
        the players.

        """
        deck = cards.allCards()
        hands = cards.dealHands(deck, 52/self.numPlayers)
        self.agents = [agentConstructor(i, hand)
                  for i, (agentConstructor,hand) in 
                  enumerate(zip(agentFuncs, hands))]
        self.numPlayers = len(self.agents)
        
        # randomly choose a player with a 3 to start
        # (proportional to how many 3's they have)
        threes = collections.Counter()
        for p, hand in enumerate(hands):
            threes[p] += hand[0]
        whosTurn = np.random.choice(cards.cardDictToList(threes))
        cardsPlayed = [cards.noCards() for i in xrange(self.numPlayers)]
        self.initialState = state.State(cardsPlayed, whosTurn, None, None)
    
    def playGame(self):
        """Plays through the game, getting an action at each turn for each player.
        :returns: A ranking of the agent indices from president to asshole.

        """
        curState = self.initialState
        results = []

        # play out the game
        while not curState.isFinalState():

            # figure out whose turn it is
            whosTurn = curState.whosTurn
            agentToMove = self.agents[whosTurn]
            # get the move - ask agent for move
            (numCards, whichCard) = agentToMove.makeMove(curState)
            # make the move - take cards out of hand, update the state
            agentToMove.hand[whichCard] -= numCards
            # print state for inspection (DEBUGGING)
            print curState.topCard, whosTurn, numCards, whichCard, map(lambda a: a.numCardsLeft(), self.agents)
            time.sleep(.2)
            # END DEBUGGING
            curState = curState.getChild((numCards, whichCard))

            # update results
            for p in curState.getDonePlayers():
                if p not in results:
                    results.append(p)
        
        # the game is over, append the asshole and return the results
        for p in xrange(self.numPlayers):
            if p not in results:
                results.append(p)
                break

        return results
