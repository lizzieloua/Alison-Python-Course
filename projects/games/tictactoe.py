import random
import tkinter as tk

# Set up the window
window = tk.Tk()
window.title("Tic Tac Toe")

# Get the width and height of the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the center of the screen
center_x = screen_width // 2
center_y = screen_height // 2

desired_width = 250
desired_height = 300

# Set the window size and position
window.geometry(f"{desired_width}x{desired_height}+{center_x - 125}+{center_y - 150}")

# Set up the game variables
board = [["", "", ""], ["", "", ""], ["", "", ""]]
user = "X"
user_wins = 0
ai = "O"
ai_wins = 0


# Set up the function to handle player moves
def player_move(row, col):
    global user, user_wins

    # Check if the game is already over
    if check_win(user) or check_tie():
        return

    # Check if the cell is already occupied
    if board[row][col] != "":
        result_label.config(text="Space is taken.")
        return
    else:
        result_label.config(text="")

    # Make the move
    board[row][col] = user

    # Update the button text
    buttons[row][col].config(text=user)

    # Check for a win
    if check_win(user):
        result_label.config(text=f"{user} wins!")
        user_wins += 1
        score_label.config(text=f"User: {user_wins} - AI: {ai_wins}")
        reset_button.config(text="New Game")
        return

    # Check for a tie
    if check_tie():
        result_label.config(text="It's a tie!")
        reset_button.config(text="New Game")
        return

    # Make the AI move
    ai_move()


# Set up the function to handle AI moves
def ai_move():
    global ai, ai_wins, result_label

    # Check for a winning move
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = ai
                if check_win(ai):
                    buttons[i][j].config(text=ai)
                    result_label.config(text=f"{ai} wins!")
                    ai_wins += 1
                    score_label.config(text=f"User: {user_wins} - AI: {ai_wins}")
                    reset_button.config(text="New Game")
                    return
                board[i][j] = ""

    # Check for a blocking move
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = user
                if check_win(user):
                    board[i][j] = ai
                    buttons[i][j].config(text=ai)
                    return
                board[i][j] = ""

    # Choose a random open cell
    choices = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                choices.append((i, j))
    i, j = random.choice(choices)
    board[i][j] = ai
    buttons[i][j].config(text=ai)


# Set up the function to check for a win
def check_win(player):
    # Check rows
    for row in board:
        if row == [player, player, player]:
            return True

    # Check columns
    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    # Check diagonals
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False


# Set up the function to check for a tie
def check_tie():
    for row in board:
        if "" in row:
            return False
    return True


# Set up the function to reset the game
def reset_game():
    global board

    board = [["", "", ""], ["", "", ""], ["", "", ""]]

    # Update the button text
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="")

    result_label.config(text="")
    reset_button.config(text="Reset")

# Set up the buttons to represent the game board
buttons = []
for i in range(3):
    button_row = []
    for j in range(3):
        button_row.append(tk.Button(text="", font=("Arial", 32), command=lambda row=i, col=j: player_move(row, col)))
        button_row[-1].grid(row=i, column=j)
    buttons.append(button_row)

# Set up the label to display the result of the game
result_label = tk.Label(text="", font=("Arial", 32))
result_label.grid(row=3, column=0, columnspan=3)

# Set up the button to reset the game
reset_button = tk.Button(text="Reset", font=("Arial", 16), command=reset_game)
reset_button.grid(row=4, column=0)

# Set up the button to quit the game
quit_button = tk.Button(text="Quit", font=("Arial", 16), command=window.destroy)
quit_button.grid(row=4, column=2)

# Set up the score label to display the standings
score_label = tk.Label(text="User: 0 - AI: 0", font=("Arial", 16))
score_label.grid(row=5, column=0, columnspan=3)

# Run the window loop
window.mainloop()
