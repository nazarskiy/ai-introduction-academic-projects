import tkinter as tk
import numpy as np
from comchecker import CComchecker
from king import CKing
from pos import CPos

CELL_SIZE = 60
WHITE_COLOR = "#eeeeee"
BLACK_COLOR = "#333333"
GRID_COLOR = "#888888"

class CBoard:
    def __init__(self, root, size: int = 4):
        assert(size in [4, 6, 8])
        self.m_size = size
        self.m_board = np.empty((size, size), dtype=object)
        white_zone = range(int(size/2 - 1))
        black_zone = range(int(size/2 + 1), size)
        for r in range(size):
            for c in range(size):
                checker = None
                if r in white_zone and (r + c) % 2 == 0: checker = CComchecker(True)
                elif r in black_zone and (r + c) % 2 == 0: checker = CComchecker(False)

                self.m_board[r, c] = CPos(r, c, checker is None, checker)

        self.m_root = root
        self.m_canvas = tk.Canvas(root, width=size * CELL_SIZE, height=size * CELL_SIZE, bg="white")
        self.m_canvas.pack()
        self.m_click_callback = None
        self.m_canvas.bind("<Button-1>", self._on_click)

    def __getitem__(self, idx) -> CPos:
        return self.m_board[idx]

    def clone_without_gui(self):
        new_board = CBoard.__new__(CBoard)
        new_board.m_size = self.m_size
        new_board.m_board = np.empty_like(self.m_board, dtype=object)
        for r in range(self.m_size):
            for c in range(self.m_size):
                pos = self.m_board[r, c]
                checker = None
                if pos.m_checker:
                    checker = pos.m_checker.clone()
                new_board.m_board[r, c] = CPos(r, c, pos.m_blank, checker)
        return new_board

    def in_boundaries(self, r: int, c: int) -> bool:
        return 0 <= r <= self.m_size - 1 and 0 <= c <= self.m_size - 1

    def set_click_callback(self, callback):
        self.m_click_callback = callback

    def _on_click(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if self.in_boundaries(row, col) and self.m_click_callback:
            self.m_click_callback(self.m_board[row, col])

    def draw(self):
        self.m_canvas.delete("all")
        for r in range(self.m_size):
            for c in range(self.m_size):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                self.m_canvas.create_rectangle(x1, y1, x2, y2, fill=WHITE_COLOR, outline=GRID_COLOR)

                pos = self.m_board[r, c]
                checker = pos.m_checker
                if checker:
                    color = "white" if checker.m_white else "black"
                    outline = "black" if checker.m_white else "white"
                    self.m_canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill=color, outline=outline)

                    if isinstance(checker, CKing):
                        self.m_canvas.create_text(
                            (x1 + x2) // 2,
                            (y1 + y2) // 2,
                            text="K",
                            fill=outline,
                            font=("Arial", 16, "bold")
                        )
