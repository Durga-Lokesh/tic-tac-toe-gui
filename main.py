import tkinter as tk
from tkinter import messagebox
import random


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("420x550")
        self.root.configure(bg="#1e1e1e")

        self.player_score = 0
        self.computer_score = 0

        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        # Difficulty variable
        self.difficulty = tk.StringVar(value="Easy")

        # Score Label
        self.score_label = tk.Label(
            self.root,
            text="Player: 0  |  Computer: 0",
            font=("Arial", 14, "bold"),
            bg="#1e1e1e",
            fg="white"
        )
        self.score_label.pack(pady=10)

        # Difficulty Dropdown
        self.create_difficulty_menu()

        # Center frame
        self.frame = tk.Frame(self.root, bg="#1e1e1e")
        self.frame.pack(expand=True)

        self.create_board()
        self.create_restart_button()

    def create_difficulty_menu(self):
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack()

        label = tk.Label(frame, text="Difficulty:", fg="white", bg="#1e1e1e")
        label.pack(side="left", padx=5)

        menu = tk.OptionMenu(frame, self.difficulty, "Easy", "Medium", "Hard")
        menu.config(bg="#444", fg="white")
        menu.pack(side="left")

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.frame,
                    text="",
                    font=("Arial", 32, "bold"),
                    width=4,
                    height=2,
                    bg="#2d2d2d",
                    fg="white",
                    command=lambda i=i, j=j: self.on_click(i, j)
                )

                button.bind("<Enter>", lambda e, b=button: b.config(bg="#444444"))
                button.bind("<Leave>", lambda e, b=button: b.config(bg="#2d2d2d"))

                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = button

    def create_restart_button(self):
        btn = tk.Button(
            self.root,
            text="Restart Game",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.reset_game
        )
        btn.pack(pady=10)

    def update_score(self):
        self.score_label.config(
            text=f"Player: {self.player_score}  |  Computer: {self.computer_score}"
        )

    def flash(self, btn):
        original = btn["bg"]
        btn.config(bg="#00ADB5")
        self.root.after(100, lambda: btn.config(bg=original))

    def highlight(self, cells):
        for i, j in cells:
            self.buttons[i][j].config(bg="#FFD700", fg="black")

    def on_click(self, i, j):
        if self.buttons[i][j]["text"] == "":
            self.buttons[i][j]["text"] = "X"
            self.flash(self.buttons[i][j])

            win = self.check_win("X")
            if win:
                self.highlight(win)
                self.player_score += 1
                self.update_score()
                self.root.after(500, lambda: self.end("🎉 You win!"))
                return

            if self.check_draw():
                self.root.after(300, lambda: self.end("Draw!"))
                return

            self.computer_move()

            win = self.check_win("O")
            if win:
                self.highlight(win)
                self.computer_score += 1
                self.update_score()
                self.root.after(500, lambda: self.end("💻 Computer wins!"))

    # 🧠 AI LOGIC BASED ON DIFFICULTY
    def computer_move(self):
        level = self.difficulty.get()

        if level == "Easy":
            self.random_move()

        elif level == "Medium":
            if random.random() < 0.5:
                self.random_move()
            else:
                self.smart_move()

        else:  # Hard
            self.smart_move()

    def random_move(self):
        empty = [(i, j) for i in range(3) for j in range(3)
                 if self.buttons[i][j]["text"] == ""]

        if empty:
            i, j = random.choice(empty)
            self.buttons[i][j]["text"] = "O"
            self.flash(self.buttons[i][j])

    def smart_move(self):
        # Try to win
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["text"] == "":
                    self.buttons[i][j]["text"] = "O"
                    if self.check_win("O"):
                        self.flash(self.buttons[i][j])
                        return
                    self.buttons[i][j]["text"] = ""

        # Block player
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["text"] == "":
                    self.buttons[i][j]["text"] = "X"
                    if self.check_win("X"):
                        self.buttons[i][j]["text"] = "O"
                        self.flash(self.buttons[i][j])
                        return
                    self.buttons[i][j]["text"] = ""

        # Else random
        self.random_move()

    def check_win(self, player):
        for i in range(3):
            if all(self.buttons[i][j]["text"] == player for j in range(3)):
                return [(i, 0), (i, 1), (i, 2)]

        for j in range(3):
            if all(self.buttons[i][j]["text"] == player for i in range(3)):
                return [(0, j), (1, j), (2, j)]

        if all(self.buttons[i][i]["text"] == player for i in range(3)):
            return [(0, 0), (1, 1), (2, 2)]

        if all(self.buttons[i][2 - i]["text"] == player for i in range(3)):
            return [(0, 2), (1, 1), (2, 0)]

        return None

    def check_draw(self):
        return all(self.buttons[i][j]["text"] != ""
                   for i in range(3) for j in range(3))

    def end(self, msg):
        messagebox.showinfo("Game Over", msg)
        self.reset_game()

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", bg="#2d2d2d", fg="white")


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()