import tkinter as tk
from tkinter import messagebox


# -----------------------------
# Game Settings
# -----------------------------
ROWS = 6
COLUMNS = 7
CELL_SIZE = 80

BOARD_WIDTH = COLUMNS * CELL_SIZE
BOARD_HEIGHT = ROWS * CELL_SIZE

EMPTY = 0
PLAYER_ONE = 1
PLAYER_TWO = 2

PLAYER_COLORS = {
    PLAYER_ONE: "#FACC15",  # Yellow
    PLAYER_TWO: "#EF4444",  # Red
}

PLAYER_NAMES = {
    PLAYER_ONE: "Player 1",
    PLAYER_TWO: "Player 2",
}

WINDOW_BG = "#111827"
PANEL_BG = "#1F2937"
BOARD_COLOR = "#2563EB"
EMPTY_SLOT_COLOR = "#E5E7EB"
TEXT_COLOR = "#F9FAFB"
BUTTON_BG = "#10B981"
BUTTON_ACTIVE_BG = "#059669"
WIN_HIGHLIGHT = "#22C55E"


class ConnectFourGame:
    """Main class for the Connect Four game."""

    def __init__(self, root):
        """Set up the game window, variables, and GUI."""
        self.root = root
        self.root.title("Connect Four")
        self.root.resizable(False, False)
        self.root.configure(bg=WINDOW_BG)

        self.board = []
        self.current_player = PLAYER_ONE
        self.game_over = False

        self.scores = {
            PLAYER_ONE: 0,
            PLAYER_TWO: 0,
        }

        self.create_widgets()
        self.restart_game()

    def create_widgets(self):
        """Create title, scoreboard, turn label, board, and restart button."""
        title_label = tk.Label(
            self.root,
            text="Connect Four",
            font=("Arial", 28, "bold"),
            bg=WINDOW_BG,
            fg=TEXT_COLOR,
        )
        title_label.pack(pady=(18, 8))

        top_panel = tk.Frame(self.root, bg=PANEL_BG)
        top_panel.pack(fill="x", padx=18, pady=(0, 12))

        self.score_label = tk.Label(
            top_panel,
            font=("Arial", 15, "bold"),
            bg=PANEL_BG,
            fg=TEXT_COLOR,
        )
        self.score_label.pack(side="left", padx=16, pady=12)

        self.turn_label = tk.Label(
            top_panel,
            font=("Arial", 15, "bold"),
            bg=PANEL_BG,
            fg=TEXT_COLOR,
        )
        self.turn_label.pack(side="right", padx=16, pady=12)

        self.canvas = tk.Canvas(
            self.root,
            width=BOARD_WIDTH,
            height=BOARD_HEIGHT,
            bg=BOARD_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack(padx=18)

        self.canvas.bind("<Button-1>", self.handle_board_click)

        restart_button = tk.Button(
            self.root,
            text="Restart Game",
            font=("Arial", 14, "bold"),
            bg=BUTTON_BG,
            fg=TEXT_COLOR,
            activebackground=BUTTON_ACTIVE_BG,
            activeforeground=TEXT_COLOR,
            relief=tk.FLAT,
            padx=18,
            pady=8,
            command=self.restart_game,
        )
        restart_button.pack(pady=18)

    def restart_game(self):
        """Reset the board and start a new round."""
        self.board = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_player = PLAYER_ONE
        self.game_over = False

        self.update_labels()
        self.draw_board()

    def update_labels(self):
        """Update scoreboard and current turn display."""
        self.score_label.config(
            text=f"Player 1: {self.scores[PLAYER_ONE]}   Player 2: {self.scores[PLAYER_TWO]}"
        )

        self.turn_label.config(
            text=f"Turn: {PLAYER_NAMES[self.current_player]}",
            fg=PLAYER_COLORS[self.current_player],
        )

    def draw_board(self, winning_cells=None):
        """Draw the board and all pieces."""
        self.canvas.delete("all")

        for row in range(ROWS):
            for col in range(COLUMNS):
                x1 = col * CELL_SIZE + 8
                y1 = row * CELL_SIZE + 8
                x2 = x1 + CELL_SIZE - 16
                y2 = y1 + CELL_SIZE - 16

                cell_value = self.board[row][col]

                if cell_value == PLAYER_ONE:
                    piece_color = PLAYER_COLORS[PLAYER_ONE]
                elif cell_value == PLAYER_TWO:
                    piece_color = PLAYER_COLORS[PLAYER_TWO]
                else:
                    piece_color = EMPTY_SLOT_COLOR

                if winning_cells and (row, col) in winning_cells:
                    outline_color = WIN_HIGHLIGHT
                    outline_width = 5
                else:
                    outline_color = BOARD_COLOR
                    outline_width = 2

                self.canvas.create_oval(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=piece_color,
                    outline=outline_color,
                    width=outline_width,
                )

    def handle_board_click(self, event):
        """Drop a piece in the selected column."""
        if self.game_over:
            return

        selected_column = event.x // CELL_SIZE

        if selected_column < 0 or selected_column >= COLUMNS:
            return

        row = self.get_open_row(selected_column)

        if row is None:
            messagebox.showwarning("Column Full", "Please choose another column.")
            return

        self.board[row][selected_column] = self.current_player

        winning_cells = self.get_winning_cells(row, selected_column)

        if winning_cells:
            self.handle_win(winning_cells)
        elif self.is_draw():
            self.handle_draw()
        else:
            self.switch_player()
            self.draw_board()

    def get_open_row(self, column):
        """Find the lowest empty row in a column."""
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][column] == EMPTY:
                return row

        return None

    def switch_player(self):
        """Switch turns between Player 1 and Player 2."""
        if self.current_player == PLAYER_ONE:
            self.current_player = PLAYER_TWO
        else:
            self.current_player = PLAYER_ONE

        self.update_labels()

    def get_winning_cells(self, row, column):
        """Check if the latest move made a winning line."""
        directions = [
            (0, 1),    # Horizontal
            (1, 0),    # Vertical
            (1, 1),    # Diagonal down-right
            (1, -1),   # Diagonal down-left
        ]

        for row_step, col_step in directions:
            connected_cells = self.collect_connected_cells(
                row,
                column,
                row_step,
                col_step,
            )

            if len(connected_cells) >= 4:
                return connected_cells[:4]

        return None

    def collect_connected_cells(self, row, column, row_step, col_step):
        """Collect connected pieces in both directions."""
        player = self.board[row][column]
        connected_cells = [(row, column)]

        connected_cells += self.collect_direction(
            row,
            column,
            row_step,
            col_step,
            player,
        )

        connected_cells += self.collect_direction(
            row,
            column,
            -row_step,
            -col_step,
            player,
        )

        return connected_cells

    def collect_direction(self, row, column, row_step, col_step, player):
        """Collect matching pieces in one direction."""
        cells = []
        current_row = row + row_step
        current_column = column + col_step

        while self.is_inside_board(current_row, current_column):
            if self.board[current_row][current_column] != player:
                break

            cells.append((current_row, current_column))

            current_row += row_step
            current_column += col_step

        return cells

    def is_inside_board(self, row, column):
        """Check whether a position is inside the board."""
        return 0 <= row < ROWS and 0 <= column < COLUMNS

    def is_draw(self):
        """Check if the board is full."""
        for col in range(COLUMNS):
            if self.board[0][col] == EMPTY:
                return False

        return True

    def handle_win(self, winning_cells):
        """End the round when a player wins."""
        self.game_over = True
        self.scores[self.current_player] += 1

        winner_name = PLAYER_NAMES[self.current_player]

        self.update_labels()
        self.draw_board(winning_cells)

        messagebox.showinfo("Game Over", f"{winner_name} wins!")

    def handle_draw(self):
        """End the round when the game is a draw."""
        self.game_over = True
        self.draw_board()
        messagebox.showinfo("Game Over", "It's a draw!")


# -----------------------------
# Start the game
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    game = ConnectFourGame(root)
    root.mainloop()