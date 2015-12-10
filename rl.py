from collections import Counter
import multiprocessing as mp
import operator as op
import sys, time, random
import cards, agent

class RLAgent(agent.Agent):

    """An agent that plays according to the Paranoid algorithm for multiplayer
    games."""

    def __init__(self, idx, hand):
        """Initialization for the Dummy Agent."""
        super(RLAgent, self).__init__(idx, hand)
        self.q = Counter()
        #self.epsilon=0.05
        self.discount=0.9
        self.alpha=0.4
        self.episodes = 1

    def getQValue(self, state, action):
        """
        Returns Q(state,action)
        Should return 0.0 if we have never seen a state
        or the Q node value otherwise
        """
        reducedState = reduceState(state)
        return self.q[(reducedState, action)]

    def computeValueFromQValues(self, state):
        """
        Returns max_action Q(state,action)
        where the max is over legal actions.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.
        """
        acts = []
        possActs = self.getAllActions(state)
        if len(possActs) == 0:
            return 0.0
        for a in possActs:
            acts.append(self.getQValue(state, a))
        return max(acts)

    def computeActionFromQValues(self, state):
        """
        Compute the best action to take in a state.  Note that if there
        are no legal actions, which is the case at the terminal state,
        you should return None.
        """
        acts = []
        possActs = self.getAllActions(state)
        if len(possActs) == 0:
            return (0, -1)
        for a in possActs:
            acts.append((a, self.getQValue(state, a)))
        return max(acts,key=op.itemgetter(1))[0]

    def getAction(self, state):
        """
        Compute the action to take in the current state.  With
        probability self.epsilon, we take a random action and
        take the best policy action otherwise.
        """
        possActions = self.getAllActions(state)
        if len(possActions) == 0:
            return (0, -1)
        r = random.random()
        if r > (30 / float(self.episodes)):
            r2 = random.random()
            if r2 > 0.5:
                if state.topCard == None:
                    return min(possActions, key=op.itemgetter(1))
                else:
                    numToPlay = max(map(op.itemgetter(0), possActions))
                    choices = filter(lambda (n,c): n == numToPlay, possActions)
                    return min(choices, key=op.itemgetter(1))
            else:
                return random.choice(possActions)
        else:
            return self.computeActionFromQValues(state)

    def update(self, state, action, nextState, reward):
        """
        The parent class calls this to observe a
        state = action => nextState and reward transition.
        You should do your Q-Value update here
        """
        reducedState = reduceState(state)
        q = self.getQValue(state, action)
        delta = reward -  q
        possActs = self.getAllActions(nextState)
        if len(possActs) == 0:
            self.q[(reducedState,action)] = q + self.alpha * delta
            return
        bestAct = self.getQValue(nextState, possActs[0])
        for aprime in possActs:
            bestAct = max(bestAct, (self.getQValue(nextState, aprime)))
        delta += self.discount * bestAct
        self.q[(reducedState, action)] = q + self.alpha * delta
        #print self.q

    def makeMove(self, state):
        act = self.getAction(state)
        nextState = state.getChild(act)
        player = state.whosTurn
#        oldNum = state.numRemaining[player]
        newNum = nextState.numRemaining[player]
        if newNum == 0:
            ratio = 1 /float(len(nextState.finished))
            reward = ratio * 20
        else:
            reward = 0
        self.update(state, act, nextState, reward) 
        return act

def reduceState(state):
    player = state.whosTurn
    numTwos = 0
    highest = 0
    high = 0
    med = 0
    low = 0
    score = 0
    for entry in state.playedCards:
#        low += entry[0] + entry[1] + entry[2]
#        med += entry[3] + entry[4] + entry[5]
#        high += entry[5] + entry[7] + entry[8]
        highest += entry[9] + entry[10] + entry[11]
        numTwos += entry[12]
        #score += (state.playedCards[0][entry] * entry)
    return (numTwos, state.numRemaining[player], state.numRemaining[player] - min(state.numRemaining))
