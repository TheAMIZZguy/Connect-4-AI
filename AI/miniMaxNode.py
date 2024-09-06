class MiniMaxNode:

    """
    Assumes that mirrored board states are already dealt with
    """
    def __init__(self, parent: 'MiniMaxNode' = None, board: list[list[int]] = None, possible_moves: dict[int] = None):

        self.board = board
        self.children = {}
        self.parents = set([parent] if parent else [])

        for move in possible_moves:
            self.children[move] = None

        self.score = None  # TODO calculate score immediately here or pass it down in constructor
        self.mini_score = None  # pass it down or use it as a node, above is from score function, this is from actual minimax
