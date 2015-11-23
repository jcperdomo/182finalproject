from collections import Counter
import operator as op
import time

import agent
import cards
import game

class MaxNAgent(agent.Agent):

    """An agent that plays according to the Max-N algorithm for multiplayer
    games. (TODO: explain max-n more, as well as how we sampling cards)"""

    def __init__(self, idx, hand):
        """Initialization for the Dummy Agent."""
        super(MaxNAgent, self).__init__(idx, hand)

    def makeMove(self, state):
        """Chooses a move by (TODO: explain max-n)

        :state: The current state from which we make a move.
        :returns: The (numCards, whichCard) action pair and the values of the
        node for each player.
        """
        allActions = self.getAllActions(state)
        if len(allActions) == 1:
            return allActions[0]
        totalPlayed = sum(sum(played.values()) for played in state.playedCards)
        bestActions = Counter()
        # subtract played cards and your own hand from cards remaining
        cardsLeft = cards.allCards()
        for played in state.playedCards:
            cardsLeft = cards.diff(cardsLeft, played)
        cardsLeft = cards.diff(cardsLeft, self.hand)

        # sample opponent hands
        print 'trialing', state.topCard, self.hand
        initHandSize = 52 / state.numPlayers
        for trial in xrange(25):
            print 'trial', trial
            hands = cards.dealHands(
                cardsLeft, 
                [ 
                    initHandSize - sum(played.itervalues())
                    for i, played in enumerate(state.playedCards) 
                    if i != self.idx # don't give hand for current player
                ]
            )
            hands.insert(self.idx, self.hand)
            agents = map(lambda (i,h): MaxNAgent(i, h),
                         zip(xrange(state.numPlayers), hands))
            bestAct, bestVals = maxN(state, self, agents, 0, state.numPlayers*2)
            bestActions[bestAct] += 1
        
        # get most frequent best action and return
        allBest = max(bestActions, key=bestActions.get)
        print allBest, bestActions
        return allBest


def maxN(state, player, agents, d, maxDepth):
    numPlayers = len(agents)
    # returns act, val
    allActions = player.getAllActions(state)
    if d > maxDepth:
        # heuristic - take action that maximizes cards played
        bestAct = None
        bestVals = [-float('inf') for p in xrange(numPlayers)]
        for possAct in allActions:
            child = state.getChild(possAct)
            cardsPlayed = [sum(played.itervalues())
                           for played in state.playedCards]
            if cardsPlayed[player.idx] > bestVals[player.idx]:
                bestAct = possAct
                bestVals = cardsPlayed
        return bestAct, bestVals
    if state.isFinalState():
        assert sum(player.hand.values()) == 0
        return (0, 0), [numPlayers - state.finished.index(player) 
                        if player in state.finished else numPlayers - 1
                        for player in xrange(numPlayers)]
    bestAct = None
    bestVals = [-float('inf') for i in xrange(numPlayers)]
    for possAct in allActions:
        numCards, whichCard = possAct
        child = state.getChild(possAct)
        nextPlayer = agents[child.whosTurn]
        nextAllActions = nextPlayer.getAllActions(child)
        hisBestAct, hisVals = maxN(child, nextPlayer, agents, d+1, maxDepth)
        if hisVals[player.idx] > bestVals[player.idx]:
            bestVals = hisVals
            bestAct = possAct

    return bestAct, bestVals
