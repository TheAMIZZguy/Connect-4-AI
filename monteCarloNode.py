import math

class MonteCarloNode():
    
    def __init__(self, parent, play, state, possibleMoves):
        
        # Info unique to this node
        self.play = play
        self.state = state
        
        # Info for the tree
        self.parent = parent
        self.children = {}
        
        # all children have possible move and their own child nodes
        # and all child nodes are unexpanded at the start, hence none
        # note that possibleMoves are also unexpanded at creation
        for move in possibleMoves:           
            self.children[str(move)] = {"play": move, "node": None}
        
        # Memory for Victor Moves
        self.recommendedMove = -1
               
        # MonteCarlo stuff for determining node
        self.games = 0
        self.wins = 0.0
              
            
    # Gets the node corresponding to the given play
    def ChildNode(self, play): 
        child = self.children[str(play)]
        if not child:
            raise Exception("No such Move")
        elif child['node'] == None:
            raise Exception('Child not expanded')
            
        return child['node']

    # Expand the child play and return the new child node
    def Expand(self, play, childState, unexpandedPlays):
        if not (self.children[str(play)]): 
            raise Exception("No such Play")
            
        # create a new MonteCarloNode based on the play that was made
        childNode = MonteCarloNode(self, play, childState, unexpandedPlays)
        # since a new child node is being expanded, add the new child
        self.children[str(play)] = {"play": play, "node": childNode}
        return childNode
    
    # Gets the PossibleMoves of the node
    def PossibleMoves(self):
        posMoves = []
        #self explanitory, get the possible moves from self.child and return
        for child in self.children.values():
            posMoves.append(child['play'])     
        return posMoves
    
    # Gets the unexpanded moves of node
    def UnexpandedMoves(self):
        #Similar to Possible Moves, but only returns the unexpanded moves
        unexMoves = []
        for child in self.children.values():
            if not child['node']:
                unexMoves.append(child['play'])
        return unexMoves
    
    # See if is a fully expaned node
    def IsFullyExpanded(self):
        #If any children are None (unexpanded), it is not fully expanded
        for child in self.children.values():
            if not child['node']:
                return False
        return True
    
    # If the node is a Leaf Node
    def IsLeaf(self):
        # return bool
        if not self.children:
            return True
        return False
    
    # UCB1 Value of node,
    def UCB1Value(self, bias):
        # usually the bias parameter is 2
        # the higher the bias, the more it favours unexplored plays
        return (self.wins/self.games) + math.sqrt(bias* math.log(self.parent.games) / self.games)

  