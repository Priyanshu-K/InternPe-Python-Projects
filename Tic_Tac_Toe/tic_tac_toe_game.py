"""
Tic Tac Toe game using Tkinter.

This program creates a simple two-player Tic Tac Toe game with a graphical
interface. Players X and O take turns, and the game checks for wins and draws.
"""

import tkinter as tk
from tkinter import messagebox


# ----------------------------- Game Constants -----------------------------
# These values make the code easier to update and keep the design consistent.
WINDOW_BG = "#111827"
BOARD_BG = "#1F2937"
BUTTON_BG = "#374151"
BUTTON_ACTIVE_BG = "#4B5563"
TEXT_COLOR = "#F9FAFB"
X_COLOR = "#38BDF8"
O_COLOR = "#F472B6"
WIN_COLOR = "#22C55E"
FONT_TITLE = ("Segoe UI", 24, "bold")
FONT_STATUS = ("Segoe UI", 16)
FONT_BUTTON = ("Segoe UI", 34, "bold")


# ----------------------------- Main Game Class -----------------------------
# The class groups all game data and GUI behavior in one organized place.
class TicTacToeGame:
    """Create and manage a two-player Tic Tac Toe game."""

    def __init__(self, root):
        """Set up the window, game state, and interface widgets."""
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("430x560")
        self.root.resizable(False, False)
        self.root.configure(bg=WINDOW_BG)

        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = []
        self.game_over = False

        self.create_widgets()

    def create_widgets(self):
        """Create the title, status label, 3x3 button grid, and restart button."""
        title_label = tk.Label(
            self.root,
            text="Tic Tac Toe",
            font=FONT_TITLE,
            bg=WINDOW_BG,
            fg=TEXT_COLOR,
        )
        title_label.pack(pady=(25, 8))

        self.status_label = tk.Label(
            self.root,
            text="Player X's turn",
            font=FONT_STATUS,
            bg=WINDOW_BG,
            fg=TEXT_COLOR,
        )
        self.status_label.pack(pady=(0, 20))

        board_frame = tk.Frame(self.root, bg=BOARD_BG)
        board_frame.pack()

        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(
                    board_frame,
                    text="",
                    width=4,
                    height=2,
                    font=FONT_BUTTON,
                    bg=BUTTON_BG,
                    fg=TEXT_COLOR,
                    activebackground=BUTTON_ACTIVE_BG,
                    activeforeground=TEXT_COLOR,
                    relief=tk.FLAT,
                    command=lambda r=row, c=col: self.handle_cell_click(r, c),
                )
                button.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(button)
            self.buttons.append(button_row)

        restart_button = tk.Button(
            self.root,
            text="Restart Game",
            font=("Segoe UI", 14, "bold"),
            bg="#2563EB",
            fg=TEXT_COLOR,
            activebackground="#1D4ED8",
            activeforeground=TEXT_COLOR,
            relief=tk.FLAT,
            padx=18,
            pady=8,
            command=self.restart_game,
        )
        restart_button.pack(pady=28)

    def handle_cell_click(self, row, col):
        """Handle a player's move when they click an empty cell."""
        if self.game_over or self.board[row][col] != "":
            return

        self.board[row][col] = self.current_player
        self.buttons[row][col].config(
            text=self.current_player,
            fg=X_COLOR if self.current_player == "X" else O_COLOR,
        )

        winning_cells = self.get_winning_cells()
        if winning_cells:
            self.announce_winner(winning_cells)
        elif self.is_draw():
            self.announce_draw()
        else:
            self.switch_player()

    def switch_player(self):
        """Change the current player and update the turn display."""
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(text=f"Player {self.current_player}'s turn")

    def get_winning_cells(self):
        """Return the winning cells if a player has three in a row."""
        possible_wins = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]

        for cells in possible_wins:
            first_cell = self.board[cells[0][0]][cells[0][1]]
            if first_cell and all(self.board[row][col] == first_cell for row, col in cells):
                return cells

        return None

    def is_draw(self):
        """Return True when every cell is filled and nobody has won."""
        return all(self.board[row][col] != "" for row in range(3) for col in range(3))

    def announce_winner(self, winning_cells):
        """End the game, highlight the winning line, and show a winner message."""
        self.game_over = True
        self.status_label.config(text=f"Player {self.current_player} wins!")

        for row, col in winning_cells:
            self.buttons[row][col].config(bg=WIN_COLOR)

        messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")

    def announce_draw(self):
        """End the game and show a draw message."""
        self.game_over = True
        self.status_label.config(text="It's a draw!")
        messagebox.showinfo("Game Over", "It's a draw!")

    def restart_game(self):
        """Reset the board and start a fresh game with Player X."""
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.status_label.config(text="Player X's turn")

        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", bg=BUTTON_BG, fg=TEXT_COLOR)


# ----------------------------- Application Start -----------------------------
# Create the Tkinter window, build the game, and start the GUI event loop.
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()