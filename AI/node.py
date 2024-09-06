import math


class Node:

    """
    Assumes that mirrored board states are already dealt with
    """
    def __init__(self, parent: 'Node' = None, board: list[list[int]] = None, possible_moves: dict[int] = None,
                 heuristic_score: int = None, miniMax_score: int = None, is_fully_expanded : bool = False, depth_search: int = 0):

        self.board = board
        self.children = {}
        self.parents = set([parent] if parent else [])
        self.is_fully_expanded = is_fully_expanded

        for move in possible_moves:
            self.children[move] = None
        
        # Recommended Move from Minimax
        self.recommended_move = -1
               
        # MonteCarlo stuff for determining UCB1 values
        self.games = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0

        # MiniMax stuff for going down the tree
        self.heuristic_score = heuristic_score  # This is the actual heuristic score
        self.miniMax_score = miniMax_score  # This gets updated from the minimax algo
        self.depth_search = depth_search  # How deep has been fully searched from this node

    def GetChildNode(self, move):
        return self.children[move]

    @staticmethod
    def LoadNode(hash):
        with h5py.File('current_game.hdf5', 'r') as f:
            node_copy = f['default']

    # TODO update
    # Expand the child play and return the new child node
    def Expand(self, play, childState, unexpandedPlays):
        if not (self.children[str(play)]): 
            raise Exception("No such Play")
            
        # create a new MonteCarloNode based on the play that was made
        childNode = Node(self, play, childState, unexpandedPlays)
        # since a new child node is being expanded, add the new child
        self.children[str(play)] = {"play": play, "node": childNode}
        return childNode

    # TODO update
    # Gets the PossibleMoves of the node by searching for existing children
    def PossibleMoves(self):
        posMoves = []
        for child in self.children.values():
            posMoves.append(child['play'])     
        return posMoves

    # TODO update
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
    """ # TODO update
    def IsFullyExpanded(self):
        for child in self.children.values():
            if not child['node']:
                return False
        return True

    # TODO update
    def FindRecommendedMove(self):
        if not self.IsFullyExpanded():
            Exception("Is not Fully Expanded")
        posMoves = []
        for child in self.children.values():
            posMoves.append(child['play'])
        return posMoves

    def IsLeaf(self):
        return not self.children


    ### NOTE: Use only the specific parent implementation of the node itself
    # # UCB1 Value of node,
    # def UCB1Value(self, bias):
    #     # usually the bias parameter is 2
    #     # the higher the bias, the more it favours unexplored plays
    #     return (self.wins/self.games) + math.sqrt(bias* math.log(self.parent.games) / self.games)

  