from collections import Counter
import multiprocessing as mp
import operator as op
import sys
import time

import agent
import cards
import game

class MaxNAgent(agent.Agent):

    """An agent that plays according to the Max-N algorithm for multiplayer
    games. (TODO: explain max-n more, as well as how we sampling cards)"""

    def makeMove(self, node):
        """Chooses a move by (TODO: explain max-n)

        :node: The current state from which we make a move.
        :returns: The (numCards, whichCard) action pair and the values of the
        node for each player.
        """
        allActions = self.getAllActions(node)
        # if there's only one option, just play that action
        if len(allActions) == 1:
            return allActions[0]

        # sample opponent hands on each trial and keep track of best actions in
        # each trial
        numTrials = 3
        # sample hands several times in parallel
        pool = mp.Pool(mp.cpu_count())
        start = time.time()
        inputs = [
            (trial, node, self.idx, self.hand) for trial in xrange(numTrials)
        ]
        bestActions = Counter(pool.map_async(simulate, inputs).get(sys.maxint))
        pool.close()
        pool.join()
        allBest = max(bestActions, key=bestActions.get)
        return allBest


def simulate(args):
    """Function to simulate the other players' cards randomly and play out the
    max^n tree based on those hands. Returns the best action.

    :trialNum: Trial number (for debugging and unique identification).
    :node: The current State object.
    :idx: The index of the current player.
    :hand: The current player's hand, which is known.
    :returns: The action tuple corresponding to the best action to take.
    """
    trialNum, node, idx, hand = args
    # subtract played cards and your own hand from cards remaining
    cardsLeft = cards.diff(cards.allCards(), [node.playedCards, hand])
    # get number of remaining cards for everyone else and deal hands
    withoutMe = list(node.numRemaining)
    del withoutMe[idx]
    hands = cards.dealHands(cardsLeft, withoutMe)
    # put my hand back in
    hands.insert(idx, hand)
    agents = map(lambda (i,h): MaxNAgent(i, h),
                 zip(xrange(node.numPlayers), hands))
    bestAct, bestVal = maxN(node, agents, 0, 2*node.numPlayers)
    return bestAct


def maxN(node, agents, d, maxDepth):
    """Returns best action and corresponding tuple as given by the max-n
    algorithm for the current node.

    :node: the current node.
    :returns: returns a tuple (bestAction, bestValue) where bestValue is a
    tuple of values (one for each player).
    """
    player = agents[node.whosTurn]
    if node.isFinalState():
        places = [5*node.numPlayers - node.finished.index(i)
                  for i in xrange(node.numPlayers)]
        return ((0, -1), places)
    # if at max depth, see which move minimizes cards remaining
    if d >= maxDepth:
        bestAct = (0, -1)
        bestVal = [heuristic(node, p) for p in agents]
        for act in player.getAllActions(node):
            child = node.getChild(act)
            childVal = [heuristic(node, p) for p in agents]
            if childVal[player.idx] > bestVal[player.idx]:
                bestAct = act
                bestVal = childVal
        return bestAct, bestVal
    # otherwise, continue to recurse down the tree
    bestAct = (0, -1)
    bestVal = tuple(-float('inf') for i in xrange(node.numPlayers))
    actions = player.getAllActions(node)
    for act in player.getAllActions(node):
        child = node.getChild(act)
        childAct, childVal = maxN(child, agents, d+1, maxDepth)
        if childVal[player.idx] > bestVal[player.idx]:
            bestAct = act
            bestVal = childVal
    return bestAct, bestVal


def heuristic(node, player):
    """A heuristic for when we reach maxDepth before reaching a final state.

    :node: The current node at which to evaluate.
    :player: The agent object for which we are evaluating the state.
    :returns: A float, with higher values representing better positions.
    """
    idx = player.idx
    numCardsPlayed = sum(node.playedCards[idx].itervalues())
    propCardsPlayed = float(numCardsPlayed) / node.initHandSize
    strengthPlayed = sum(k*v for k, v in node.playedCards[idx].iteritems())
    strengthRemaining = sum(k*v for k, v in player.hand.iteritems())
    initStrength = strengthPlayed + strengthRemaining
    propStrengthRemaining = float(strengthRemaining) / initStrength
    return propStrengthRemaining + 1.1*propCardsPlayed
