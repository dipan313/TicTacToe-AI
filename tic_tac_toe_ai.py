import tkinter as tk
from tkinter import messagebox
import random

# Initialize the board
board = [" " for _ in range(9)]

# Function to check for a win or draw
def check_winner():
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6)             # diagonals
    ]
    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    if " " not in board:
        return "Draw"
    return None

# AI move based on difficulty
def ai_move(difficulty):
    if difficulty == "Easy":
        return easy_ai()
    elif difficulty == "Medium":
        return medium_ai()
    elif difficulty == "Hard":
        return hard_ai()

# Easy AI: Random move
def easy_ai():
    empty_cells = [i for i, cell in enumerate(board) if cell == " "]
    return random.choice(empty_cells) if empty_cells else None

# Medium AI: Block player or random move
def medium_ai():
    # Block the player if they're about to win
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            if check_winner() == "X":
                board[i] = " "  # Reset cell
                return i
            board[i] = " "
    # Otherwise, play randomly
    return easy_ai()

# Hard AI: Minimax algorithm
def minimax(is_maximizing):
    winner = check_winner()
    if winner == "X":
        return -1
    elif winner == "O":
        return 1
    elif " " not in board:
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(False)
                board[i] = " "
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(True)
                board[i] = " "
                best_score = min(best_score, score)
        return best_score

def hard_ai():
    best_score = -float("inf")
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

# Handle player's move
def make_move(index, player):
    if board[index] == " ":
        board[index] = player
        buttons[index].config(text=player, state="disabled",
                              disabledforeground="blue" if player == "X" else "red")
        winner = check_winner()
        if winner:
            end_game(winner)
        elif player == "X":  # If player moved, AI should play next
            ai_index = ai_move(current_difficulty)
            if ai_index is not None:
                make_move(ai_index, "O")

# End the game
def end_game(winner):
    if winner == "Draw":
        messagebox.showinfo(
            "Game Over",
            "🤝 It's a draw! Great minds think alike!\nplay again"
        )
    elif winner == "X":
        messagebox.showinfo(
            "Congratulations!",
            "🎉 You win! 🏆\n\nYou're a Tic Tac Toe master!\n\nReady for another victory?"
        )
    elif winner == "O":
        messagebox.showinfo(
            "Game Over",
            "😏 AI wins! 🤖\n\nBetter luck next time, human!\n\nThink you can outsmart me in the next game?"
        )
    reset_board()

# Reset the board and restart the game
def reset_board():
    global board
    board = [" " for _ in range(9)]
    for btn in buttons:
        btn.config(text=" ", state="normal")

# Restart the game to difficulty selection
def restart_game():
    global board
    board = [" " for _ in range(9)]
    for btn in buttons:
        btn.destroy()  # Remove all buttons
    restart_button.pack_forget()  # Hide the Restart button
    difficulty_frame.pack()  # Show the difficulty selection frame

# Create the game window
root = tk.Tk()
root.title("Tic Tac Toe")

# Ask for difficulty level
def choose_difficulty(level):
    global current_difficulty
    current_difficulty = level
    difficulty_frame.pack_forget()
    create_board()

difficulty_frame = tk.Frame(root)
tk.Label(difficulty_frame, text="Choose Difficulty:", font=("Helvetica", 16)).pack(pady=10)
tk.Button(difficulty_frame, text="Easy", font=("Helvetica", 14), command=lambda: choose_difficulty("Easy"), bg="lightgreen").pack(pady=5)
tk.Button(difficulty_frame, text="Medium", font=("Helvetica", 14), command=lambda: choose_difficulty("Medium"), bg="yellow").pack(pady=5)
tk.Button(difficulty_frame, text="Hard", font=("Helvetica", 14), command=lambda: choose_difficulty("Hard"), bg="red").pack(pady=5)
difficulty_frame.pack()

# Create the game board
def create_board():
    global buttons
    buttons = []
    for i in range(9):
        btn = tk.Button(root, text=" ", font=("Helvetica", 24), height=2, width=5, bg="lightblue",
                        command=lambda i=i: make_move(i, "X"))
        btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
        buttons.append(btn)
    restart_button.pack(pady=10)

# Create a Restart button
restart_button = tk.Button(root, text="Restart Game", font=("Helvetica", 14), bg="orange", command=restart_game)

# Start the Tkinter event loop
root.mainloop()