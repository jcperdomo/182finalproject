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

class mctsNode(state.State):
    """
    Class for game tree for MCTS
    lastMove = action taken from parent node
    visits = number of times node has been expanded
    score = sum of results based on simulations
    parent = parent node
    hand = current hand

    """
    # remove Agent inheritance just use state
    def __init__(self, playedCards, whosTurn, hand, idx, lastMove,
                topCard=None, lastPlayed=None, finished=[], parent = None):
        """
        lastMove =  action from parent Node, None for the root node
        children =  list of all child nodes

        """
        self.lastMove = lastMove
        self.visits = 0.
        self.score = 0.
        self.terminal = cards.empty(hand)
        self.children = []
        self.parent  = parent
        self.hand = hand
        self.idx = idx
        super(mctsNode, self).__init__(playedCards, whosTurn,
                     topCard=None, lastPlayed=None, finished=[])
        # need a super statement for the agent id MISSING

    # adds a particular child to a node
    def addChild(self, action):
        # get successor state from state module
        state = self.getChild(action)

        # update, curent hand and append child node
        newHand = cards.diff(self.hand, {action[1]: action[0]})
        if cards.empty(newHand):
            # missing the definition of self.idx
            # need to flip score since president is first on the list
            # score for terminal nodes is equal to the position in
            score =  state.finished.index(self.idx) ** -1

        self.children.append(mctsNode(state.playedCards, state.whosTurn,
                            newHand, self.idx, action, state.topCard,
                            state.lastPlayed, state.finished, self))

    # adds all children to a node
    def addAllChildren(self):
        curr_state = state.State(self.playedCards, self.whosTurn, self.topCard,
                                self.lastPlayed, self.finished)
        #print self.hand
        player = agent.Agent(self.idx, self.hand)
        poss_actions = player.getAllActions(curr_state)
        for action in poss_actions:
            self.addChild(action)
#todo what do you do if the tree is completely expanded, or if all the children are terminal nodes
#what happens with selection

class mctsAgent(agent.Agent):

    def __init__(self, idx, hand):
        super(mctsAgent, self).__init__(idx, hand)


    # given a list of nodes, returns best child according to UCT algorithm
    def bestChild(self, children):
        # added 1 to prevent division by 0 errors
        sorted_children = sorted(children, key = lambda child: child.score/child.visits + c * sqrt(log(child.parent.visits)/(child.visits + 1)))
        # return best child
        return sorted_children[-1]

    # returns node selected by tree policy
    def selection(self, root):
        if root.children == []:
            return self.expansion(root)
        else:
            self.selection(self.bestChild(root.children))

    # expands all children for a node
    def expansion(self, node):
        node.addAllChildren()
        # if all the nodes are terminal then ...
        # if node.children == []:
        return random.choice(node.children)

    # given a node, plays out game using the default policy returning a score for the node
    def simulation(self, node):
        # dummy agents to play the remaining games quickly
        print "Entered simulation in MCTS"
        start = time.time()
        if node.terminal:
            return node.score
        cardsLeft = cards.diff(cards.allCards(), [node.playedCards, node.hand])
        otherRemaining = list(node.numRemaining)
        del otherRemaining[self.idx]
        hands = cards.dealHands(cardsLeft , otherRemaining)
        hands.insert(self.idx, node.hand)
        print "MCTS agent hands: ", hands
        agents = [dummyAgent.DummyAgent for i in xrange(node.numPlayers)]
        gm = game.Game(agents, hands, node.playedCards, node.whosTurn,
                       node.topCard, node.lastPlayed, node.finished)
        results = gm.playGame()
        end = time.time() - start
        print "time in simulation", end
        return results.index(self.idx) ** -1


    # updates all nodes up to the root based on result of simulation
    def backpropagation(self, node, result):
        print "entered backpropagation"
        node.visits += 1
        node.score += result
        if node.parent == None:
            return
        else:
            self.backpropagation(node.parent,result)

    def makeMove(self, state):
        time_start = time.time()
        time_end  = 2
        #def __init__(self, playedCards, whosTurn, hand, idx, lastMove,
        #            topCard=None, lastPlayed=None, finished=[], parent = None):
        root = mctsNode(state.playedCards, state.whosTurn, self.hand, self.idx,
                        None, state.topCard, state.lastPlayed, state.finished,
                        None)
        while time.time() < time_start + time_end:
            print "looped"
            nextNode = self.selection(root)
            result = self.simulation(nextNode)
            self.backpropagation(nextNode, result)
        print "Exited loop"
        bestKid = sorted(root.children, key = lambda child: child.score)[-1]
        return bestKid.lastMove
