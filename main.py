#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andres Zepeda Perez

@Contact: AndresZepeda137@gmail.com
"""
# import numpy as np
# import random
# import pygame
# import sys
# import math
#
# BLUE = (0,0,255)
# BLACK = (0,0,0)
# RED = (255,0,0)
# YELLOW = (255,255,0)
#
# ROW_COUNT = 6
# COLUMN_COUNT = 7
#
# PLAYER = 0
# AI = 1
#
# EMPTY = 0
# PLAYER_PIECE = 1
# AI_PIECE = 2
#
# WINDOW_LENGTH = 4
# SQUARESIZE = 100
#
# width = COLUMN_COUNT * SQUARESIZE
# height = (ROW_COUNT + 1) * SQUARESIZE
#
# size = (width, height)
#
# RADIUS = int(SQUARESIZE / 2 - 5)
#
#
# def draw_board(board):
#     for c in range(COLUMN_COUNT):
#         for r in range(ROW_COUNT):
#             pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
#             pygame.draw.circle(screen, BLACK, (
#             int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
#
#     for c in range(COLUMN_COUNT):
#         for r in range(ROW_COUNT):
#             if board[r][c] == PLAYER_PIECE:
#                 pygame.draw.circle(screen, RED, (
#                 int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
#             elif board[r][c] == AI_PIECE:
#                 pygame.draw.circle(screen, YELLOW, (
#                 int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
#     pygame.display.update()
#
#
#
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     board = board = np.zeros((ROW_COUNT,COLUMN_COUNT))
#     game_over = False
#
#     pygame.init()
#
#     screen = pygame.display.set_mode(size)
#     draw_board(board)
#     pygame.display.update()
#
#     myfont = pygame.font.SysFont("monospace", 75)
#
#     turn = random.randint(PLAYER, AI)
#
#     piece = PLAYER_PIECE
#     time = 0
#     while time < 10:
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()
#
#             if event.type == pygame.MOUSEMOTION:
#                 pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
#                 posx = event.pos[0]
#                 if turn == PLAYER:
#                     pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
#
#             pygame.display.update()
#
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
#                 # print(event.pos)
#                 # Ask for Player 1 Input
#                 if turn == PLAYER:
#                     posx = event.pos[0]
#                     col = int(math.floor(posx / SQUARESIZE))
#                     row = int(math.floor(posy / SQUARESIZE))
#
#                     board[row][col] = piece
#
#                     piece = AI_PIECE if piece == PLAYER_PIECE else PLAYER_PIECE
#
#                     if is_valid_location(board, col):
#                         row = get_next_open_row(board, col)
#                         drop_piece(board, row, col, PLAYER_PIECE)
#
#                         if winning_move(board, PLAYER_PIECE):
#                             label = myfont.render("Player 1 wins!!", 1, RED)
#                             screen.blit(label, (40, 10))
#                             game_over = True
#
#                         time += 1
#

from StartScreen import StartScreen

if __name__ == '__main__':
    ui = StartScreen()
    player1, player2 = ui.show_start_screen()
    pass