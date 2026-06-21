import random
import tkinter as tk
from tkinter import messagebox


# -----------------------------
# Game settings
# -----------------------------
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
CELL_SIZE = 20
SPEED = 120

BG_COLOR = "#111827"
SNAKE_COLOR = "#22c55e"
FOOD_COLOR = "#ef4444"
TEXT_COLOR = "#ffffff"


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")

        self.canvas = tk.Canvas(
            root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg=BG_COLOR,
            highlightthickness=0
        )
        self.canvas.pack()

        self.score_label = tk.Label(
            root,
            text="Score: 0",
            font=("Arial", 16, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        self.score_label.pack(fill="x")

        self.root.bind("<KeyPress>", self.change_direction)

        self.restart_game()

    def restart_game(self):
        """Start or restart the game."""
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.next_direction = "Right"
        self.score = 0
        self.game_over = False

        self.score_label.config(text="Score: 0")
        self.create_food()
        self.update_game()

    def create_food(self):
        """Create food at a random position."""
        while True:
            x = random.randrange(0, WINDOW_WIDTH, CELL_SIZE)
            y = random.randrange(0, WINDOW_HEIGHT, CELL_SIZE)

            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def change_direction(self, event):
        """Change snake direction using arrow keys."""
        key = event.keysym

        if key == "Up" and self.direction != "Down":
            self.next_direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.next_direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.next_direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.next_direction = "Right"

    def move_snake(self):
        """Move the snake one step forward."""
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            new_head = (head_x, head_y - CELL_SIZE)
        elif self.direction == "Down":
            new_head = (head_x, head_y + CELL_SIZE)
        elif self.direction == "Left":
            new_head = (head_x - CELL_SIZE, head_y)
        else:
            new_head = (head_x + CELL_SIZE, head_y)

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.create_food()
        else:
            self.snake.pop()

    def check_collision(self):
        """Check if the snake hits the wall or itself."""
        head_x, head_y = self.snake[0]

        hit_wall = (
            head_x < 0
            or head_x >= WINDOW_WIDTH
            or head_y < 0
            or head_y >= WINDOW_HEIGHT
        )

        hit_self = self.snake[0] in self.snake[1:]

        return hit_wall or hit_self

    def draw_game(self):
        """Draw the snake, food, and background."""
        self.canvas.delete("all")

        for x, y in self.snake:
            self.canvas.create_rectangle(
                x,
                y,
                x + CELL_SIZE,
                y + CELL_SIZE,
                fill=SNAKE_COLOR,
                outline=BG_COLOR
            )

        food_x, food_y = self.food
        self.canvas.create_oval(
            food_x,
            food_y,
            food_x + CELL_SIZE,
            food_y + CELL_SIZE,
            fill=FOOD_COLOR,
            outline=BG_COLOR
        )

    def update_game(self):
        """Keep the game running until Game Over."""
        if self.game_over:
            return

        self.move_snake()

        if self.check_collision():
            self.game_over = True
            answer = messagebox.askyesno(
                "Game Over",
                f"Your score: {self.score}\n\nDo you want to restart?"
            )

            if answer:
                self.restart_game()
            else:
                self.root.destroy()
            return

        self.draw_game()
        self.root.after(SPEED, self.update_game)


# -----------------------------
# Start the program
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()