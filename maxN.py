from collections import Counter
import operator as op
import time

import agent
import cards
import game

class MaxNAgent(agent.Agent):

    """An agent that plays according to the Max-N algorithm for multiplayer
    games. (TODO: explain max-n more, as well as how we sampling cards)"""

    def makeMove(self, state):
        """Chooses a move by (TODO: explain max-n)

        :state: The current state from which we make a move.
        :returns: The (numCards, whichCard) action pair and the values of the
        node for each player.
        """
        # if it's an initial state, you have to play your 3's
        if state.isInitialState():
            numThrees = self.hand[0]
            return (numThrees, 0)
        allActions = self.getAllActions(state)
        # if there's only one option, just play that action (it's a pass)
        if len(allActions) == 1:
            return allActions[0]
        # subtract played cards and your own hand from cards remaining
        cardsLeft = cards.diff(cards.allCards(), [state.playedCards,self.hand])

        # sample opponent hands on each trial and keep track of best actions in
        # each trial
        bestActions = Counter()
        print '{} possible actions'.format(len(allActions))
        start = time.time()
        for trial in xrange(5):
            print 'trial', trial
            # get number of remaining cards for everyone else and deal hands
            withoutMe = list(state.numRemaining)
            del withoutMe[self.idx]
            hands = cards.dealHands(cardsLeft, withoutMe)
            # put my hand back in
            hands.insert(self.idx, self.hand)
            agents = map(lambda (i,h): MaxNAgent(i, h),
                         zip(xrange(state.numPlayers), hands))
            bestAct, bestVal = maxN(state, agents, 0, 2*state.numPlayers)
            bestActions[bestAct] += 1
        
        # get most frequent best action and return
        allBest = max(bestActions, key=bestActions.get)
        print allBest, bestActions, '{} seconds'.format(time.time() - start)
        return allBest


def maxN(node, agents, d, maxDepth):
    """Returns best action and corresponding tuple as given by the max-n
    algorithm for the current node.

    :node: the current node.
    :returns: returns a tuple (bestAction, bestValue) where bestValue is a
    tuple of values (one for each player).
    """
    player = agents[node.whosTurn]
    if node.isFinalState():
        places = [node.finished.index(i) for i in xrange(node.numPlayers)]
        return ((0, -1), places)
    # if at max depth, see which move minimizes cards remaining
    # TODO: improve the heuristic
    if d >= maxDepth:
        bestAct = (0, -1)
        bestVal = [-nc for nc in node.numRemaining]
        for act in player.getAllActions(node):
            child = node.getChild(act)
            childVal = [-nc for nc in child.numRemaining]
            if childVal[player.idx] > bestVal[player.idx]:
                bestAct = act
                bestVal = childVal
        return bestAct, bestVal
    # otherwise, continue to recurse down the tree
    bestAct = (0, -1)
    bestVal = tuple(-float('inf') for i in xrange(node.numPlayers))
    for act in player.getAllActions(node):
        child = node.getChild(act)
        childAct, childVal = maxN(child, agents, d+1, maxDepth)
        if childVal[player.idx] > bestVal[player.idx]:
            bestAct = act
            bestVal = childVal
    return bestAct, bestVal
