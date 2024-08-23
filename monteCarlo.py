#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25, 2019

@author: Andres Zepeda
"""

from monteCarloNode import MonteCarloNode
import random
from datetime import datetime
from datetime import timedelta
import threading
import victor
import csv
from state import State
from concurrent.futures import ThreadPoolExecutor, as_completed

class MCTS():
     
    def __init__(self, game):
        self.game = game
        self.UCB1Bias = 2 #change bias here
        #lets us get any node given a state
        self.nodes = {} #{state: node}, give it a state as key, it will give node as value
    
    #if the state does not exit, create a parentless node for the root node
    def MakeNode(self, state):
        #checks if empty
        if not self.nodes:
            #get the possible moves of the board
            possibleMoves = self.game.PossibleMoves(state)[:]
            #create a new node, parentless
            node = MonteCarloNode(None, None, state, possibleMoves)
            #add the state as a node
            self.nodes[tuple(state.playHistory)] = node

    #Runs through the tree, building the statistics for a set amount of minutes
    #  this is the actual learning that runs the 4 steps of MCTS
    def RunTreeTime(self, state, minutes_, usingMinimaxSelection, lom, midGame):
        #Create the root node for the tree
        self.MakeNode(state)
        simulations = 0
        
        #Info for Victor, the columns of moves
        lomString = ""       
        if lom is not None:
            lomString = "".join(lom)
            
        endTime = datetime.now() + timedelta(minutes = minutes_)
        while datetime.now() < endTime:
            #Starting the first step, Selection
            #print("Running Simulation")
            if usingMinimaxSelection:
                #start = datetime.now()
                node = self.SelectionMininmax(state, midGame, lomString)
                #print("MiniMax Sel took: ", datetime.now()-start)
            else:
                #start = datetime.now()
                node = self.Selection(state)
                #print("MCTS Sel took: ", datetime.now()-start)
            #this checks if the selected node is a winning node
            winner = self.game.Winner(node.state)
            
            #if its not a leaf node, and it wasn't a winning node (double checking) then expand the node and simulate a game (MCTS steps 2 and 3)
            if node.IsLeaf() == False and winner == -1:
                #Starting the second step, Expansion
                #print("Running Expansion")
                node = self.Expansion(node)
                
                #Starting the third step, Simulation
                #print("Running Simulation")
                
                #Instead of simulating just once, it will simulate X times 
                #  and select the most common value to minimize random chance
                """
                #start = datetime.now()    
                result = []                
                processes = []                
                
                with ThreadPoolExecutor(max_workers=10) as executor:
                    for num in range(9):
                        processes.append(executor.submit(self.Simulation, state.board, state.player))
                
                for task in as_completed(processes):
                    result.append(int(task.result()))
                    #print(int(task.result()))
                
                winner = int(max(set(result), key=result.count))
                """
                #this is if there is no leaf parallelisation
                winner = self.Simulation(state.board, state.player)
                
                #print(datetime.now() - start)
                #print("Winner is,",winner)

            #print("Running BackPropagation")
            #MCTS step 4, based on winner and the node 
            self.Backpropogation(node, winner)

            simulations += 1
        #print(simulations) #simulations of current move
        return simulations #to add to the total simulations
             
    
    #Runs through the tree for a set amount of simulations
    def RunTreeSimulations(self, state, simulations_, usingMinimaxSelection, lom, midGame):
        #Create the root node for the tree
        self.MakeNode(state)
        simulations = 0  
        
        lomString = ""
        if lom is not None:
            lomString = "".join(lom)
        
        while simulations < simulations_:
            #print("Running Selection")
            #Select a node (MCTS step 1)
            
            if usingMinimaxSelection:
                #start = datetime.now()
                node = self.SelectionMininmax(state, midGame, lomString)
                #print("MiniMax Sel took: ", datetime.now()-start)
            else:
                #start = datetime.now()
                node = self.Selection(state)
                #print("MCTS Sel took: ", datetime.now()-start)
                
            #this checks if the selected node is a winning node
            winner = self.game.Winner(node.state)
            
            #if its not a leaf node, and it wasn't a winning node (double checking) then expand the node and simulate a game (MCTS steps 2 and 3)
            if node.IsLeaf() == False and winner == -1:
                #print("Running Expansion")
                node = self.Expansion(node)
                #print("Running Simulation")
                """
                Instead of simulating just once, it will simulate X times 
                and select the most common value to minimize random chance
                """
                """
                #start = datetime.now()    
                result = []                
                processes = []                
                
                with ThreadPoolExecutor(max_workers=10) as executor:
                    for num in range(9):
                        processes.append(executor.submit(self.Simulation, state.board, state.player))
                
                for task in as_completed(processes):
                    result.append(int(task.result()))
                    #print(int(task.result()))
                
                winner = int(max(set(result), key=result.count))
                """
                #this is if there is no leaf parallelisation
                winner = self.Simulation(state.board, state.player)

            #print("Running BackPropagation")
            #MCTS step 4, based on winner and the node 
            self.Backpropogation(node, winner)
            #print("Finished BackPropogation")

            simulations += 1
        #print(simulations) #simulations of current move
        return simulations #to add to the total simulations
    
    #gets the best move from a position
    #based on most amount of simulations played
    def BestMove(self, state):
        self.MakeNode(state)
        
        if not self.nodes[str(state.playHistory)].IsFullyExpanded():
            raise Exception("Missing Info")
            
        #node = self.nodes[state.Hash()]
        node = self.nodes[str(state.playHistory)]
        posMoves = node.PossibleMoves()
        bestMove = []
        maxSims = -100
        for move in posMoves:
            childNode = node.ChildNode(move)
            if childNode.games > maxSims:
                bestMove = move
                maxSims = childNode.games
        
        return bestMove        
        
    
    # MCTS Step 1, choose nodes until needing to expand
    # Will always stop selection and choose an unexpanded node if any available
    def Selection(self, state):
        #Since the board at the beggining is empty, it needs to add the '[]' or else it gets a KeyError
        self.nodes['[]'] = self.nodes[()]
        
        #gets the selected node from the list of nodes, based on the board        
        try:
            node = self.nodes[state.Hash()]
        except:
            print("Not Sufficiently Expanded: Starting a force Expansion")
            self.Expansion(self.nodes[state.Hash2()])
            self.Expansion(self.nodes[state.Hash2()])
            self.Expansion(self.nodes[state.Hash2()])
            self.Expansion(self.nodes[state.Hash2()])
            self.Expansion(self.nodes[state.Hash2()])
            self.Expansion(self.nodes[state.Hash2()])
            self.Expansion(self.nodes[state.Hash2()])
            node = self.nodes[state.Hash()]
        
        #sets UCB1 bias
        bias = 2
        while (node.IsFullyExpanded()) and (not node.IsLeaf()):
            moves = node.PossibleMoves()
            bestPlay = []
            bestUCB1 = -100
            #will loop through all the moves and select highest UCB1
            for move in moves: 
                childUCB1 = node.ChildNode(move).UCB1Value(bias)
                if childUCB1 > bestUCB1:
                    bestPlay = move
                    bestUCB1 = childUCB1
                    
            node = node.ChildNode(bestPlay)
        
        return node
     
    # MCTS Step 1, choose nodes until needing to expand
    # Will always stop selection and choose an unexpanded node if any available
    def SelectionMininmax(self, state, midGame, lom):
        #Since the board at the beggining is empty, it needs to add the '[]' or else it gets a KeyError
        self.nodes['[]'] = self.nodes[()]
        
        #gets the selected node from the list of nodes, based on the board
        try:
            node = self.nodes[state.Hash()]
        except:
            #if a move is made by another player and it isnt already expanded, it will break the game
            #thus if there is an error (usually KeyError), it will forcefully make the previous node have that move expanded
            print("Not Sufficiently Expanded: Starting a force Expansion")
            self.Expansion(self.nodes[state.Hash2()])
            self.Expansion(self.nodes[state.Hash2()])
            self.Expansion(self.nodes[state.Hash2()])
            self.Expansion(self.nodes[state.Hash2()])
            self.Expansion(self.nodes[state.Hash2()])
            self.Expansion(self.nodes[state.Hash2()])
            self.Expansion(self.nodes[state.Hash2()])
            node = self.nodes[state.Hash()]
        
        selectedMinimax = 7
        currentSelectionMoves = []
        #sets UCB1 bias
        bias = 2
        
        if not node.IsFullyExpanded():
            return node
        
        while node.recommendedMove > -1 and (node.IsFullyExpanded()) and (not node.IsLeaf()):
            selectedMinimax = node.recommendedMove          
            moves = node.PossibleMoves()
            bestPlay = []
            bestUCB1 = -100
            #will loop through all the moves and select highest UCB1
            for move in moves: 
                childUCB1 = node.ChildNode(move).UCB1Value(bias)
                if move[1] == selectedMinimax:
                    childUCB1 += .350
                if childUCB1 > bestUCB1:
                    bestPlay = move
                    bestUCB1 = childUCB1
                               
            node = node.ChildNode(bestPlay)
            
            if (not node.IsFullyExpanded()) or (node.IsLeaf()):
                return node    
                    
        #print("Vic is Starting")
        stop_event = threading.Event()
       
        #This initiates the thread that will run and send it all the important information
        if node.parent is not None:
            #change the node.state to just state if not working. and maybe not in the node.parent
            if (node.state.vicBoard == node.parent.state.vicBoard):
                print("State board equals its parent")
                print(node.state.vicBoard)
                print(node.parent.state.vicBoard)
                if node.parent.parent is not None:
                    print(node.parent.parent.state.vicBoard)
                    vic = threading.Thread(target=victor.main,args=(stop_event, node.state.vicBoard, node.state.player, node.parent.parent.state.vicBoard, midGame, lom,))
                else:
                    print("And doesn't have a grandparent")
                    vic = threading.Thread(target=victor.main,args=(stop_event, node.state.vicBoard, node.state.player, None, midGame, lom,))
            else:
                vic = threading.Thread(target=victor.main,args=(stop_event, node.state.vicBoard, node.state.player, node.parent.state.vicBoard, midGame, lom,))
        else:
            print("Running Vic Selection for first move")
            vic = threading.Thread(target=victor.main,args=(stop_event, node.state.vicBoard, node.state.player, None, midGame, lom,))

        vic.daemon = True
        vic.start()     
        #SCC False means that it is waiting for its turn
        SCC = False
        
        while (node.IsFullyExpanded()) and (not node.IsLeaf()):
            moves = node.PossibleMoves()
            bestPlay = []
            bestUCB1 = -100

            #Telling victor to start finding the best move
            csv_file = open("VCC.csv", mode="w")
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow('1')           
            csv_file.close()
            #Waiting for victor to find move before continuing      
            endTimer = datetime.now() + timedelta(seconds = 59)
            while not SCC:
                csv_file = open("SCC.csv")
                csv_reader = csv.reader(csv_file,delimiter=",") 
                
                lineCount = 1
                for row in csv_reader:
                    if lineCount == 1:
                        if int(f'{row[0]}') == 1:
                            #print("CVV reads ", row)
                            SCC = True   
                    lineCount += 1
                csv_file.close()

                if datetime.now() > endTimer:
                    for move in moves: 
                        childUCB1 = node.ChildNode(move).UCB1Value(bias)
                        if childUCB1 > bestUCB1:
                            bestPlay = move
                            bestUCB1 = childUCB1
                            node = node.ChildNode(bestPlay)
            
                    if (not node.IsFullyExpanded()) or (node.IsLeaf()):
                        stop_event.set()
                        try:
                            vic.join(timeout=.00001)
                        except:
                            pass
                        return node
            
            #Pausing victor to finish its own thing
            csv_file = open("VCC.csv", mode="w")
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow('0')           
            csv_file.close()                    
            
            #looking at the move Victor found
            csv_file = open("ExMove.csv")
            csv_reader = csv.reader(csv_file,delimiter=",")
            lineCount = 1
            for row in csv_reader:
                if lineCount == 7:
                    #print("Selection Reads this as Vic Rec: ", row)
                    selectedMinimax = int(f'{row[0]}')
                lineCount += 1
            csv_file.close()
            
            #will loop through all the moves and select highest UCB1
            for move in moves: 
                childUCB1 = node.ChildNode(move).UCB1Value(bias)
                if move[1] == selectedMinimax:
                    childUCB1 += .350
                    node.recommendedMove = move[1]
                if childUCB1 > bestUCB1:
                    bestPlay = move
                    bestUCB1 = childUCB1
                           
            node = node.ChildNode(bestPlay)
            
            if (not node.IsFullyExpanded()) or (node.IsLeaf()):
                stop_event.set()
                try:
                    vic.join(timeout=.00001)
                except:
                    pass
                return node
            
            #this is to tell victor which selection was made so it has the same board placement
            currentSelectionMoves.append(bestPlay[1])
            
            #print("Best play is ", bestPlay[1])
            #print("CSM is ", currentSelectionMoves)
            try:
                csv_file = open("ExMove.csv")
                csv_reader = csv.reader(csv_file,delimiter=",")
                lines = list(csv_reader)
                csv_file.close()
                #print(lines)
                lines[2] = currentSelectionMoves
                #print(lines)
                csv_file = open("ExMove.csv", mode="w", newline = '')
                csv_writer = csv.writer(csv_file, delimiter=",")
                for line in range(len(lines)):
                    csv_writer.writerow(lines[line])
                csv_file.close()
            except:
                csv_file = open("ExMove.csv")
                csv_reader = csv.reader(csv_file,delimiter=",")
                lines = list(csv_reader)
                csv_file.close()
                #print(lines)
                lines[2] = currentSelectionMoves
                #print(lines)
                csv_file = open("ExMove.csv", mode="w", newline = '')
                csv_writer = csv.writer(csv_file, delimiter=",")
                for line in range(len(lines)):
                    csv_writer.writerow(lines[line])
                csv_file.close()
                
            csv_file = open("VCC.csv", mode="w")
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow('1')           
            csv_file.close()

        stop_event.set()
        try:
            vic.join(timeout=.00001)
        except:
            pass
        return node
    
    # MCTS Step 2, expand a new node
    def Expansion(self, node):
        #print("Expanded")
        #selects a random unexpanded node
        moves = node.UnexpandedMoves()
        if len(moves) == 0:
            print("No unexpanded Moves")
            return
        move = random.choice(moves)
        #gets the new board state from the move,
        childState = self.game.MakeMove(node.state, move)
        #gets the child's own possible moves and prepares the node for expansion
        childUnexpandedMoves = self.game.PossibleMoves(childState)
        childNode = node.Expand(move, childState, childUnexpandedMoves)
        self.nodes[childState.Hash()] = childNode
        return childNode
        
    
    # MCTS Step 3, simulate a game from the new node, get winner
    def Simulation(self, aBoard, thePlayer):
        #print("Simulaiton Running")
        state = State([], aBoard, thePlayer)
        winner = self.game.Winner(state)
        
        #while there is no winner
        while winner == -1:
            moves = self.game.PossibleMoves(state)
            move = random.choice(moves)
            state = self.game.MakeMove(state, move)
            winner = self.game.Winner(state)
        return winner  
    
    # MCTS Step 4, backpropagate the information
    # *itself and all parents will increase their plays
    # *all the nodes of the non winner (not the actual winner) will increase their win counter
    # -- It increase the non winner counter due to it selecting a node based on parent, which is the other player
    def Backpropogation(self, node, winner):
        #print("Backprop in Progress")
        while node is not None:
            node.games += 1
            if winner == 0:
                node.wins += 0.5
            elif not node.state.IsPlayer(winner):
                node.wins += 1
            node = node.parent 

    #lets you see the stats of the children of a node used for selection
    def GetStats(self, state):
        #Does this to eliminate KeyError
        self.nodes['[]'] = self.nodes[()]
        #Gets the stat of the node and its direct children
        node = self.nodes[str(state.playHistory)]
        #print("NodeID: ", node.iD)
        stats =  {"plays": node.games, "wins": node.wins, "children": []}
        for child in node.children.values():
            if child['node'] == None:
                stats['children'].append({ "play": child['play'], "games": None, "wins": None})
            else:
                stats['children'].append({ "play": child['play'], "games": child['node'].games, "wins": child['node'].wins})
        
        return stats
    