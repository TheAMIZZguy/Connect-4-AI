import math

class MonteCarloNode:

    """
    Assumes that mirrored board states are already dealt with
    """
    def __init__(self, parent: 'MonteCarloNode' = None, board: list[list[int]] = None, possible_moves: dict[int] = None):

        self.board = board
        self.children = {}
        self.parents = set([parent] if parent else [])

        for move in possible_moves:
            self.children[move] = None
        
        # Recommended Move from Minimax
        self.recommended_move = -1
               
        # MonteCarlo stuff for determining UCB1 values
        self.games = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def GetChildNode(self, move):
        return self.children[move]

    # Expand the child play and return the new child node
    def Expand(self, play, childState, unexpandedPlays):
        if not (self.children[str(play)]): 
            raise Exception("No such Play")
            
        # create a new MonteCarloNode based on the play that was made
        childNode = MonteCarloNode(self, play, childState, unexpandedPlays)
        # since a new child node is being expanded, add the new child
        self.children[str(play)] = {"play": play, "node": childNode}
        return childNode
    
    # Gets the PossibleMoves of the node by searching for existing children
    def PossibleMoves(self):
        posMoves = []
        for child in self.children.values():
            posMoves.append(child['play'])     
        return posMoves
    
    # Gets the unexpanded moves of node
    def UnexpandedMoves(self):
        # Similar to Possible Moves, but only returns the unexpanded moves
        unexMoves = []
        for child in self.children.values():
            if not child['node']:
                unexMoves.append(child['play'])
        return unexMoves
    

    """
    If any children are None (unexpanded), it is not fully expanded
    """
    def IsFullyExpanded(self):
        for child in self.children.values():
            if not child['node']:
                return False
        return True

    def IsLeaf(self):
        return not self.children


    ### NOTE: Use only the specific parent implementation of the node itself
    # # UCB1 Value of node,
    # def UCB1Value(self, bias):
    #     # usually the bias parameter is 2
    #     # the higher the bias, the more it favours unexplored plays
    #     return (self.wins/self.games) + math.sqrt(bias* math.log(self.parent.games) / self.games)

  