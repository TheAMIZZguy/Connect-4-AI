from game import Game
from monteCarlo import MCTS
from datetime import datetime
import csv





class Play:

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



def PlayGame():

for testedGame in range(1):
    print("\n\n===============\nSimulating game ", testedGame + 1)
    startTime = datetime.now()

    game = Game()
    mcts = MCTS(game)
    mcts2 = MCTS(game)

    state = game.Start()
    winner = game.Winner(state)

    move = []
    totalSims = 0
    totalSims1 = 0
    totalSims2 = 0

    # Edit these depending on how you want to play
    isLearningSelf = False
    forHumans = True

    tempBool = True

    # this is so the tree is at least somewhat built before they start playing (to avoid errors)
    mcts2.RunTreeSimulations(state, 7, False, None, False)

    # This resets the data sent to ExMove.csv
    csv_file = open("ExMove.csv", mode="w")
    csv_writer = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['Current Selected Moves:'])
    csv_writer.writerow([])
    csv_writer.writerow(['Victor Recommended Move'])
    csv_writer.writerow([])
    csv_file.close()

    listOfRows1 = []
    listOfRows2 = []

    currentlyInMini = True
    # If the computer will train by itself and play against itself
    if isLearningSelf:

        contNum = 0
        while winner == -1:

            """ RunTreeX( 
                    the State, 
                    time (in mins) to think, 
                    If it will use MiniMaxed based Training
                    If above is true: The list of the Columns of the other player's moves excluding the last one,
                    If the game has already started or not)
            """
            try:
                # .0835 for 5 seconds .0167 for 1 second .01169 for .7 seconds
                t = datetime.now()
                # this version is so that the algorithm uses MCTS half of the time
                if len(listOfRows2) > 1:
                    totalSims1 += mcts.RunTreeSimulations(state, 12250, False, listOfRows2[:-1], True)
                else:
                    totalSims1 += mcts.RunTreeSimulations(state, 12250, False, None, False)

                print("Player 1 ran in ", datetime.now() - t)

                print(mcts.GetStats(state))
                move = mcts.BestMove(state)
                print("Chosen Play MCTS: ", move)
            except Exception as e:
                print("Error: ", e)
                crashCount += 1
                print("Lol it crashed ;-;")
                if len(listOfRows2) > 1:
                    totalSims1 += mcts.RunTreeSimulations(state, 7, True, listOfRows2[:-1], True)
                else:
                    totalSims1 += mcts.RunTreeSimulations(state, 7, True, None, False)
                # print(mcts.GetStats(state))
                move = mcts.BestMove(state)
                # print("Chosen Play: ", move)

            # adds to the info on what has happened in the game before sending it off
            listOfRows1.append(str(move[0]))

            csv_file = open("ExMove.csv", mode="w")
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow(['Current Selected Moves:'])
            csv_writer.writerow([])
            csv_writer.writerow(['Victor Recommended Move'])
            csv_writer.writerow([])
            csv_file.close()

            # moves the state forward
            state = game.MakeMove(state, move)
            winner = game.Winner(state)

            if winner != -1:
                break

            # prints board
            print()
            print("Player: ", (state.player))
            for row in state.board:
                print(row)

            try:
                # .0835 for 5 seconds .0167 for 1 second 0.01169 for .7 seconds
                if currentlyInMini:
                    if len(listOfRows1) > 1:
                        totalSims2 += mcts2.RunTreeSimulations(state, 49, True, listOfRows1[:-1], True)
                    else:
                        totalSims2 += mcts2.RunTreeSimulations(state, 49, True, None, False)
                    currentlyInMini = False
                else:
                    if len(listOfRows2) > 1:
                        totalSims2 += mcts2.RunTreeSimulations(state, 12250, False, listOfRows1[:-1], True)
                    else:
                        totalSims2 += mcts2.RunTreeSimulations(state, 12250, False, None, False)
                    currentlyInMini = True
                print("Player 2 ran in ", datetime.now() - t)
                print(mcts2.GetStats(state))
                move = mcts2.BestMove(state)
                print("Chosen Play MCTS: ", move)
            except Exception as e:
                print("Error: ", e)
                crashCount += 1
                print("Lol it crashed2 ;-;")
                if len(listOfRows1) > 1:
                    totalSims2 += mcts2.RunTreeSimulations(state, 7, False, listOfRows1[:-1], True)
                else:
                    totalSims2 += mcts2.RunTreeSimulations(state, 7, False, None, False)
                # print(mcts2.GetStats(state))
                move = mcts2.BestMove(state)
                # print("Chosen Play: ", move)

            listOfRows2.append(str(move[0]))

            csv_file = open("ExMove.csv", mode="w")
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow(['Current Selected Moves:'])
            csv_writer.writerow([])
            csv_writer.writerow(['Victor Recommended Move'])
            csv_writer.writerow([])
            csv_file.close()

            # moves the state forward
            state = game.MakeMove(state, move)
            winner = game.Winner(state)

            # prints board
            print()
            print("Player: ", (state.player))
            for row in state.board:
                print(row)

            if winner != -1:
                break

    ##########################################################################################################
    # Computer trains by itself and plays against external Player
    else:
        userPlayerString = input("Player 1 or 2? ")  # comment out if not human
        userPlayer = int(userPlayerString)

        # MCTS needs to have at least the nodes of tree built
        # so this lets it make the nodes before a move is made by external player if they move firs
        if userPlayer == 1:
            mcts.RunTreeSimulations(state, 7, False, None, False)

        s1 = None
        # keep making moves and running until there is a winner (1,2,or 0)
        while winner == -1:

            print()
            print("Player: ", (state.player))

            game.PrintBoard(state.board, forHumans)

            if userPlayer == state.player:
                while move not in game.PossibleMoves(state):
                    # print("Possible Moves: ", game.PossibleMoves(state))
                    userColString = input("Enter Your move (1-7): ")
                    userCol = int(userColString) - 1

                    for i in range(7):
                        if [i, userCol] in game.PossibleMoves(state):
                            move = [i, userCol]

                    if move not in game.PossibleMoves(state):
                        print("Move not Possible")

                listOfRows2.append(str(move[0]))

                csv_file = open("ExMove.csv", mode="w")
                csv_writer = csv.writer(csv_file, delimiter=",")
                csv_writer.writerow(['Current Selected Moves:'])
                csv_writer.writerow([])
                csv_writer.writerow(['Victor Recommended Move'])
                csv_writer.writerow([])
                csv_file.close()

            else:
                # time to have the algorithm think for x minutes
                # simulations to have it think for x simulations
                # TODO update to newest versions/Add Minimax Hybrid
                try:
                    if currentlyInMini:
                        if len(listOfRows1) > 1:
                            totalSims += mcts.RunTreeSimulations(state, 49, True, listOfRows2[:-1], True)
                        else:
                            totalSims += mcts.RunTreeSimulations(state, 49, True, None, False)
                        currentlyInMini = False
                    else:
                        if len(listOfRows2) > 1:
                            totalSims += mcts.RunTreeSimulations(state, 12250, False, listOfRows2[:-1], True)
                        else:
                            totalSims += mcts.RunTreeSimulations(state, 12250, False, None, False)
                        currentlyInMini = True
                    # print("Player 2 ran in " , datetime.now() - t)
                except Exception as e:
                    print("Error: ", e)
                    crashCount += 1
                    print("Lol it crashed2 ;-;")
                    if len(listOfRows1) > 1:
                        totalSims += mcts.RunTreeSimulations(state, 7, False, listOfRows2[:-1], True)
                    else:
                        totalSims += mcts.RunTreeSimulations(state, 7, False, None, False)
                    # totalSims += mcts.RunTreeSimulations(state,1000)

                print(mcts.GetStats(state))
                move = mcts.BestMove(state)
                print("Chosen Play: ", move)

            state = game.MakeMove(state, move)
            winner = game.Winner(state)

    ###############################################################################################
    if winner == 1:
        totalPlayer1Wins += 1
    elif winner == 2:
        totalPlayer2Wins += 1
    elif winner == 0:
        totalDrawGames += 1
    else:
        totalGameErrors += 1
        print("This shouldn't happen")

    print("-----------------")
    print("Winner: ", winner)
    game.PrintBoard(state.board, forHumans)

    totalSims = totalSims1 + totalSims2
    print("\nTotal Simulations 1: ", totalSims1)
    print("Total Simulations 2: ", totalSims2)
    print("Total Simulations: ", totalSims)
    print("Elapsed Time: ", datetime.now() - startTime)
    totalTime += (datetime.now() - startTime)

    print("\nCurrentTotalPlayer1Wins: ", totalPlayer1Wins)
    print("CurrentTotalPlayer2Wins: ", totalPlayer2Wins)
    print("CurrentTotalDrawGames: ", totalDrawGames)
    print("CurrentTotalGameErrors: ", totalGameErrors)
    print("CurrentTotal Elapsed Time: ", totalTime)
    print("Current Crashes ;/ : ", crashCount)

print("\n\n\nTotalPlayer1Wins: ", totalPlayer1Wins)
print("TotalPlayer2Wins: ", totalPlayer2Wins)
print("TotalDrawGames: ", totalDrawGames)
print("TotalGameErrors: ", totalGameErrors)
print("Total Elapsed Time: ", totalTime)
print("Crashes ;/ : ", crashCount)
