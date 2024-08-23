#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from state import State

"""
    Board Deciphering:
        Rows = 7   (horizontal)
        Columns = 7   (veritcal)
        
        0 means place without 'chip'
        1 means player 1 chip
        2 means player 2 chip
        3 means a place you can put a chip
"""
    
startBoard = [[0,0,0,0,0,0,0], #the board is a 6 row
                 [0,0,0,0,0,0,0], # with 7 columns
                 [0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0],
                 [3,3,3,3,3,3,3]]

class Game():

    #inizializes the root node with no parent, starting state and player1
    def Start(self): 
        # want to create copy so they dont edit each other
        newBoard = startBoard[:]
        return State([], newBoard, 1) 
    
    #gets the possible moves from the current board
    def PossibleMoves(self, state): 
        moves = [] #list of possible moves
      
        i = 0 # to mark the indexes of the possible moves
        j = 0 # indexes start at 0, obv
        for row in state.board:      
            j = 0 #reset column index at each row
            if 3 in row:
                for column in row:                 
                    #print(column)
                    if column == 3: # if it finds a possible move
                        #add it to possible moves from the Play class
                        moves.append([i,j])
                    j = j + 1
            i = i + 1 # it is added
        return moves #
    
    #makes the move from the player and updates the board
    def AfterMove(self, state, move):
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
    
    #inverts tbetween player 1 and 2, self explanitory
    def InvertPlayer(self, player): 
        tempPlayer = player
        if tempPlayer == 1:
            tempPlayer = 2
        else:
            tempPlayer = 1
        return tempPlayer
    
    #just to visualize the board, the forHumans parameter if true removes the 3's from the board to make it easier to read 
    def PrintBoard(self, board, forHumans):
        if forHumans == True:
            protoBoard = [row[:] for row in board]
            
            for row in range(len(protoBoard)):
                for value in range(len(protoBoard[row])):
                    if protoBoard[row][value] == 3:
                        protoBoard[row][value] = 0
                        
            for row in protoBoard:         
                print(row)
            print("-")
        else:
            for row in board:         
                print(row)
            print("-")
     
    #Simulates a random game from a state and current player
    def RandomGame(self, state, player):
        randomPlayer = player        
        winner = -1
        while winner == -1:
            #self.PrintBoard(randomBoard)
            move = random.choice(self.PossibleMoves(state))
            state.board = self.AfterMove(state, move[0], move[1], randomPlayer)
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
    
