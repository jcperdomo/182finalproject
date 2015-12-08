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
    def __init__(self, playedCards, whosTurn, hands, idx, lastMove,
                topCard=None, lastPlayed=None, finished=[], parent = None, score=0.):
        """
        lastMove =  action from parent Node, None for the root node
        children =  list of all child nodes
        visits  =  number of time node has been visited
        whosTurn =  id of player to move
        hands =  list of hand dictionaries for each player
        idx = idx of agent
        t

        """
        self.lastMove = lastMove
        self.visits = 0.
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
            #print "PASS action top card should be the same", newState.topCard
        else:
            #print "didn't pass", action, newState.topCard
            player_hand  = dict(self.hands[self.whosTurn])
            new_hand = cards.diff(player_hand, {action[1]: action[0]})
            newHands = list(self.hands)
            newHands[self.whosTurn] = new_hand
        score = 0.

        if self.idx in newState.finished:
            score = (newState.finished.index(self.idx) + 1) ** -1
        newNode = mctsNode(newState.playedCards, newState.whosTurn,
                            newHands, self.idx, action, newState.topCard,
                            newState.lastPlayed, newState.finished, self, score)
        self.children.append(newNode)

    # adds all children to a node
    def addAllChildren(self, actions):
        for action in actions:
            self.addChild(action)


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
    """
        every node in the tree, has the hand of the agent, but when you make moves you make them based on the actions
        of whos turn it is,

        therefore, you need to keep track of the hands of all the player everytime in order to correctly
        calculate the children for each node, each node needs a list of the current hand for each player
        probably will update the simulation thing at that point at that point




    """
    # returns node selected by tree policy
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
                #print "hand at current node", root.hands[root.whosTurn]
                #print "top card", root.topCard, THIS IS RIGHT
                #print "actions", actions
                root.addAllChildren(actions)
                selected_child = random.choice(root.children)
                return selected_child
        else:
            return self.selection(self.bestChild(root.children))


    # given a node, plays out game using the default policy returning a score for the node
    def simulation(self, node):
        start = time.time()
        # if agent's hand is empty return score
        if cards.empty(node.hands[self.idx]):
            return node.score
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
        time_end  = 1
        cardsLeft = cards.diff(cards.allCards(), [state.playedCards, self.hand])
        otherRemaining = list(state.numRemaining)
        del otherRemaining[self.idx]
        hands = cards.dealHands(cardsLeft , otherRemaining)
        hands.insert(self.idx, dict(self.hand))
        root = mctsNode(state.playedCards, self.idx, hands, self.idx,
                        None, state.topCard, state.lastPlayed, state.finished)
        if root.terminal:
            #print self.hand
            print self.idx in state.finished
            #print "thinks state is terminal"
            return agent.PASS
        loop_count = 0

        while time.time() < time_start + time_end:
            loop_count += 1
            nextNode = self.selection(root)
            result = self.simulation(nextNode)
            #print "exited simulation"
            self.backpropagation(nextNode, result)
        #print "number of loops", loop_count
        bestKid = sorted(root.children, key = lambda child: child.score)[-1]
        #print "possible actions: ", self.getAllActions(state)
        #print "actions at children", [child.lastMove for child in root.children]
        #print "chosen action", bestKid.lastMove
        print state.numRemaining
        return bestKid.lastMove
