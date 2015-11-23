import collections
import numpy as np

import cards
import state

class Game(object):

    """The class for the actual game, which is responsible for getting moves
    from players and organizing play."""

    def __init__(self, agentFuncs):
        """Initializes the game with the agents listed as the players. Supports
        games of sizes 4-6 (for now).

        :agentFuncs: List of agent constructors that will be used to construct
        the players.

        """
        self.agentFuncs = agentFuncs
        self.numPlayers = len(agentFuncs)
    
    def playGame(self):
        """Plays through the game, getting an action at each turn for each player.
        :returns: A ranking of the agent indices from president to asshole.

        """
        deck = cards.allCards()
        hands = cards.dealHands(deck, 52/4)
        agents = [agentConstructor(hand)
                  for agentConstructor, hand in zip(self.agentFuncs, hands)]
        
        # randomly choose a player with a 3 to start
        # (proportional to how many 3's they have)
        threes = collections.Counter()
        for p, hand in enumerate(hands):
            threes[p] += hand[0]
        initWhosTurn = np.random.choice(cards.cardDictToList(threes))
        initCardsPlayed = [cards.noCards() for i in xrange(self.numPlayers)]
        initialState = state.State(initCardsPlayed, initWhosTurn, None, None)
        curState = initialState
        results = []

        # play out the game
        while not curState.isFinalState():

            # figure out whose turn it is
            whosTurn = curState.whosTurn
            agentToMove = agents[whosTurn]
            
            # if this player played the last card, clear the deck

            # get the move - ask agent for move
            (numCards, whichCard) = agentToMove.makeMove(curState)
            print curState.topCard, curState.lastPlayed, whosTurn, numCards, whichCard, min(map(len, curState.playedCards))
            # make the move - take cards out of hand, update the state
            agentToMove.hand[whichCard] -= numCards
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
