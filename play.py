from game import Game
from monteCarlo import MCTS
from datetime import datetime
import csv


class Play:
    # TODO add all options, generalize more
    """
    :arg thinking_method: 'time' or 'moves', how long the AI thinks per turn
    :arg thinking_amount: positive number either in seconds (double, if thinking_method = 'time') or in number of nodes to explore (integer, if thinking_method = 'moves')
    :arg human_player: 0 if there is no human player, 1 if human is player 1, 2 if human is player 2
    :arg use_database: should the AI use the saved database?
    """
    def __init__(self, thinking_method: str = "time", thinking_amount = 1, human_player: int = 0, use_database: bool = False):
        self.game = Game()
        self.AI1 = MCTS(game)  # If the AI is player 1
        self.AI2 = MCTS(game)  # If the AI is player 2
        # This initializes AI2 to start with at turn 2
        self.AI2.RunTreeSimulations(state, 7, False, None, False)

        if thinking_method not in ["time", "moves"]:
            IOError("thinking_method must be one of 'time' or 'moves'")
        self.thinking_method = thinking_method
        if thinking_amount <= 0:
            IOError("thinking_amount must be positive")
        if thinking_method == "moves" and not isinstance(thinking_amount, int):
            IOError("thinking_amount must be an integer when considering move depth")
        self.thinking_amount = thinking_amount

        if thinking_method not in [0, 1, 2]:
            IOError("human_player must be one of 0, 1, or 2")
        self.human_player = human_player

        self.use_database = use_database



    def PlayGame(self):

        #################
        # TODO extract this stuff with UI
        userPlayerString = input("Player 1 or 2? ")  # comment out if not human
        userPlayer = int(userPlayerString)

        winner = False
        # keep making moves and running until there is a winner (1,2,or 0)
        while not winner:

            print()
            print("Player: ", self.game.current_player)

            self.game.PrintBoard()

            if userPlayer == self.game.current_player:
                col = self.GetUserMove()
            else:
                col = self.GetAIMove()

            row = self.game.MakeMove(col)
            winner = self.game.CheckWin(row, col)

        #################
        pass
        # TODO, game over

    # TODO, depreciate with UI
    def GetUserMove(self):
        move = -1
        while move not in self.game.possible_moves.keys():
            # print("Possible Moves: ", game.PossibleMoves(state))
            user_col_string = input("Enter Your Move (1-7): ")
            move = int(user_col_string) - 1

        return move

    # TODO make this more generalized for all options
    def GetAIMove(self):
        if self.thinking_method == "time":
            self.AI1.RunTreeTime()
            return mcts.BestMove(state)

        return self.GetAIMoveMoves()

