#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from state import State

"""
    Board Deciphering:
        Rows = 6     (horizontal)
        Columns = 7  (vertical)
        
        0 means place without 'chip'
        1 means player 1 chip
        2 means player 2 chip
        3 means a place you can put a chip
"""

#the board is 6 rows with 7 columns
startBoard = [[0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0],
              [3,3,3,3,3,3,3]]

"""
Game as a class initializes the board and moves the game along
The important capabilities are:
- Obtaining what are the current possible moves
- Finding what are the possible moves a player can make
- Determining if someone has won the game
"""
class Game:

    def __init__(self, board: list[list[int]] = None):
        if board is None:
            self.current_player = 1
            self.board = [[0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0]]
            self.possible_moves = [[5,0],[5,1],[5,2],[5,3],[5,4],[5,5],[5,6]]
        else:
            self.board = board
            self.current_player, self.possible_moves = self.SetupBoard(self.board)


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
        possible_moves = []

        for col in range(len(board[0])):
            for row in reversed(range(len(board))):
                value = board[row][col]
                if value != 0:
                    move_count += 1
                if value == 0:
                    if row == len(board) - 1 or board[row + 1][col] != 0:
                        possible_moves.append([row, col])
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


    """
    Makes the move from the player and updates the game accordingly
    """
    def MakeMove(self, move):
        # Make the move
        self.board[move[0]][move[1]] = self.current_player

        # Change the player
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

        # Update possible moves
        def UpdatePossibleMoves(self, col):
            if self.possible_moves[col] > 0:
                self.possible_moves[col] -= 1  # Move up by 1 due to gravity
            else:
                self.possible_moves.pop(col)  # Remove if it's already at the top
        # TODO change the rest of stuff with possible moves so I can use this logic


        #The history of the play
        newHistory = (state.playHistory[:])
        #add the current play to history
        newHistory.append(move) 
        #make this new state have the same board to edit.

        newBoard = [row[:] for row in state.board]
        if newBoard[move[0]][move[1]] == 3: #making sure its a possible move
            newBoard[move[0]][move[1]] = state.player #make the move as the player
            if move[0] > 0: #if its not at the top...
                newBoard[move[0]-1][move[1]] = 3 #make place above possible
        #print("PLAYER:", player)
        newPlayer = self.InvertPlayer(state.player) #invert the player
        #print("PLAYER@:", newPlayer)
        return State(newHistory, newBoard, newPlayer) #new state
    
    #inverts between player 1 and 2, self explanitory
    def InvertPlayer(self, player): 
        tempPlayer = player
        if tempPlayer == 1:
            tempPlayer = 2
        else:
            tempPlayer = 1
        return tempPlayer

    def PrintBoard(self):
        for row in self.board:
            print(row)
        print("-")

     
    #Simulates a random game from a state and current player
    def RandomGame(self, state, player):
        randomPlayer = player        
        winner = -1
        while winner == -1:
            #self.PrintBoard(randomBoard)
            move = random.choice(self.PossibleMoves(state))
            state.board = self.MakeMove(state, move[0], move[1], randomPlayer)
            winner = self.Winner(state.board)
            if self.PossibleMoves(state.board) == []:
                winner = 0
            if randomPlayer == 1:
                randomPlayer = 2
            else:
                randomPlayer = 1
        #print("The winner is", winner)
        return winner
    
    #checks for winner, returns the int of the player who won, 0 for draw, and -1 for no winner
    def Winner(self, state):
        board = state.board
        
        #if the top row is full of 1's and 2's it means its full and therefore tie
        if (3 in board[0]) or (0 in board[0]):
          pass
        else:
            return 0
            
        
        #Horizontal Win
        for row in board:
            for num in range(0,4):#so it doesnt go out of index range
                #print(num)cc
                if row[num] == row[num+1] == row[num+2] == row[num+3] and not (row[num] == 3 or row[num] == 0):
                    #since it is 4 in a row, return the value of the winning spot
                    return row[num]
        
        #Vertical Win
        for col in range(0,7): #using range so its based on the index
            for row in range(0,3): #less rows
                #print(num)
                if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] and not (board[row][col] == 3 or board[row][col] == 0):
                    return board[row][col]
                
        #Left diagonal win
        for row in range(0,3): #using range so its based on the index
            for col in range(0,4): #the rest is the same
                #print(num)
                if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] and not (board[row][col] == 3 or board[row][col] == 0):
                    return board[row][col] 
                
        #Right diagonal win
        for row in range(0,3): #using range so its based on the index
            for col in [6,5,4,3]: #it needs to loop from the right
                #print(num)
                if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3] and not (board[row][col] == 3 or board[row][col] == 0):
                    return board[row][col]
        
        #-1 means that there is no winner... yet
        return -1
    
