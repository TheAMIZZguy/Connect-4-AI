import tkinter as tk

class EndScreen:
    def __init__(self, winner):
        self.root = tk.Tk()
        self.root.title("Game Over")
        self.root.geometry("400x200")

        # Display the winner
        if winner is None:
            message = "It's a Draw!"
        else:
            message = f"Player {winner} Wins!"

        tk.Label(self.root, text=message, font=("Arial", 24)).pack(pady=20)

        # Play Again Button
        play_again_button = tk.Button(self.root, text="Play Again", command=self.play_again)
        play_again_button.pack(side="left", padx=20, pady=20)

        # Quit Button
        quit_button = tk.Button(self.root, text="Quit", command=self.quit_game)
        quit_button.pack(side="right", padx=20, pady=20)

    def show_end_screen(self):
        self.root.mainloop()
        return self.is_playing

    def play_again(self):
        self.is_playing = True
        self.root.quit()
        self.root.destroy()

    def quit_game(self):
        self.is_playing = False
        self.root.quit()