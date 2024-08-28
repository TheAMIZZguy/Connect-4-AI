#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andres Zepeda Perez

@Contact: AndresZepeda137@gmail.com
"""

from UI.startScreen import StartScreen
from UI.endScreen import EndScreen
from UI.boardUI import BoardUI
from play import Play

if __name__ == '__main__':
    isPlaying = True
    while isPlaying:
        startScreen = StartScreen()
        player1, player2 = startScreen.show_start_screen()

        # Play the game and get the winner
        gamestate = Play(player1, player2)
        winner = gamestate.PlayGame()  # Placeholder for game execution

        #########
        # board = [[0 for _ in range(7)] for _ in range(6)]  # Empty board
        #
        # # Initialize BoardUI
        # BoardUI.initialize(None)  # Passing None for play_instance as we're testing in isolation
        #
        # # Update the initial board (display an empty board with human turn enabled)
        # BoardUI.update_board(board, human_turn=True)
        #
        # # Start the UI event loop
        # current_player = 1
        # game_over = False
        #
        # while not game_over:
        #     BoardUI._root.update()  # Process UI events
        #
        #     if current_player == 1:  # Human player's turn
        #         move = BoardUI._selected_column
        #         if move is not None:
        #             print(f"Human moved at column: {move}")
        #             # Find the first empty row in the selected column
        #             for row in reversed(range(6)):
        #                 if board[row][move - 1] == 0:  # Adjust for 0-indexing
        #                     board[row][move - 1] = current_player
        #                     break
        #             BoardUI._selected_column = None
        #             current_player = 2  # Switch to AI
        #             BoardUI.update_board(board, human_turn=False)
        #
        #     else:  # AI's turn
        #         move = random.randint(1, 7)
        #         print(f"AI moved at column: {move}")
        #         # Find the first empty row in the randomly selected column
        #         for row in reversed(range(6)):
        #             if board[row][move - 1] == 0:  # Adjust for 0-indexing
        #                 board[row][move - 1] = current_player
        #                 break
        #         current_player = 1  # Switch back to Human
        #         BoardUI.update_board(board, human_turn=True)
        #
        #     # Draw the updated board state
        #     BoardUI.draw_board()
        #
        #     # For this test, you can set a condition to end the loop
        #     if all(cell != 0 for row in board for cell in row):
        #         game_over = True
        #
        # winner = 8712
        ##################
        # Show the end screen and get the decision
        endScreen = EndScreen(winner)
        isPlaying = endScreen.show_end_screen()

        BoardUI.end_board_ui()

        # Keep the endgame board screen visible until a new game starts or it is manually closed
        # gamestate.end_board_ui()