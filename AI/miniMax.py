import random
import math
from node import Node
from game import Game
from cache import get_node, save_node, create_new_node

# TODOS:
# Make as a class
# recieve a board position and return a column
# the minimax args are default in the init
# use game stuff for is terminal? and  stuff
#     (note to self, send current player info to winning move in game, so that this can use it to find terminal easier)

class MiniMax:

    def __init__(self, game):
        self.game = game
        self.current_node = Node(board=self.game.board, possible_moves=self.game.possible_moves)
        create_new_node(self.current_node)

        # Heuristics Values
        self.window_length = 4
        self.center_score = 3
        self.four_score = math.inf
        self.three_score = 5
        self.two_score = 2
        self.enemy_three_score = 4

        # Constants
        self.COLUMN_COUNT = 7
        self.ROW_COUNT = 6
        self.PLAYER1 = 1
        self.PLAYER2 = 2
        self.EMPTY = 0

    """
    Returns: best_move, node_score
    """
    def minimax(self, depth, alpha, beta, is_maximizing_player):
        valid_locations = self.game.possible_moves.keys()
        is_terminal = self.game.Winner()

        # TODO confirm that None is the best choice here
        if depth == 0:
            return None, self.score_position(self.game.current_player)

        if is_terminal == self.PLAYER1:
            return None, math.inf
        elif is_terminal == self.PLAYER2:
            return None, -math.inf
        elif is_terminal == self.EMPTY:
            return None, 0

        if is_maximizing_player:
            value = -math.inf
            column = random.choice(valid_locations)  # TODO: could just choose the first value
            for col in valid_locations:
                # row = self.game.possible_moves[col]  # TODO: can you use node for this
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, AI_PIECE)
                new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)  # could just choose the first value
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, PLAYER_PIECE)
                new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    """
        Returns: best_move, node_score
        """

    def depth_search(self, node, depth, alpha, beta, is_maximizing_player):
        possible_moves = node.possible_moves.keys()
        is_terminal = Game.Winner(node.board)

        # TODO confirm that None is the best choice here
        if depth == 0:
            return None, self.score_position(self.game.current_player)

        if is_terminal == self.PLAYER1:
            return None, math.inf
        elif is_terminal == self.PLAYER2:
            return None, -math.inf
        elif is_terminal == self.EMPTY:
            return None, 0

        if is_maximizing_player:
            value = -math.inf
            column = random.choice(possible_moves)  # TODO: could just choose the first value
            for col in possible_moves:
                row = node.possible_moves[col]
                # get the next node
                next_node =
                b_copy = board.copy()
                drop_piece(b_copy, row, col, AI_PIECE)
                new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(possible_moves)  # could just choose the first value
            for col in possible_moves:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, PLAYER_PIECE)
                new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def get_valid_locations(board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations


    # AI.algorithm == "Minimax":
    # return AI.BestMove(depth=AI.MINI_depth, use_database=AI.use_database)

    def pick_best_move(self, depth: int = 0, use_database: bool = False):
        node =

        valid_locations = get_valid_locations(board)
        best_score = -10000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, piece)
            score = score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col


    # def pick_best_move(board, piece):
    #     valid_locations = get_valid_locations(board)
    #     best_score = -10000
    #     best_col = random.choice(valid_locations)
    #     for col in valid_locations:
    #         row = get_next_open_row(board, col)
    #         temp_board = board.copy()
    #         drop_piece(temp_board, row, col, piece)
    #         score = score_position(temp_board, piece)
    #         if score > best_score:
    #             best_score = score
    #             best_col = col
    #
    #     return best_col

    """
    Score Heuristic Function from https://github.com/KeithGalli/Connect4-Python/blob/master/connect4_with_ai.py#L120
    Note that this is very simple, does not fully consider a move that would make the enemy/you immediately win
      exclusively focuses on how many you get in a row
    """
    def score_position(self, player):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(self.game.board[:, self.COLUMN_COUNT // 2])]
        center_count = center_array.count(player)
        score += center_count * self.center_score

        ## Score Horizontal
        for r in range(self.ROW_COUNT):
            row_array = [int(i) for i in list(self.game.board[r, :])]
            for c in range(self.COLUMN_COUNT - 3):
                window = row_array[c:c + self.window_length]
                score += self.evaluate_window(window, player)

        ## Score Vertical
        for c in range(self.COLUMN_COUNT):
            col_array = [int(i) for i in list(self.game.board[:, c])]
            for r in range(self.ROW_COUNT - 3):
                window = col_array[r:r + self.window_length]
                score += self.evaluate_window(window, player)

        ## Score positive sloped diagonal
        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                window = [self.game.board[r + i][c + i] for i in range(self.window_length)]
                score += self.evaluate_window(window, player)

        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                window = [self.game.board[r + 3 - i][c + i] for i in range(self.window_length)]
                score += self.evaluate_window(window, player)

        return score

    def evaluate_window(self, window, current_player):
        score = 0
        other_player = self.PLAYER1
        if current_player == self.PLAYER1:
            other_player = self.PLAYER2

        if window.count(current_player) == 4:
            score += self.four_score
        elif window.count(current_player) == 3 and window.count(self.EMPTY) == 1:
            score += self.three_score
        elif window.count(current_player) == 2 and window.count(self.EMPTY) == 2:
            score += self.two_score

        if window.count(other_player) == 3 and window.count(self.EMPTY) == 1:
            score -= self.enemy_three_score

        return score

    # # Ask for Player 2 Input
    if turn == AI and not game_over:

        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
