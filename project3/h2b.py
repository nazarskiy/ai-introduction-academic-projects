import tkinter as tk
from pos import CPos
from board import CBoard
from game import CGame

class CHuman2Bot:
    def __init__(self, root, size: int = 6, human_is_white: bool = True):
        self.m_root = root
        self.m_size = size
        self.human_is_white = human_is_white
        self.bot_is_white = not human_is_white
        self.m_game = CGame(CBoard(root, size))
        self.m_selected_pos = None
        self.m_game.m_board.set_click_callback(self.on_tile_click)
        self.m_game.m_board.draw()

        if not self.human_is_white:
            self.m_root.after(300, self.play_bot_turn)

    def on_tile_click(self, pos: CPos):
        if self.m_game.is_game_over():
            print("Game over")
            self.show_game_over()
            return

        if self.m_selected_pos is None:
            if pos.m_blank or not pos.m_checker:
                return
            if pos.m_checker.m_white == self.human_is_white:
                self.m_selected_pos = pos
        else:
            all_moves = self.m_game.all_valid_moves(self.human_is_white)

            for path, captured in all_moves:
                if path and path[0] == (self.m_selected_pos.m_r, self.m_selected_pos.m_c) and path[-1] == (pos.m_r, pos.m_c):
                    move = path
                    self.m_game.make_move((move, captured))
                    self.m_selected_pos = None
                    self.m_game.m_board.draw()
                    self.m_root.after(500, self.play_bot_turn)
                    return

            self.m_selected_pos = None

    def play_bot_turn(self):
        if self.m_game.is_game_over():
            print("Game over")
            self.show_game_over()
            return

        move = self.m_game.best_move(is_white=self.bot_is_white, depth=1)
        if move:
            self.m_game.make_move(move)
            self.m_game.m_board.draw()

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
