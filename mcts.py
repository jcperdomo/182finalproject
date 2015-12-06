import state
import agent
import random
import game
import dummyAgent
import cards
import time, sys
from math import sqrt, log

# constant used to gauge level of exploration in node selection
c = 1/sqrt(2)
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
                topCard=None, lastPlayed=None, finished=[], parent = None, score=0.):
        """
        lastMove =  action from parent Node, None for the root node
        children =  list of all child nodes

        """
        self.lastMove = lastMove
        self.visits = 0.
        self.score = score
        self.terminal = cards.empty(hand)
        self.children = []
        self.parent  = parent
        self.hand = hand
        self.idx = idx
        self.turn = (self.idx ==  whosTurn)
        super(mctsNode, self).__init__(playedCards, whosTurn,
                     topCard=None, lastPlayed=None, finished=[])
        # need a super statement for the agent id MISSING

    # adds a particular child to a node
    def addChild(self, action):
        # get successor state from state module
        state = self.getChild(action)
        # update, curent hand and append child node
        newHand = self.hand
        if self.turn:
            newHand = cards.diff(self.hand, {action[1]: action[0]})
        score = 0.
        if self.idx in state.finished:
            #print "finished list ", state.finished
            score = (state.finished.index(self.idx) + 1) ** -1
        #print "Node Content:"
        newNode = mctsNode(state.playedCards, state.whosTurn,
                            newHand, self.idx, action, state.topCard,
                            state.lastPlayed, state.finished, self, score)
        #print newNode is None
        self.children.append(newNode)

    # adds all children to a node
    def addAllChildren(self):
        curr_state = state.State(self.playedCards, self.whosTurn, self.topCard,
                                self.lastPlayed, self.finished)
        if self.turn:
            hand = self.hand
        else:
            hands = cards.dealHands(cards.diff(cards.allCards(),
                curr_state.playedCards), curr_state.numRemaining)
            hand = hands[curr_state.whosTurn]

        player = agent.Agent(curr_state.whosTurn, hand)
        poss_actions = player.getAllActions(curr_state)
        for action in poss_actions:
            #count += 1
            self.addChild(action)
        #print "number of children added ", count
#todo what do you do if the tree is completely expanded, or if all the children are terminal nodes
#what happens with selection

class mctsAgent(agent.Agent):

    def __init__(self, idx, hand):
        super(mctsAgent, self).__init__(idx, hand)


    # given a list of nodes, returns best child according to UCT algorithm
    def bestChild(self, children):
        # added 1 to prevent division by 0 errors
        sorted_children = sorted(children, key = lambda child: child.score/(child.visits + 1)
                                + c * sqrt(log(child.parent.visits)/(child.visits + 1)))
        # return best child
        return sorted_children[-1]

    # returns node selected by tree policy
    def selection(self, root):
        if root.children == []:
            root.addAllChildren()
            #print "num children", len(root.children)
            selected_child = random.choice(root.children)
            #print "Selected child is NONE in selection ", selected_child is None
            return selected_child
        else:
            #print "num childrenss", len(root.children)
            #for i in root.children:
            #    print i is None
            return self.selection(self.bestChild(root.children))

    # expands all children for a node
    def expansion(self, node):
        #print "before num kids: ", len(node.children)
        #print  "without adding children", node.children
        node.addAllChildren()
        #print "after num kids: ", len(node.children)
        #print "having added all children", node.children
        #for i in range(len(node.children)):
        #    print isinstance(node.children[i], mctsNode)
        #for i in node.children:
        #    print "type el: ", type(i)
        #    print "node is instance: ", isinstance(i, mctsNode)
        # if all the nodes are terminal then ...
        # if node.children == []:
        print  "exited expansion"
        res  = random.choice(node.children)
        print res
        return res

    # given a node, plays out game using the default policy returning a score for the node
    def simulation(self, node):
        # dummy agents to play the remaining games quickly
        #print "Entered simulation in MCTS"
        #print node
        #print "node is instance: ", isinstance(node, mctsNode)
        start = time.time()
        if node.terminal:
            return node.score
        cardsLeft = cards.diff(cards.allCards(), [node.playedCards, node.hand])
        otherRemaining = list(node.numRemaining)
        #print otherRemaining
        del otherRemaining[node.idx]
        #print self.idx
        #print otherRemaining
        hands = cards.dealHands(cardsLeft , otherRemaining)
        hands.insert(node.idx, node.hand)
        agents = [dummyAgent.DummyAgent for i in xrange(node.numPlayers)]
        gm = game.Game(agents, hands, node.playedCards, node.whosTurn,
                       node.topCard, node.lastPlayed, node.finished)
        results = gm.playGame()
        end = time.time() - start
        #print "time in simulation", end
        return (results.index(self.idx) + 1) ** -1


    # updates all nodes up to the root based on result of simulation
    def backpropagation(self, node, result):
        #print "entered backpropagation"
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
        #            topCard=None, lastPlayed=None, finished=[], parent = None, score=0.):
        root = mctsNode(state.playedCards, state.whosTurn, self.hand, self.idx,
                        None, state.topCard, state.lastPlayed, state.finished)
        loop_count = 0
        while time.time() < time_start + time_end:
            loop_count += 1
            #print "looped"
            nextNode = self.selection(root)
            #print "type of selected node is NONE in Make move", nextNode is None
            #print "next node ", nextNode.numRemaining
            result = self.simulation(nextNode)
            #print  "exited simulation2"
            self.backpropagation(nextNode, result)
            #print "exited backpropagation stage"
        #print "EXITED LOOP", loop_count
        bestKid = sorted(root.children, key = lambda child: child.score)[-1]
        return bestKid.lastMove
