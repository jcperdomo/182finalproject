import state
import agent
import random
import game
import dummyAgent
import cards
import time, sys
from collections import Counter
from math import sqrt, log

# constant used to gauge level of exploration in node selection
c = 10

# time (in seconds) MCTS is allowed to round
budget = 1

"""
    Monte Carlo Tree Search:

    Includes modules for game tree as well as the agent class



"""

class mctsNode(state.State):
    """
    Class for game tree for MCTS

    lastMove = action taken from parent node
    visits = number of times node has been expanded
    score = sum of results based on simulations
    parent = parent node
    hands = list of hand dictionaries for each player at that point based on sampling
    depth = depth of node in the tree, used for testing purposes
    idx = idx of agent
    whosTurn =  id of player to move

    """

    def __init__(self, playedCards, whosTurn, hands, idx, lastMove, depth,
                topCard=None, lastPlayed=None, finished=[], parent = None, score=0.):

        self.lastMove = lastMove
        self.depth = depth
        self.visits = 1.
        self.score = score
        self.children = []
        self.parent  = parent
        self.hands = hands
        self.idx = idx
        self.terminal = cards.empty(hands[self.idx])
        self.turn = (self.idx == whosTurn)
        super(mctsNode, self).__init__(playedCards, whosTurn,
                     topCard, lastPlayed, finished)

    # adds a particular child to a node
    def addChild(self, action):
        # get successor state from state module
        curr_state = state.State(self.playedCards, self.whosTurn,
                            self.topCard, self.lastPlayed, self.finished)
        newState = curr_state.getChild(action)
        if action == agent.PASS:
            newHands = list(self.hands)
        else:
            player_hand  = dict(self.hands[self.whosTurn])
            new_hand = cards.diff(player_hand, {action[1]: action[0]})
            newHands = list(self.hands)
            newHands[self.whosTurn] = new_hand
        score = 0.
        # if agent got rid of cards, initialize score to finishing position
        if self.idx in newState.finished:
            score = (newState.finished.index(self.idx) + 1) ** -1
        newNode = mctsNode(newState.playedCards, newState.whosTurn, newHands,
                            self.idx, action, self.depth + 1, newState.topCard,
                            newState.lastPlayed, newState.finished, self, score)
        self.children.append(newNode)

    # adds all children to a node
    def addAllChildren(self, actions):
        for action in actions:
            self.addChild(action)
"""

    Agent Class for MCTS agent. Contains functions for each major stage of the
    algorithm.


"""

class mctsAgent(agent.Agent):

    def __init__(self, idx, hand):
        super(mctsAgent, self).__init__(idx, hand)


    # given a list of nodes, returns best child according to UCT algorithm
    def bestChild(self, children):
        sorted_children = sorted(children, key = lambda child: child.score / child.visits
                                + c * sqrt(log(child.parent.visits)/(child.visits + 1)))
        # return best child
        return sorted_children[-1]


    # returns node selected by tree policy, includes the expansion of the tree
    def selection(self, root):
        numDone = len(root.finished)
        if root.children == []:
            # player to play has no cards, but game isn't finished
            if (not root.turn) and cards.empty(root.hands[root.whosTurn]) and root.numPlayers > numDone:
                root.addChild(agent.PASS)
                return self.selection(root.children[0])
            elif (root.turn and root.terminal) or root.isFinalState():
                return root
            else:
                curr_state = state.State(root.playedCards, root.whosTurn,
                                root.topCard, root.lastPlayed, root.finished)
                testagent = agent.Agent(root.whosTurn, root.hands[root.whosTurn])
                actions = testagent.getAllActions(curr_state)
                root.addAllChildren(actions)
                selected_child = random.choice(root.children)
                return selected_child
        else:
            return self.selection(self.bestChild(root.children))

    """
        given a node, plays out game using the default policy returning a
        (normalized) score for that node
    """
    def simulation(self, node):
        #start = time.time()
        # if agent's hand is empty return score
        if cards.empty(node.hands[self.idx]):
            return node.score / node.visits
        else:
            count = 0
            for i in range(node.numPlayers):
                if cards.empty(node.hands[i]):
                    count += 1
            if count == node.numPlayers - 1:
                return (node.numPlayers + 1) ** -1
            agents = [dummyAgent.DummyAgent for i in xrange(node.numPlayers)]
            gm = game.Game(agents, node.hands, node.playedCards, node.whosTurn,
                           node.topCard, node.lastPlayed, node.finished)
            results = gm.playGame()
            #end = time.time() - start
            #print "time in simulation", end
            return ((results.index(self.idx) + 1) ** -1) / node.visits


    # updates all nodes up to the root based on result of simulation
    def backpropagation(self, node, result):
        node.visits += 1
        node.score += result
        if node.parent == None:
            return
        else:
            self.backpropagation(node.parent,result)

    def makeMove(self, state):
        # if there is just 1 action (PASS), avoid the comptutation
        actions = self.getAllActions(state)
        res_actions = []
        if len(actions) == 1:
            #print  actions[0]
            return actions[0]
        # do the sampling x times, then pick most common action
        x = 10
        for i in xrange(x):
            time_start = time.time()
            cardsLeft = cards.diff(cards.allCards(), [state.playedCards, self.hand])
            otherRemaining = list(state.numRemaining)
            del otherRemaining[self.idx]
            hands = cards.dealHands(cardsLeft , otherRemaining)
            hands.insert(self.idx, dict(self.hand))
            root = mctsNode(state.playedCards, self.idx, hands, self.idx,
                            None, 0, state.topCard, state.lastPlayed, state.finished)
            loop_count = 0
            while time.time() < time_start + budget:
                loop_count += 1
                nextNode = self.selection(root)
                result = self.simulation(nextNode)
                self.backpropagation(nextNode, result)
            #print "number of loops", loop_count, used for testing
            sorted_children  = sorted(root.children, key = lambda child: child.score/child.visits)
            res_actions.append(sorted_children[-1].lastMove)
        numActions = Counter(res_actions).most_common()
        return numActions[0][0]
