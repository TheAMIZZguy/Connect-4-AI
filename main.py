#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andres Zepeda Perez

@Contact: AndresZepeda137@gmail.com
"""
from startScreen import StartScreen
from endScreen import EndScreen
from play import Play

if __name__ == '__main__':
    isPlaying = True
    while isPlaying:
        startScreen = StartScreen()
        player1, player2 = startScreen.show_start_screen()

        # Play the game and get the winner
        # gamestate = Play(player1, player2)
        # winner = gamestate.PlayGame()  # Placeholder for game execution
        winner = 1
        # Show the end screen and get the decision
        endScreen = EndScreen(winner)
        isPlaying = endScreen.show_end_screen()

        # Keep the endgame board screen visible until a new game starts or it is manually closed
        # gamestate.end_board_ui()