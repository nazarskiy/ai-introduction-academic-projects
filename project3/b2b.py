from board import CBoard
from game import CGame
import time
import tkinter as tk

class CBot2Bot:
    def __init__(self, root, size=6):
        self.m_root = root
        self.m_size = size
        self.m_turn_white = True
        self.m_game = CGame(CBoard(root, size))
        self.m_game.m_board.draw()
        self.m_root.after(300, self.play_turn)

    def play_turn(self):
        time.sleep(0.5)
        if self.m_game.is_game_over():
            print("Game over")
            self.show_game_over()
            return

        move = self.m_game.best_move(is_white=self.m_turn_white, depth=9 if self.m_turn_white else 9)
        if move:
            self.m_game.make_move(move)
            self.m_game.m_board.draw()
        else:
            print("No valid move for", "White" if self.m_turn_white else "Black")

        self.m_turn_white = not self.m_turn_white
        self.m_root.after(800, self.play_turn)

    def show_game_over(self):
        winner = self.m_game.who_winner()
        message = {
            "white": "White won!",
            "black": "Black won!",
            "tie": "It's a tie!"
        }[winner]

        for widget in self.m_root.winfo_children():
            widget.destroy()

        result_label = tk.Label(self.m_root, text=message, font=("Helvetica", 32), bg="white")
        result_label.pack(expand=True, fill="both")