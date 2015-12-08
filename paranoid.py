from collections import Counter
import multiprocessing as mp
import operator as op
import sys, time
import cards, agent

class ParanoidAgent(agent.Agent):

    """An agent that plays according to the Paranoid algorithm for multiplayer
    games."""

    def __init__(self, idx, hand):
        """Initialization for the Dummy Agent."""
        super(ParanoidAgent, self).__init__(idx, hand)
        self.nodeList = []

    def makeMove(self, state):
        allActions = self.getAllActions(state)
        # if there's only one option, just play that action
        if len(allActions) == 1:
            return allActions[0]

        """
        # sample opponent hands on each trial and keep track of best actions in
        # each trial
        numTrials = 5
        # sample hands several times in parallel
        pool = mp.Pool(numTrials)
        start = time.time()
        inputs = [
        (trial, state, self.idx, self.hand) for trial in xrange(numTrials)
        ]
        bestActions = Counter(pool.map_async(simulate, inputs).get(sys.maxint))
        pool.close()
        pool.join()
        allBest = max(bestActions, key=bestActions.get)
        print allBest, bestActions, '{} seconds'.format(time.time() - start)
        return allBest
        """

        start = time.time()
        args = (0, state, self.idx, self.hand)
        res, nodes = simulate(args)
        #print res, (time.time() - start)
        self.nodeList.append(nodes)
        return res

nodesExpanded = 0

def simulate(args):
    """Function to simulate the other players' cards randomly and play out the
    paranoid game tree based on those hands. Returns the best action.
    """
    global nodesExpanded
    trial, state, index, hand = args
    # subtract played cards and your own hand from cards remaining
    cardsLeft = cards.diff(cards.allCards(), [state.playedCards, hand])
    # get number of remaining cards for everyone else and deal hands
    withoutMe = list(state.numRemaining)
    del withoutMe[index]
    hands = cards.dealHands(cardsLeft, withoutMe)
    # put my hand back in
    hands.insert(index, hand)
    agents = map(lambda (i,h): ParanoidAgent(i, h),
                 zip(xrange(state.numPlayers), hands))
    res = paranoid(state, 1, agents, -(sys.maxint -1), sys.maxint)
    return res[0], nodesExpanded


def paranoid (state, depth, agents, a, b):
    global nodesExpanded
    act = (0, -1)
    player = agents[state.whosTurn]
    nodesExpanded += 1
    if state.isFinalState():
        heu = state.heuristic()
        # Assume all players are playing against the max agent
        return a, heu[0] - sum(heu[1:])

    if depth >= 2:
        bestVal = [heuristic(state, p) for p in agents]
        for action in player.getAllActions(state):
            child = state.getChild(action)
            childVal = [heuristic(state, p) for p in agents]
            if childVal[player.idx] > bestVal[player.idx]:
                act = action
                bestVal = childVal
        return act, bestVal[0] - sum(bestVal[1:])

    # The max player
    if state.whosTurn == 0:
        v = -(sys.maxint - 1)
        for action in player.getAllActions(state):
            nextState = state.getChild(action)
            val = paranoid(nextState, depth, agents, a, b)[1]
            if val > v:
                v = val
                act = action
            if v > b:
                return (action, v)
            a = max(a, v)

    # A min player
    if state.whosTurn != 0:
        v = sys.maxint
        if player.idx == (state.numPlayers - 1):
            depth += 1
        for action in player.getAllActions(state):
            nextState = state.getChild(action)
            val = paranoid(nextState, depth, agents, a, b)[1]
            if val < v:
                v = val
                act = action
            if v < a:
                return (action, v)
            b = min(b, v)
    return act, v

def heuristic(state, player):
    """A heuristic for when we reach maxDepth before reaching a final state.

    :node: The current node at which to evaluate.
    :player: The agent object for which we are evaluating the state.
    :returns: A float, with higher values representing better positions.
    """
    idx = player.idx
    numCardsPlayed = sum(state.playedCards[idx].itervalues())
    propCardsPlayed = float(numCardsPlayed) / state.initHandSize
    strengthPlayed = sum(k*v for k, v in state.playedCards[idx].iteritems())
    strengthRemaining = sum(k*v for k, v in player.hand.iteritems())
    initStrength = strengthPlayed + strengthRemaining
    propStrengthRemaining = float(strengthRemaining) / initStrength
    return propStrengthRemaining + propCardsPlayed
