import random
import tkinter
import tkinter as tk


class TicTacToeMenu(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Tic Tac Toe Menu")

        # Set the window size and position
        self.geometry(calc_geometry(window=self, width=250, height=100))

        # Create the main menu frame
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Create the menu label
        menu_label = tk.Label(main_frame, text="Select number of players:")
        menu_label.pack()

        # Create the 1 player button
        one_player_button = tk.Button(main_frame, text="1 Player", command=lambda: self.choose_num_players(1))
        one_player_button.pack()

        # Create the 2 players button
        two_players_button = tk.Button(main_frame, text="2 Players", command=lambda: self.choose_num_players(2))
        two_players_button.pack()

    def choose_num_players(self, num_players: int == 1):
        """ Send the number of players to the TicTacToe game """
        self.destroy()
        game = TicTacToe(selection=num_players)
        game.mainloop()


class TicTacToe(tk.Tk):
    def __init__(self, selection: int == 1):

        # Set up the window
        tk.Tk.__init__(self)
        self.title("Tic Tac Toe")

        # Set the window size and position
        self.geometry(calc_geometry(window=self, width=250, height=300))

        # Set up the game variables
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.user = "X"
        self.user1_wins = 0
        self.user2_wins = 0
        self.ai = "O"
        self.ai_wins = 0
        self.one_player = True if selection == 1 else False

        # Set up the buttons to represent the game board
        self.buttons = []
        for i in range(3):
            button_row = []
            for j in range(3):
                button_row.append(
                    tk.Button(text="", font=("Arial", 32), command=lambda row=i, col=j: self.player_move(row, col)))
                button_row[-1].grid(row=i, column=j)
            self.buttons.append(button_row)

        # Set up the label to display the result of the game
        self.result_label = tk.Label(text="", font=("Arial", 32))
        self.result_label.grid(row=3, column=0, columnspan=3)

        # Set up the button to reset the game
        self.reset_button = tk.Button(text="Reset", font=("Arial", 16), command=self.reset_game)
        self.reset_button.grid(row=4, column=0)

        # Set up the button to quit the game
        self.quit_button = tk.Button(text="Quit", font=("Arial", 16), command=self.destroy)
        self.quit_button.grid(row=4, column=2)

        # Set up the score label to display the standings
        score_message = "User: 0 - AI: 0" if self.one_player else "Player 1: 0 - Player 2: 0"
        self.score_label = tk.Label(text=score_message, font=("Arial", 16))
        self.score_label.grid(row=5, column=0, columnspan=3)

    def player_move(self, row, col):
        """ Set up the function to handle player moves """

        # Check if the game is already over
        if self.check_win(self.user) or self.check_tie():
            return

        # Check if the cell is already occupied
        if self.board[row][col] != "":
            self.result_label.config(text="Space is taken.")
            return
        else:
            self.result_label.config(text="")

        # Make the move
        self.board[row][col] = self.user

        # Update the button text
        self.buttons[row][col].config(text=self.user)

        # Check for a win
        if self.check_win(self.user):
            self.result_label.config(text=f"{'Player 1' if self.user == 'X' else 'Player 2'} Wins!")
            self.reset_button.config(text="New Game")
            
            if self.one_player:
                self.user1_wins += 1
            else:
                if self.user == "X":
                    self.user1_wins += 1
                else:
                    self.user2_wins += 1
            
            score_message = (
                f"User: {self.user1_wins} - AI: {self.ai_wins}" 
                if self.one_player else 
                f"Player 1: {self.user1_wins} - Player 2: {self.user2_wins}")
            self.score_label.config(text=score_message)

            return

        # Check for a tie
        if self.check_tie():
            self.result_label.config(text="It's a tie!")
            self.reset_button.config(text="New Game")
            return

        if self.one_player:
            # Make the AI move
            self.ai_move()
        else:
            # Switch the user value
            self.user = "X" if self.user == "O" else "O"

    def ai_move(self):
        """ Set up the function to handle AI moves """
        # Check for a winning move
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = self.ai
                    if self.check_win(self.ai):
                        self.buttons[i][j].config(text=self.ai)
                        self.result_label.config(text="AI Wins!")
                        self.ai_wins += 1
                        self.score_label.config(text=f"User: {self.user1_wins} - AI: {self.ai_wins}")
                        self.reset_button.config(text="New Game")
                        return
                    self.board[i][j] = ""

        # Check for a blocking move
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = self.user
                    if self.check_win(self.user):
                        self.board[i][j] = self.ai
                        self.buttons[i][j].config(text=self.ai)
                        return
                    self.board[i][j] = ""

        # Choose a random open cell
        choices = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    choices.append((i, j))
        i, j = random.choice(choices)
        self.board[i][j] = self.ai
        self.buttons[i][j].config(text=self.ai)

    def check_win(self, player):
        """ Set up the function to check for a win """
        # Check rows
        for row in self.board:
            if row == [player, player, player]:
                return True

        # Check columns
        for col in range(3):
            if self.board[0][col] == player and self.board[1][col] == player and self.board[2][col] == player:
                return True

        # Check diagonals
        if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
            return True
        if self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player:
            return True

        return False

    def check_tie(self):
        """ Set up the function to check for a tie """
        for row in self.board:
            if "" in row:
                return False
        return True

    def reset_game(self):
        """ Set up the function to reset the game """
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]

        # Update the button text
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")

        self.result_label.config(text="")
        self.reset_button.config(text="Reset")


def calc_geometry(*, window: tkinter.Tk, width: int, height: int):
    # Calculate the center of the screen
    center_x = window.winfo_screenwidth() // 2
    center_y = window.winfo_screenheight() // 2

    return f"{width}x{height}+{center_x - width // 2}+{center_y - height // 2}"


if __name__ == "__main__":
    menu = TicTacToeMenu()
    menu.mainloop()

