import random
import math
from node import Node
from game import Game
from cache import GetNode, SaveNode, CreateNewNode


# Constants
COLUMN_COUNT = 7
ROW_COUNT = 6
PLAYER1 = 1
PLAYER2 = 2
EMPTY = 0

# Heuristics Values
WINDOW_LENGTH = 4
CENTER_SCORE = 3
FOUR_SCORE = math.inf
THREE_SCORE = 5
TWO_SCORE = 2
ENEMY_THREE_SCORE = 4


class MiniMax:

    # Assuming we start at the first turn
    def __init__(self, game, use_database=False):
        self.game = game
        self.db_path = "current_game.db"
        if use_database:
            self.db_path = "database.db"

        self.current_node = CreateNewNode(board=self.game.board, parent=None, possible_moves=self.game.possible_moves, current_player=1, db_path=self.db_path)


    """
    Returns: node_score via MiniMax
    """
    def DepthSearch(self, node, depth, alpha, beta):
        possible_moves = node.possible_moves.keys()
        is_terminal = Game.Winner(node.board)

        if node.depth >= depth:
            return node.miniMax_score

        if depth == 0:
            if node.heuristic_score is None:
                node.heuristic_score = MiniMax.ScorePosition(node.board, node.current_player)
            return node.heuristic_score

        if is_terminal == PLAYER1:
            node.heuristic_score = math.inf
            node.miniMax_score = math.inf
            node.depth = math.inf
            return math.inf
        elif is_terminal == PLAYER2:
            node.heuristic_score = -math.inf
            node.miniMax_score = -math.inf
            node.depth = math.inf
            return -math.inf
        elif is_terminal == EMPTY:
            node.heuristic_score = 0
            node.miniMax_score = 0
            node.depth = math.inf
            return 0

        if node.current_player == 1: # Is maximizing player
            value = -math.inf
            for col in possible_moves:
                row = node.possible_moves[col]
                new_board, new_possible_moves = Game.MakeMove(node.board, node.current_player, node.possible_moves, row, col)
                # get the next node
                next_node = CreateNewNode(board=new_board, parent=node, possible_moves=new_possible_moves, current_player=node.other_player, db_path=self.db_path)
                if next_node.DepthSearch < depth - 1:
                    next_node.miniMax_score = self.DepthSearch(next_node, depth - 1, alpha, beta) # recursive
                if next_node.miniMax_score > value:
                    value = next_node.miniMax_score
                    node.recommended_move = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        else:  # Minimizing player, effectively the same code but it (guessing) is marginally faster to do it like this, TODO confirm
            value = math.inf
            for col in possible_moves:
                row = node.possible_moves[col]
                new_board, new_possible_moves = Game.MakeMove(node.board, node.current_player, node.possible_moves, row, col)
                # get the next node
                next_node = CreateNewNode(board=new_board, parent=node, possible_moves=new_possible_moves, current_player=node.other_player, db_path=self.db_path)
                if next_node.DepthSearch < depth - 1:
                    next_node.miniMax_score = self.DepthSearch(next_node, depth - 1, alpha, beta)  # recursive
                if next_node.miniMax_score < value:
                    value = next_node.miniMax_score
                    node.recommended_move = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
        node.miniMax_score = value
        node.DepthSearch = depth
        SaveNode(node, db_path=self.db_path)
        return value

    def BestMove(self, depth: int = 1):

        node = GetNode(self.game.board, db_path=self.db_path)

        if node.DepthSearch < depth:
            _ = self.DepthSearch(node, depth, -math.inf, math.inf)

        return node.recommended_move

    """
    Score Heuristic Function from https://github.com/KeithGalli/Connect4-Python/blob/master/connect4_with_ai.py#L120
    Note that this is very simple, does not fully consider a move that would make the enemy/you immediately win
      exclusively focuses on how many you get in a row
    """
    @staticmethod
    def ScorePosition(board, player):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        center_count = center_array.count(player)
        score += center_count * CENTER_SCORE

        ## Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += MiniMax.EvaluateWindow(window, player)

        ## Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_COUNT - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += MiniMax.EvaluateWindow(window, player)

        ## Score positive sloped diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += MiniMax.EvaluateWindow(window, player)

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += MiniMax.EvaluateWindow(window, player)

        return score

    @staticmethod
    def EvaluateWindow(window, current_player):
        score = 0
        other_player = PLAYER1
        if current_player == PLAYER1:
            other_player = PLAYER2

        if window.count(current_player) == 4:
            score += FOUR_SCORE
        elif window.count(current_player) == 3 and window.count(EMPTY) == 1:
            score += THREE_SCORE
        elif window.count(current_player) == 2 and window.count(EMPTY) == 2:
            score += TWO_SCORE

        if window.count(other_player) == 3 and window.count(EMPTY) == 1:
            score -= ENEMY_THREE_SCORE

        return score

