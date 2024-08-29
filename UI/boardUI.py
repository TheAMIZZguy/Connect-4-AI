import tkinter as tk
import json
import os
import pygame

class BoardUI:
    _root = None
    _canvas = None
    _board_state = None
    _human_turn = False
    _selected_column = None
    _play_instance = None

    @staticmethod
    def initialize(play_instance=None):
        print("Initialized")
        BoardUI._play_instance = play_instance
        BoardUI.load_settings()

        BoardUI._root = tk.Tk()
        BoardUI._root.title("Connect-4")
        BoardUI._root.geometry("700x600")

        BoardUI._canvas = tk.Canvas(BoardUI._root, width=700, height=600, bg=BoardUI.board_colour)
        BoardUI._canvas.pack()

        BoardUI._canvas.bind("<Button-1>", BoardUI.click_handler)

        pygame.mixer.init()

    @staticmethod
    def load_settings():
        try:
            with open(os.path.join(".\\SaveData", "settings.json"), "r") as f:
                settings = json.load(f)
                BoardUI.player1_colour = settings.get("player1_colour", "#FF0000")
                BoardUI.player2_colour = settings.get("player2_colour", "#FFFF00")
                BoardUI.no_chip_colour = settings.get("no_chip_colour", "#FFFFFF")
                BoardUI.board_colour = settings.get("board_colour", "#0000FF")
                BoardUI.chip_sound_path = settings.get("chip_sound_path", "./SaveData/sounds/chipdrop_8bit.mp3")
                BoardUI.result_sound_path = settings.get("result_sound_path", "./SaveData/sounds/endgame_8bit.mp3")
        except FileNotFoundError:
            BoardUI.player1_colour = "#FF0000"
            BoardUI.player2_colour = "#FFFF00"
            BoardUI.no_chip_colour = "#FFFFFF"
            BoardUI.board_colour = "#0000FF"
            BoardUI.chip_sound_path = "./SaveData/sounds/chipdrop_8bit.mp3"
            BoardUI.result_sound_path = "./SaveData/sounds/endgame_8bit.mp3"

    @staticmethod
    def update_board(board_state, human_turn=False):
        print("Updated Board")
        BoardUI._board_state = board_state
        BoardUI._human_turn = human_turn
        BoardUI.draw_board()
        BoardUI.play_chip_sound()

    @staticmethod
    def draw_board():
        print("Drawing Board")
        BoardUI._canvas.delete("all")  # Clear the canvas
        for row in range(6):
            for col in range(7):
                x1 = col * 100
                y1 = row * 100
                x2 = x1 + 100
                y2 = y1 + 100
                if BoardUI._board_state[row][col] == 1:
                    color = BoardUI.player1_colour
                elif BoardUI._board_state[row][col] == 2:
                    color = BoardUI.player2_colour
                else:
                    color = BoardUI.no_chip_colour
                BoardUI._canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill=color, outline="black")

    @staticmethod
    def play_chip_sound():
        pygame.mixer.music.load(BoardUI.chip_sound_path)
        pygame.mixer.music.play()

    @staticmethod
    def play_result_sound():
        pygame.mixer.music.load(BoardUI.result_sound_path)
        pygame.mixer.music.play()

    @staticmethod
    def click_handler(event):
        print("click")
        if BoardUI._human_turn:
            col = event.x // 100 + 1
            BoardUI._selected_column = col
            # BoardUI._play_instance.human_move(col)

    @staticmethod
    def start_ui():
        print("start")
        BoardUI._root.mainloop()

    @staticmethod
    def end_board_ui():
        if BoardUI._root:
            BoardUI._root.destroy()