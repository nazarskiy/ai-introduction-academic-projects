import tkinter as tk
from b2b import CBot2Bot
from h2b import CHuman2Bot

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Checkers")
    type = None
    while type not in ["b2b", "h2b"]:
        type = input("Choose the type of the game (b2b or h2b): ").strip()

    if type == "b2b":
        app = CBot2Bot(root, size=8)
    elif type == "h2b":
        app = CHuman2Bot(root, size=8)

    root.mainloop()
