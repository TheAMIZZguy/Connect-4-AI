#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andres Zepeda Perez

@Contact: AndresZepeda137@gmail.com
Made with ChatGPT-4o because I don't like making GUIs
"""

import pygame
import tkinter as tk
from tkinter import ttk
from play import Player
from tkinter import colorchooser
from tkinter import filedialog
import os
import json

class StartScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect-4 Start Menu")
        self.root.geometry("800x500")

        # Set up a responsive grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=1)
        self.root.rowconfigure(5, weight=1)

        self.TITLE_ROW = 0
        self.PLAYER_ROW = 1
        self.TYPE_ROW = 2
        self.ALGORITHM_ROW = 3
        self.METHOD_ROW = 4
        self.AMOUNT_ROW = 5
        self.DEPTH_ROW = 6
        self.DATABASE_ROW = 7
        self.BUTTON_ROW = 8

        self.player_type = [tk.StringVar(value="Human"), tk.StringVar(value="Human")]
        self.algorithm = [tk.StringVar(value="Hybrid"), tk.StringVar(value="Hybrid")]
        self.method = [tk.StringVar(value="Time"), tk.StringVar(value="Time")]
        self.mcts_amount = [tk.StringVar(value="1"), tk.StringVar(value="1")]
        self.minimax_depth = [tk.StringVar(value="1"), tk.StringVar(value="1")]
        self.use_database = [tk.BooleanVar(value=False), tk.BooleanVar(value=False)]

        # Initialize AI option widgets for later use
        self.method_label = [None, None]
        self.method_options = [None, None]
        self.mcts_amount_label = [None, None]
        self.mcts_amount_entry = [None, None]
        self.minimax_depth_label = [None, None]
        self.minimax_depth_entry = [None, None]
        self.use_database_checkbox = [None, None]
        self.use_database_checkbox_tooltip = [None, None]

        # Initialize customization variables
        self.player1_colour = "#FF0000"  # Default Red
        self.player2_colour = "#FFFF00"  # Default Yellow
        self.no_chip_colour = "#FFFFFF"  # Default White
        self.board_colour = "#0000FF"  # Default Blue
        self.chip_sound_path = r"./SaveData/sounds/chipdrop_8bit.mp3"
        self.result_sound_path = r"./SaveData/sounds/endgame_8bit.mp3"

        # Load settings from previous session if available
        self.load_settings()

    def show_start_screen(self):
        # Title
        title_label = tk.Label(self.root, text="Connect-4", font=("monospace", 35))
        title_label.grid(row=self.TITLE_ROW, column=0, columnspan=2, pady=20, sticky="n")

        # Player 1 configuration
        self.create_player_options(1)

        # Player 2 configuration
        self.create_player_options(2)

        # Start Button
        start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        start_button.grid(row=self.BUTTON_ROW, column=1, pady=20)

        # Customization Button
        customization_button = tk.Button(self.root, text="Customization", command=self.show_customization_options)
        customization_button.grid(row=self.BUTTON_ROW, column=0, pady=20)

        self.root.mainloop()
        return self.player1, self.player2

    def create_player_options(self, player):

        column = player - 1
        # Player label
        player_label = tk.Label(self.root, text="Player 1" if player == 1 else "Player 2", font=("monospace", 25))
        player_label.grid(row=self.PLAYER_ROW, column=column, pady=10)

        # Player type radio buttons
        type_label = tk.Label(self.root, text="Player Type:", font=("monospace", 15))
        type_label.grid(row=self.TYPE_ROW, column=column, sticky="w", padx=20)
        human_radio = tk.Radiobutton(self.root, text="Human", variable=self.player_type[column], value="Human", command=self.toggle_player_options)
        human_radio.grid(row=self.TYPE_ROW, column=column, sticky="e", padx=70)
        ai_radio = tk.Radiobutton(self.root, text="AI", variable=self.player_type[column], value="AI", command=self.toggle_player_options)
        ai_radio.grid(row=self.TYPE_ROW, column=column, sticky="e", padx=20)

        # Algorithm dropdown
        algorithm_label = tk.Label(self.root, text="Algorithm Type:", font=("monospace", 15))
        algorithm_label.grid(row=self.ALGORITHM_ROW, column=column, sticky="w", padx=20)
        algorithm_options = ttk.Combobox(self.root, textvariable=self.algorithm[column], values=["Hybrid", "MCTS", "Minimax"], state="readonly", width=15)
        algorithm_options.grid(row=self.ALGORITHM_ROW, column=column, sticky="e", padx=20)
        algorithm_options.bind("<<ComboboxSelected>>", self.toggle_algorithm_options)

        # MCTS options
        self.method_label[column] = tk.Label(self.root, text="MCTS Method:", font=("monospace", 15))
        self.method_label[column].grid(row=self.METHOD_ROW, column=column, sticky="w", padx=20)
        self.method_options[column] = ttk.Combobox(self.root, textvariable=self.method[column], values=["Time (seconds)", "Simulations (int)"], state="readonly", width=15)
        self.method_options[column].grid(row=self.METHOD_ROW, column=column, sticky="e", padx=20)

        self.mcts_amount_label[column] = tk.Label(self.root, text="Method Amount:", font=("monospace", 15))
        self.mcts_amount_label[column].grid(row=self.AMOUNT_ROW, column=column, sticky="w", padx=20)
        self.mcts_amount_entry[column] = tk.Entry(self.root, textvariable=self.mcts_amount[column], width=18)
        self.mcts_amount_entry[column].grid(row=self.AMOUNT_ROW, column=column, sticky="e", padx=20)

        # Minimax options
        self.minimax_depth_label[column] = tk.Label(self.root, text="MiniMax Depth:", font=("monospace", 15))
        self.minimax_depth_label[column].grid(row=self.DEPTH_ROW, column=column, sticky="w", padx=20)
        self.minimax_depth_entry[column] = tk.Entry(self.root, textvariable=self.minimax_depth[column], width=18)
        self.minimax_depth_entry[column].grid(row=self.DEPTH_ROW, column=column, sticky="e", padx=20)

        # Use Database checkbox
        self.use_database_checkbox[column] = tk.Checkbutton(self.root, text="Use Database", variable=self.use_database[column])
        self.use_database_checkbox[column].grid(row=self.DATABASE_ROW, column=column, sticky="w", padx=20)
        self.use_database_checkbox_tooltip[column] = tk.Label(self.root, text="(Gets Harder Over Time)", font=("monospace", 10), fg="grey")
        self.use_database_checkbox_tooltip[column].grid(row=self.DATABASE_ROW, column=column, sticky="e", padx=20)

        self.toggle_player_options()

    # IDK why this doesn't work, but not necessary
    def toggle_player_options(self, event=None):
        for column in [0,1]:
            if self.method_label[column]:
                is_removing = self.player_type[column].get() == "Human"
                for widget in [self.method_label[column], self.method_options[column], self.mcts_amount_label[column],
                               self.mcts_amount_entry[column], self.minimax_depth_label[column], self.minimax_depth_entry[column],
                               self.use_database_checkbox[column], self.use_database_checkbox_tooltip[column]]:
                    widget.grid_remove() if is_removing else widget.grid()

        self.toggle_algorithm_options()

    def toggle_algorithm_options(self, event=None):
        for column in [0,1]:
            algorithm = self.algorithm[column].get()
            if algorithm == "MCTS":
                self.show_mcts_options(column)
                self.hide_minimax_options(column)
            elif algorithm == "Minimax":
                self.hide_mcts_options(column)
                self.show_minimax_options(column)
            else:  # algorithm == "Hybrid":
                self.show_mcts_options(column)
                self.show_minimax_options(column)

    def show_mcts_options(self, column):
        if self.method_label[column]:
            self.method_label[column].grid()
            self.method_options[column].grid()
            self.mcts_amount_label[column].grid()
            self.mcts_amount_entry[column].grid()

    def hide_mcts_options(self, column):
        if self.method_label[column]:
            self.method_label[column].grid_remove()
            self.method_options[column].grid_remove()
            self.mcts_amount_label[column].grid_remove()
            self.mcts_amount_entry[column].grid_remove()

    def show_minimax_options(self, column):
        if self.minimax_depth_label[column]:
            self.minimax_depth_label[column].grid()
            self.minimax_depth_entry[column].grid()

    def hide_minimax_options(self, column):
        if self.minimax_depth_label[column]:
            self.minimax_depth_label[column].grid_remove()
            self.minimax_depth_entry[column].grid_remove()

    def start_game(self):
        if not self.validate_inputs():
            return

        self.player1 = self.create_player(player_num=1, player_type=self.player_type[0].get(), algorithm=self.algorithm[0].get(),
                                     method=self.method[0].get(), mcts_amount=self.mcts_amount[0].get(),
                                     minimax_depth=self.minimax_depth[0].get(), use_database=self.use_database[0].get())
        self.player2 = self.create_player(player_num=2, player_type=self.player_type[1].get(), algorithm=self.algorithm[1].get(),
                                     method=self.method[1].get(), mcts_amount=self.mcts_amount[1].get(),
                                     minimax_depth=self.minimax_depth[1].get(), use_database=self.use_database[1].get())
        # Save current settings to JSON
        self.save_settings()

        self.root.quit()
        self.root.destroy()  # Close the window after starting the game

    def create_player(self, player_num, player_type, algorithm="Hybrid", method="time", mcts_amount="1", minimax_depth="1", use_database=False):
        if player_type == "Human":
            return Player(is_human=True, player_num=player_num)
        else:
            if algorithm == "MCTS":
                return Player(is_human=False, player_num=player_num, algorithm="MCTS", MCTS_method=method, MCTS_amount=int(mcts_amount), use_database=use_database)
            elif algorithm == "Minimax":
                return Player(is_human=False, player_num=player_num, algorithm="Minimax", MINI_depth=int(minimax_depth), use_database=use_database)
            else: # algorithm == "Hybrid":
                return Player(is_human=False, player_num=player_num, algorithm="Hybrid", MCTS_method=method, MCTS_amount=float(mcts_amount), MINI_depth=int(minimax_depth), use_database=use_database)

    def validate_inputs(self):
        try:
            for column in [0,1]:
                if self.algorithm[column].get() in ["MCTS", "Hybrid"]:
                    if self.method[column].get() == "Time":
                        time_amount = float(self.mcts_amount[column].get())
                        if time_amount <= 0:
                            raise ValueError
                    elif self.method[column].get() == "Simulations":
                        sim_amount = int(self.mcts_amount[column].get())
                        if sim_amount <= 0:
                            raise ValueError
                if self.algorithm[column].get() in ["Minimax", "Hybrid"]:
                    depth = int(self.minimax_depth[column].get())
                    if depth <= 0:
                        raise ValueError
        except ValueError:
            self.show_error_screen("Invalid input. Please enter positive numbers for Amount and Depth.")
            return False
        return True

    def show_error_screen(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.title("Input Error")
        tk.Label(error_window, text=message, fg="red").pack(pady=20)
        tk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)

    def show_customization_options(self):
        customization_window = tk.Toplevel(self.root)
        customization_window.title("Customization Options")

        # Colour selection for Player 1 chips
        player1_colour_button = tk.Button(customization_window, text="Player 1 Chip Colour",
                                         command=self.select_player1_colour)
        player1_colour_button.grid(row=0, column=0, padx=10, pady=10)
        self.player1_colour_preview = tk.Label(customization_window, text=" ", bg=self.player1_colour, width=10)
        self.player1_colour_preview.grid(row=0, column=1)

        # Colour selection for Player 2 chips
        player2_colour_button = tk.Button(customization_window, text="Player 2 Chip Colour",
                                         command=self.select_player2_colour)
        player2_colour_button.grid(row=1, column=0, padx=10, pady=10)
        self.player2_colour_preview = tk.Label(customization_window, text=" ", bg=self.player2_colour, width=10)
        self.player2_colour_preview.grid(row=1, column=1)

        # Colour selection for No chips slot
        no_chip_colour_button = tk.Button(customization_window, text="No Chip Slot Colour",
                                         command=self.select_no_chip_colour)
        no_chip_colour_button.grid(row=2, column=0, padx=10, pady=10)
        self.no_chip_colour_preview = tk.Label(customization_window, text=" ", bg=self.no_chip_colour, width=10)
        self.no_chip_colour_preview.grid(row=2, column=1)

        # Colour selection for Board
        board_colour_button = tk.Button(customization_window, text="Board Colour", command=self.select_board_colour)
        board_colour_button.grid(row=3, column=0, padx=10, pady=10)
        self.board_colour_preview = tk.Label(customization_window, text=" ", bg=self.board_colour, width=10)
        self.board_colour_preview.grid(row=3, column=1)

        # Sound selection for Chip placement
        chip_sound_button = tk.Button(customization_window, text="Select Chip Placement Sound",
                                      command=self.select_chip_sound)
        chip_sound_button.grid(row=4, column=0, padx=10, pady=10)
        self.chip_sound_preview = tk.Button(customization_window, text="Play Chip Sound", command=self.play_chip_sound)
        self.chip_sound_preview.grid(row=4, column=1)

        # Sound selection for Winning/Draw/Losing sound
        result_sound_button = tk.Button(customization_window, text="Select Result Sound",
                                        command=self.select_result_sound)
        result_sound_button.grid(row=5, column=0, padx=10, pady=10)
        self.result_sound_preview = tk.Button(customization_window, text="Play Result Sound", command=self.play_result_sound)
        self.result_sound_preview.grid(row=5, column=1)

        close_button = tk.Button(customization_window, text="Close", command=customization_window.destroy)
        close_button.grid(row=6, column=0, pady=20)

    def select_player1_colour(self):
        colour = colorchooser.askcolor(title="Choose Player 1 Chip Colour")[1]
        if colour:
            self.player1_colour = colour
            self.player1_colour_preview.config(bg=colour)

    def select_player2_colour(self):
        colour = colorchooser.askcolor(title="Choose Player 2 Chip Colour")[1]
        if colour:
            self.player2_colour = colour
            self.player2_colour_preview.config(bg=colour)

    def select_no_chip_colour(self):
        colour = colorchooser.askcolor(title="Choose No Chip Slot Colour")[1]
        if colour:
            self.no_chip_colour = colour
            self.no_chip_colour_preview.config(bg=colour)

    def select_board_colour(self):
        colour = colorchooser.askcolor(title="Choose Board Colour")[1]
        if colour:
            self.board_colour = colour
            self.board_colour_preview.config(bg=colour)

    def select_chip_sound(self):
        path = filedialog.askopenfilename(title="Select Chip Placement Sound",
                                          filetypes=[("Sound files", "*.wav *.mp3")])
        if path:
            self.chip_sound_path = path
            self.chip_sound_preview.config(text=os.path.basename(path))

    def select_result_sound(self):
        path = filedialog.askopenfilename(title="Select Result Sound", filetypes=[("Sound files", "*.wav *.mp3")])
        if path:
            self.result_sound_path = path
            self.result_sound_preview.config(text=os.path.basename(path))

    def play_chip_sound(self):
        if self.chip_sound_path:
            pygame.mixer.init()
            pygame.mixer.music.load(self.chip_sound_path)
            pygame.mixer.music.play()

    def play_result_sound(self):
        if self.result_sound_path:
            pygame.mixer.init()
            pygame.mixer.music.load(self.result_sound_path)
            pygame.mixer.music.play()

    def save_settings(self):
        settings = {
            "player1_colour": self.player1_colour,
            "player2_colour": self.player2_colour,
            "no_chip_colour": self.no_chip_colour,
            "board_colour": self.board_colour,
            "chip_sound_path": self.chip_sound_path,
            "result_sound_path": self.result_sound_path,

            "player_type": [self.player_type[0].get(), self.player_type[1].get()],
            "algorithm": [self.algorithm[0].get(), self.algorithm[1].get()],
            "method": [self.method[0].get(), self.method[1].get()],
            "mcts_amount": [self.mcts_amount[0].get(), self.mcts_amount[1].get()],
            "minimax_depth": [self.minimax_depth[0].get(), self.minimax_depth[1].get()],
            "use_database": [self.use_database[0].get(), self.use_database[1].get()],
        }

        os.makedirs("../SaveData", exist_ok=True)
        with open(os.path.join("../SaveData", "settings.json"), "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open(os.path.join("../SaveData", "settings.json"), "r") as f:
                settings = json.load(f)
                self.player1_colour = settings.get("player1_colour", self.player1_colour)
                self.player2_colour = settings.get("player2_colour", self.player2_colour)
                self.no_chip_colour = settings.get("no_chip_colour", self.no_chip_colour)
                self.board_colour = settings.get("board_colour", self.board_colour)
                self.chip_sound_path = settings.get("chip_sound_path", self.chip_sound_path)
                self.result_sound_path = settings.get("result_sound_path", self.result_sound_path)

                for column in [0,1]:
                    self.player_type[column].set(settings.get("player_type")[column])
                    self.algorithm[column].set(settings.get("algorithm")[column])
                    self.method[column].set(settings.get("method")[column])
                    self.mcts_amount[column].set(settings.get("mcts_amount")[column])
                    self.minimax_depth[column].set(settings.get("minimax_depth")[column])
                    self.use_database[column].set(settings.get("use_database")[column])
        except FileNotFoundError:
            pass

