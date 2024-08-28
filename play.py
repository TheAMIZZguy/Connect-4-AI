from game import Game
# from monteCarlo import MCTS  # todo finish MCTS
# from miniMax import MiniMax  # todo finish MiniMax
from UI.boardUI import BoardUI

from random import randint


class Player:
    def __init__(self, is_human: bool = False, player_num: int = 1, algorithm: str = "Hybrid",
                 MCTS_method: str = "time", MCTS_amount = 1, MINI_depth = 1, use_database: bool = False):
        self.is_human = is_human
        self.player_num = player_num  # 1 or 2

        self.algorithm = algorithm  # "MCTS" or "Minimax" or "Hybrid"

        if self.algorithm in ["MCTS", "Hybrid"]:

            self.MCTS_method = MCTS_method  # 'time' (s) or 'moves' (n)

            if MCTS_method == "moves" and not isinstance(MCTS_amount, int):
                IOError("thinking_amount must be an integer when considering move depth")
            self.MCTS_amount = MCTS_amount

        if self.algorithm in ["Minimax", "Hybrid"]:
            self.MINI_depth = MINI_depth  # 'time' (s) or 'moves' (n)

        self.use_database = use_database

class Play:
    """
    :arg thinking_method: 'time' or 'moves', how long the AI thinks per turn
    :arg thinking_amount: positive number either in seconds (double, if thinking_method = 'time') or in number of nodes to explore (integer, if thinking_method = 'moves')
    :arg human_player: 0 if there is no human player, 1 if human is player 1, 2 if human is player 2
    :arg use_database: should the AI use the saved database?
    """
    def __init__(self, player1: Player, player2: Player):
        self.game = Game()

        self.player1 = player1
        self.player2 = player2

        # if not self.player1.is_human:
        #     if self.player1.algorithm == "MCTS":
        #         self.AI1 = MCTS(game)
        #     elif self.player1.algorithm == "Minimax":
        #         self.AI1 = MiniMax(game)
        #     else:
        #         self.AI1 = MCTS(game, True)
        #
        # if not self.player2.is_human:
        #     if self.player2.algorithm == "MCTS":
        #         self.AI2 = MCTS(game)
        #     elif self.player1.algorithm == "Minimax":
        #         self.AI2 = MiniMax(game)
        #     else:
        #         self.AI2 = MCTS(game, True)
        #     if self.player2.algorithm in ["MCTS", "Hybrid"] and not self.player2.use_database:
        #         self.AI2.RunTreeSimulations(7)

        BoardUI.initialize(self)

    def PlayGame(self):
        # Start with the initial board
        BoardUI.update_board(self.game.board, human_turn=self.player1.is_human if self.game.current_player == 1 else self.player2.is_human)

        winner = False
        round = 1
        # keep making moves and running until there is a winner or the game is a draw
        while not winner and round < 22:
            # self.game.PrintBoard()
            BoardUI._root.update()

            while True:
                if self.game.current_player == 1:
                    if self.player1.is_human:
                        col = self.GetUserMove()
                    else:
                        col = self.GetAIMove()
                else:
                    if self.player2.is_human:
                        col = self.GetUserMove()
                    else:
                        col = self.GetAIMove()
                if col in self.game.possible_moves.keys():
                    break

            row = self.game.MakeMove(col)
            winner = self.game.CheckWin(row, col)
            round += 1

            BoardUI.update_board(self.game.board, human_turn=self.player1.is_human if self.game.current_player == 1 else self.player2.is_human)
            BoardUI.draw_board()

        return self.game.other_player


    def GetUserMove(self):
        move = None
        while move is None:
            BoardUI._root.update()
            move = BoardUI._selected_column
        BoardUI._selected_column = None
        print("HUMAN TECHNOLOGY: ", move)
        return move - 1

    def GetAIMove(self):
        AI = self.AI1 if self.game.current_player == self.player1 else self.AI2

        if AI.algorithm == "Minimax":
            return AI.BestMove(depth=AI.MINI_depth, use_database=AI.use_database)
        else:
            if AI.MCTS_method == "time":
                AI.RunTreeTime(time=AI.MCTS_amount, use_database=AI.use_database)
            else:
                AI.RunTreeSimulations(simulations=AI.MCTS_amount, use_database=AI.use_database)

            return AI.BestMove()

    def GetAIMove(self):
        move = randint(0,6)
        print("AI TECHNOLOGY: ", move + 1)
        return move


