import state
import agent
import random
import game
import dummyAgent
import cards
import time, sys
from math import sqrt, log

# constant used to gauge level of exploration in node selection
exploration_c = 1/sqrt(2)
"""
    Monte Carlo Tree Search:





"""

class mctsNode(state.State, agent.Agent):
"""
    Class for game tree for MCTS
    lastMove = action taken from parent node
    visits = number of times node has been expanded
    score = sum of results based on simulations
    parent = parent node
    hand = current hand

"""
    def __init__(self, playedCards, whosTurn,
                 topCard=None, lastPlayed=None, finished=[], lastMove, parent = None, hand, terminal):
    """
        lastMove =  action from parent Node, None for the root node
        children =  list of all child nodes

    """
        self.lastMove = lastMove
        self.visits = 0.
        self.score = 0.
        if terminal:
            self.score = sys.maxint
        self.children = []
        self.parent  = parent
        self.hand = hand
        super(mctsNode, self).__init__(playedCards, whosTurn,
                     topCard=None, lastPlayed=None, finished=[])

    # adds a particular child to a node
    def addChild(self, action):
        # get successor state from state module
        state = self.getChild(action)
        terminal = False
        if state.isFinalState():
            terminal = True
        # update, curent hand and append child node
        newHand = cards.diff(self.hand, {action[1]: action[0]})
        self.children.append(mctsNode(state.playedCards, state.whosTurn, state.topCard,
            state.lastPlayed, state.finished, action, self, newHand, terminal))

    # adds all children to a node
    def addAllChildren(self):
        poss_actions = self.getAllActions()
        for action in poss_actions:
            self.addChild(action)
#TODO what do you do if the tree is completely expanded, or if all the children are terminal nodes
#what happens with selection

class mctsAgent(agent.Agent):

    def __init__(self, idx, hand):
        super(mctsAgent, self).__init__(idx, hand)

    # given a list of nodes, returns best child according to UCT algorithm
    def bestChild(children):
        # added 1 to prevent division by 0 errors
        sorted_children = sorted(children, key = lambda child: child.score/child.visits + c * sqrt(log(child.parent.visits)/(child.visits + 1)))
        # return best child
        return sorted_children[-1]

    # returns node selected by tree policy
    def selection(root):
        if root.children == []:
            self.expansion(root)
        else:
            self.selection(self.bestChild(root.children))

    # expands all children for a node
    def expansion(node):
        node.addAllChildren()
        # if all the nodes are terminal then ...
        # if node.children == []:
        return random.choice(node.children)

    # given a node, plays out game using the default policy returning a score for the node
    def simulation(node):
        # dummy agents to play the remaining games quickly

        cardsLeft = cards.diff(cards.allCards, [node.cardsPlayed, node.hand])
        otherRemaining = list(node.numRemaining)
        del otherRemaining[self.idx]
        hands = cards.dealHands(cardsLeft , otherRemaining)
        hands.insert(self.idx, node.hand)
        agents = [dummyAgent.DummyAgent] * node.numPlayers
        game = game.Game(agents, hands, node.playedCards, node.whosTurn)
        results = game.playGame()
        return results.index(self.idx)


    # updates all nodes up to the root based on result of simulation
    def backpropagation(node, result):
        node.visits += 1
        node.score += result
        if node.parent == None:
            return
        else:
            self.backpropagation(node.parent,result)

    def makeMove(self, state):
        time_start = time.time()
        time_end  = 5
        root = mctsNode(state.playedCards, state.whosTurn,
                     state.topCard, state.lastPlayed, state.finished, None, self.hand)
        while time.time() < time_start + time_end:
            nextNode = self.selection(root)
            result = self.simulation(node)
            self.backpropagation(nextNode, result)

        bestKid = sorted(root.children, key = lambda child: child.score)[-1]
        return bestKid.lastMove
