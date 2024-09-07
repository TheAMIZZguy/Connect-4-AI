#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

"""
    Board Deciphering:
        Rows = 6     (horizontal)
        Columns = 7  (vertical)
        
        0 means place without 'chip'
        1 means player 1 chip
        2 means player 2 chip
"""

# #the board is 6 rows with 7 columns
# startBoard = [[0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0]]

"""
Game as a class initializes the board and moves the game along
The important capabilities are:
- Obtaining what are the current possible moves
- Finding what are the possible moves a player can make
- Determining if someone has won the game
"""
class Game:

    def __init__(self, board: list[list[int]] = None, current_player: int = None, possible_moves : dict[int] = None):
        if board is None:
            self.current_player = 1
            self.board = [[0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0]]
            self.possible_moves = {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5}
        else:
            self.board = board
            if current_player is not None and possible_moves is not None:
                self.current_player = current_player
                self.possible_moves = possible_moves
            else:
                self.current_player, self.possible_moves = self.SetupBoard(self.board)

        self.other_player = 2 if self.current_player == 1 else 1


    """
    Initializes the root node with no parent, starting state and player1
    """
    @staticmethod
    def FindCurrentPlayer(board: list[list[int]]):
        move_count = sum(value != 0 for row in board for value in row)
        current_player = (move_count % 2) + 1

        return current_player

    """
    Given a board, find whose turn it is and what moves are possible
    """
    @staticmethod
    def SetupBoard(board: list[list[int]]):
        move_count = 0
        possible_moves = {}

        for col in range(len(board[0])):
            for row in reversed(range(len(board))):
                value = board[row][col]
                if value != 0:
                    move_count += 1
                if value == 0:
                    if row == len(board) - 1 or board[row + 1][col] != 0:
                        possible_moves[col] = row
                    break

        return (move_count % 2) + 1, possible_moves

    @staticmethod
    def GetBoardHash(board: list[list[int]]):
        board_tuple = tuple(tuple(row) for row in board)
        return hash(board_tuple)

    @staticmethod
    def GetMirroredBoardHash(board: list[list[int]]):
        # Mirror the board by reversing each row
        mirrored_board = [row[::-1] for row in board]

        # Convert the mirrored board to a tuple of tuples and hash it
        mirrored_board_tuple = tuple(tuple(row) for row in mirrored_board)
        return hash(mirrored_board_tuple)

    @staticmethod
    def GetMirroredColumn(col):
        return 6 - col

    '''
    Makes the move from the player and updates the game accordingly. Returns the row the play was made in
    '''
    @staticmethod
    def MakeMove(board, current_player, possible_moves, col, row):
        # Make the move
        new_board = [row[:] for row in board]
        new_board[row][col] = current_player

        # Change the player
        # next_player = 1 if current_player == 2 else 2

        # Update possible moves
        new_possible_moves = possible_moves.copy()
        if new_possible_moves[col] > 0:
            new_possible_moves[col] -= 1  # Move up by 1 due to gravity
        else:
            new_possible_moves.pop(col)  # Remove if it's already at the top

        return new_board, new_possible_moves #, next_player

    def PrintBoard(self):
        for row in self.board:
            print(row)
        print("-")

    """
    Plays a random game from board position
    """
    @staticmethod
    def RandomGame(board: list[list[int]] = None, current_player: int = None, possible_moves : dict[int] = None):
        game = Game(board, current_player, possible_moves)
        has_won = False
        while not has_won:
            if len(game.possible_moves.keys()) == 0:
                return 0
            col = random.choice(game.possible_moves.keys())
            row = game.possible_moves[col]
            new_board, new_possible_moves = game.MakeMove(game.board, game.current_player, game.possible_moves, col, row)
            game.board = new_board
            game.possible_moves = new_possible_moves
            game.current_player, game.other_player = game.other_player, game.current_player
            has_won = Game.CheckWin(game.board, row, col, game.other_player)  # Other player since we already made the move
        return game.other_player  # Other player since we already won but before the "current" player has made a move

    """
    The fast version of checking to see if a move leads to a win
    """
    @staticmethod
    def CheckWin(board, row, col, player):
        def count_in_direction(delta_row, delta_col):
            count = 0
            r, c = row + delta_row, col + delta_col
            while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player:
                count += 1
                r += delta_row
                c += delta_col
            return count

        # Check all four directions
        directions = [
            (0, 1),  # Horizontal right
            (1, 0),  # Vertical down
            (1, 1),  # Diagonal down-right
            (1, -1)  # Diagonal down-left
        ]

        for delta_row, delta_col in directions:
            count = 1  # Start with the current piece
            count += count_in_direction(delta_row, delta_col)  # Check in the positive direction
            count += count_in_direction(-delta_row, -delta_col)  # Check in the negative direction
            if count >= 4:
                return True  # Win found

        return False  # No win found

    """
    checks for winner, returns the int of the player who won, 0 for draw, and -1 for no winner
    """
    @staticmethod
    def Winner(board):

        # Horizontal Win
        for row in board:
            for num in range(4):  # So it doesn't go out of index range
                if (row[num] != 0) and (row[num] == row[num+1] == row[num+2] == row[num+3]):
                    #  Since it is 4 in a row, return the value of the winning spot
                    return row[num]
        
        # Vertical Win
        for col in range(7):
            for row in range(3):
                if (board[row][col] != 0) and (board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]):
                    return board[row][col]
                
        # Left diagonal win
        for row in range(3):
            for col in range(4):
                if (board[row][col] != 0) and (board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]):
                    return board[row][col]
                
        # Right diagonal win
        for row in range(0,3):
            for col in [6,5,4,3]:
                if (board[row][col] != 0) and (board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3]):
                    return board[row][col]

        for row in board:
            for item in row:
                if item == 0:
                    return 0  # Draw

        return -1  # No winner
    
