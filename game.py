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
        3 means a place you can put a chip
"""

# #the board is 6 rows with 7 columns
# startBoard = [[0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0],
#               [3,3,3,3,3,3,3]]

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

    def GetBoardHash(self):
        board_tuple = tuple(tuple(row) for row in self.board)
        return hash(board_tuple)

    def GetMirroredBoardHash(self):
        # Mirror the board by reversing each row
        mirrored_board = [row[::-1] for row in self.board]

        # Convert the mirrored board to a tuple of tuples and hash it
        mirrored_board_tuple = tuple(tuple(row) for row in mirrored_board)
        return hash(mirrored_board_tuple)

    '''
    Makes the move from the player and updates the game accordingly
    '''
    def MakeMove(self, col):
        # Make the move
        self.board[col][self.possible_moves[col]] = self.current_player

        # Change the player
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

        # Update possible moves
        if self.possible_moves[col] > 0:
            self.possible_moves[col] -= 1  # Move up by 1 due to gravity
        else:
            self.possible_moves.pop(col)  # Remove if it's already at the top

    def PrintBoard(self):
        for row in self.board:
            print(row)
        print("-")

    """
    Plays a random game from current position
    """
    def RandomGame(self):
        hasWon = False
        while not hasWon:
            if len(self.possible_moves.keys()) == 0:
                return 0
            col = random.choice(self.possible_moves.keys())
            row = self.possible_moves[col]
            self.MakeMove(col)
            hasWon = self.CheckWin(row, col)
        return self.other_player

    """
    The fast version of checking to see if a move leads to a win
    """
    def CheckWin(self, row, col):
        def count_in_direction(delta_row, delta_col):
            count = 0
            r, c = row + delta_row, col + delta_col
            while 0 <= r < len(self.board) and 0 <= c < len(self.board[0]) and self.board[r][c] == self.other_player:
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
    def Winner(self):

        #Horizontal Win
        for row in self.board:
            for num in range(0,4):#so it doesnt go out of index range
                #print(num)cc
                if row[num] == row[num+1] == row[num+2] == row[num+3] and not (row[num] == 3 or row[num] == 0):
                    #since it is 4 in a row, return the value of the winning spot
                    return row[num]
        
        #Vertical Win
        for col in range(0,7): #using range so its based on the index
            for row in range(0,3): #less rows
                #print(num)
                if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col] and not (self.board[row][col] == 3 or self.board[row][col] == 0):
                    return self.board[row][col]
                
        #Left diagonal win
        for row in range(0,3): #using range so its based on the index
            for col in range(0,4): #the rest is the same
                #print(num)
                if self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3] and not (self.board[row][col] == 3 or self.board[row][col] == 0):
                    return self.board[row][col]
                
        #Right diagonal win
        for row in range(0,3): #using range so its based on the index
            for col in [6,5,4,3]: #it needs to loop from the right
                #print(num)
                if self.board[row][col] == self.board[row+1][col-1] == self.board[row+2][col-2] == self.board[row+3][col-3] and not (self.board[row][col] == 3 or self.board[row][col] == 0):
                    return self.board[row][col]
        
        #-1 means that there is no winner... yet
        return -1
    
