import tkinter as tk


class Piece:
    def __init__(self, color: str, x: int, y: int):
        """
        Initializes a Piece object with the given color, x position, and y position.

        :param color: the color of the piece, either "red" or "black"
        :param x: the x position of the piece on the board, an integer from 0 to 7
        :param y: the y position of the piece on the board, an integer from 0 to 7
        """
        # Set starting piece variables
        self.color = color
        self.x = x
        self.y = y
        self.king = False
        self.captured = False


class Board:
    def __init__(self):
        """
        Initializes a Board object with the default board configuration and the current player set to "red".
        """
        # Initialize the board to be a 8x8 grid of None values
        self.board = [[None for _ in range(8)] for _ in range(8)]

        # The current player is set to "red" at the start of the game
        self.current_player = "red"

        # Set starting board variables
        self.game_over = False
        self.selected_piece = None
        self.selected_x = None
        self.selected_y = None
        self.initialize_board()
        self.red_wins = 0
        self.black_wins = 0

    def initialize_board(self):
        """
        Initializes the board with the starting configuration of the game.
        """
        # Iterate through the first 3 rows
        for i in range(3):

            # Iterate through each column in the row
            for j in range(8):

                # Check if the current square is a valid position for a piece
                if (i + j) % 2 == 1:

                    # Place a black piece in the current square
                    self.board[i][j] = Piece("black", i, j)

        # Iterate through the last 3 rows
        for i in range(5, 8):

            # Iterate through each column in the row
            for j in range(8):

                # Check if the current square is a valid position for a piece
                if (i + j) % 2 == 1:

                    # Place a red piece in the current square
                    self.board[i][j] = Piece("red", i, j)

    def make_move(self, start_x, start_y, end_x, end_y):
        """
        Makes a move from the square at position (start_x, start_y) to the square at position (end_x, end_y)
        if the move is valid.

        :param start_x: the x position of the starting square, an integer from 0 to 7
        :param start_y: the y position of the starting square, an integer from 0 to 7
        :param end_x: the x position of the ending square, an integer from 0 to 7
        :param end_y: the y position of the ending square, an integer from 0 to 7
        """
        # Get the piece at the starting square
        piece = self.board[start_x][start_y]

        # Check if there is no piece at the starting square or the piece is not the current player's color
        if piece is None or piece.color != self.current_player:
            print("Invalid move: no piece at start position or wrong color")
            return

        # Check if the ending square is off the board
        if end_x < 0 or end_x > 7 or end_y < 0 or end_y > 7:
            print("Invalid move: end position is off the board")
            return

        # Check if the ending square is not a valid position for a piece
        if (end_x + end_y) % 2 == 0:
            print("Invalid move: end position is not a valid square")
            return

        # Check if the piece is not moving diagonally
        if abs(end_x - start_x) != abs(end_y - start_y):
            print("Invalid move: piece can only move diagonally")
            return

        # Check if the piece is not moving one or two squares at a time
        if abs(end_x - start_x) > 2:
            print("Invalid move: can only move one or two squares at a time")
            return

        # Check if the ending square is already occupied
        if self.board[end_x][end_y] is not None:
            print("Invalid move: desired space is already occupied")
            return

        # Check if the piece is not a king
        if not piece.king:

            # Check if the piece is red and the move is backwards
            if piece.color == "red" and end_x > start_x:
                print("Invalid move: red piece cannot move backwards")
                return

            # Check if the piece is black and the move is backwards
            if piece.color == "black" and end_x < start_x:
                print("Invalid move: black piece cannot move backwards")
                return

        # Capture move - the ending square is 2 spaces away
        if abs(end_x - start_x) == 2:

            # Calculate the x position of the captured piece
            capture_x = (start_x + end_x) // 2

            # Calculate the y position of the captured piece
            capture_y = (start_y + end_y) // 2

            # Get the captured piece
            capture_piece = self.board[capture_x][capture_y]

            # Check if there is no piece to capture or the captured piece is the same color as the moving piece
            if capture_piece is None or capture_piece.color == piece.color:
                print("Invalid move: no piece to capture or same color")
                return

            # Remove the captured piece from the board
            self.board[capture_x][capture_y] = None

            # Place the moving piece at the ending square
            self.board[end_x][end_y] = piece

            # Remove the piece from the starting square
            self.board[start_x][start_y] = None

            # Update the x position of the piece
            piece.x = end_x

            # Update the y position of the piece
            piece.y = end_y

            # Check if the piece has reached the opposite end of the board
            if (piece.color == "red" and end_x == 0) or (piece.color == "black" and end_x == 7):

                # Promote the piece to a king
                piece.king = True

            # Check if double jump is possible from the ending square
            if self.check_double_jump(end_x, end_y):

                # Set the selected piece to the moving piece
                self.selected_piece = piece

                # Set the selected x position to the ending x position
                self.selected_x = end_x

                # Set the selected y position to the ending y position
                self.selected_y = end_y

                # TODO: Force the player to take the double jump move.
                #  One method is to keep track of all possible valid double jumps and not accept any moves until the
                #  currently selected piece moves to one of the valid double jump spaces

                # End the make move
                return
        else:
            # Place the moving piece at the ending square
            self.board[end_x][end_y] = piece

            # Remove the piece from the starting square
            self.board[start_x][start_y] = None

            # Update the x position of the piece
            piece.x = end_x

            # Update the y position of the piece
            piece.y = end_y

            # Check if the piece has reached the opposite end of the board
            if (piece.color == "red" and end_x == 0) or (piece.color == "black" and end_x == 7):

                # Promote the piece to a king
                piece.king = True

        # Switch the current player to the other color since there is not a double jump opportunity
        self.current_player = "red" if self.current_player == "black" else "black"

        # Deselect the piece
        self.selected_piece = None

        # Clear the selected x position
        self.selected_x = None

        # Clear the selected y position
        self.selected_y = None

    def check_double_jump(self, x, y):
        """
        Determine if a double jump is possible for the piece located at x and y

        :param x: the x position of the starting square, an integer from 0 to 7
        :param y: the y position of the starting square, an integer from 0 to 7
        """
        # Get the piece at the given position
        piece = self.board[x][y]

        # If the piece is not a king
        if not piece.king:

            # Check the forward diagonal directions if the piece is red
            if self.current_player == "red":

                # Return if a forward double jump is possible
                return self.check_forward_double_jumps(x, y)
            else:

                # Return if a backward double jump is possible
                return self.check_backward_double_jumps(x, y)
        else:

            # Since the piece is a king, check all 4 diagonal directions for a double jump
            return self.check_forward_double_jumps(x, y) or self.check_backward_double_jumps(x, y)

    def check_forward_double_jumps(self, x, y):
        """
        Check if a double jump is possible in the right direction (forward for red)

        :param x: the x position of the starting square, an integer from 0 to 7
        :param y: the y position of the starting square, an integer from 0 to 7
        """
        # Determine the coordinates of two squares away in the top-right direction
        jump_x = x - 2
        jump_y = y + 2

        # Verify that the jump space's coordinates are not out of bounds
        if jump_x >= 0 and jump_y <= 7:

            # Get the piece in between the starting piece and the jump space
            capture_piece = self.board[x - 1][y + 1]

            # Check the jump with the top-right jump square
            check = self.check_jump(capture_piece, jump_x, jump_y)

            # If the check was True, return True
            if check:
                return True

        # Determine the coordinates of two squares away in the top left direction
        jump_x = x - 2
        jump_y = y - 2

        # Verify that the jump space's coordinates are not out of bounds
        if jump_x >= 0 and jump_y >= 0:

            # Get the piece in between the starting piece and the jump space
            capture_piece = self.board[x - 1][y - 1]

            # Check the jump with the top-left jump square
            check = self.check_jump(capture_piece, jump_x, jump_y)

            # If the check was True, return True
            if check:
                return True

        # A double jump is not possible
        return False

    def check_backward_double_jumps(self, x, y):
        """
        Check if a double jump is possible in the left direction (backward for red)

        :param x: the x position of the starting square, an integer from 0 to 7
        :param y: the y position of the starting square, an integer from 0 to 7
        """
        # Determine the coordinates of two squares away in the bottom-right direction
        jump_x = x + 2
        jump_y = y + 2

        # Verify that the jump space's coordinates are not out of bounds
        if jump_x <= 7 and jump_y <= 7:

            # Get the piece in between the starting piece and the jump space
            capture_piece = self.board[x + 1][y + 1]

            # Check the jump with the bottom-right jump square
            check = self.check_jump(capture_piece, jump_x, jump_y)

            # If the check was True, return True
            if check:
                return True

        # Determine the coordinates of two squares away in the bottom-left direction
        jump_x = x + 2
        jump_y = y - 2

        # Verify that the jump space's coordinates are not out of bounds
        if jump_x <= 7 and jump_y >= 0:

            # Get the piece in between the starting piece and the jump space
            capture_piece = self.board[x + 1][y - 1]

            # Check the jump with the bottom-left jump square
            check = self.check_jump(capture_piece, jump_x, jump_y)

            # If the check was True, return True
            if check:
                return True

        # A double jump is not possible
        return False

    def check_jump(self, capture_piece, jump_x: int, jump_y: int):
        """
        Check if a double jump is possible with the provided jump coordinates

        :param capture_piece: the value of the space between the starting and jump squares, a Piece or None
        :param jump_y: the y position of the jumping to square, an integer from 0 to 7
        :param jump_x: the x position of the jumping to square, an integer from 0 to 7
        """
        # If there is a different-colored piece one square away and an empty space in the jump coordinates
        if (
                capture_piece is not None and
                capture_piece.color != self.current_player and
                self.board[jump_x][jump_y] is None
        ):
            # A double jump is possible
            return True

    def check_game_over(self):
        """
        Check if the current state of the board means that the game is over
        """

        # The starting value for the count of all red pieces
        red_count = 0

        # The starting value for the count of all black pieces
        black_count = 0

        # Iterate through each row
        for i in range(8):

            # Iterate through each column in the row
            for j in range(8):

                # Get the piece in the current square
                piece = self.board[i][j]

                # Check if there is a piece in the square and the color is red
                if piece is not None and piece.color == "red":

                    # Increment the count for red pieces
                    red_count += 1

                # Check if there is a piece in the square and the color is black
                elif piece is not None and piece.color == "black":

                    # Increment the count for black pieces
                    black_count += 1

        # Check if there are no more red pieces
        if red_count == 0:

            # Therefore, the black player wins
            print("Black player wins!")

            # Set the board's game over value to true
            self.game_over = True

            # Increment the number of times that the black player has won
            self.black_wins += 1

        # Check if there are no more black pieces
        elif black_count == 0:

            # Therefore, the red player wins
            print("Red player wins!")

            # Set the board's game over value to true
            self.game_over = True

            # Increment the number of times that the red player has won
            self.red_wins += 1

        # Since the red player still has pieces, check if they still can move at least one of their pieces
        elif self.current_player == "red":

            # Assume that no red pieces are able to move
            can_move = False

            # Iterate through each row
            for i in range(8):

                # Iterate through each column in the row
                for j in range(8):

                    # Check if the current square has a piece and the color is red
                    if self.board[i][j] is not None and self.board[i][j].color == "red":

                        # Check if this piece can move
                        if self.can_move(i, j):

                            # Set can move to true
                            can_move = True

                            # Break out of this loop since at least one red piece can move
                            break

                # Check if the can move variable was set to true
                if can_move:

                    # Break out of this loop since at least one red piece can move
                    break

            # Check if the can move variable was never set to true
            if not can_move:

                # The game ends as a draw since the Red player cannot move any of their pieces
                print("Red player has no moves left, game is a draw")

                # Set the board's game over value to true
                self.game_over = True

        # Since the black player still has pieces, check if they still can move at least one of their pieces
        else:

            # Assume that no black pieces are able to move
            can_move = False

            # Iterate through each row
            for i in range(8):

                # Iterate through each column in the row
                for j in range(8):

                    # Check if the current square has a piece and the color is black
                    if self.board[i][j] is not None and self.board[i][j].color == "black":

                        # Check if this piece can move
                        if self.can_move(i, j):

                            # Set can move to true
                            can_move = True

                            # Break out of this loop since at least one black piece can move
                            break

                # Check if the can move variable was set to true
                if can_move:

                    # Break out of this loop since at least one black piece can move
                    break

            # Check if the can move variable was never set to true
            if not can_move:

                # The game ends as a draw since the Black player cannot move any of their pieces
                print("Black player has no moves left, game is a draw")

                # Set the board's game over value to true
                self.game_over = True

    def can_move(self, x, y):
        """
        Check if a piece at the given position can make a move

        :param y: the y position of a square, an integer from 0 to 7
        :param x: the x position of a square, an integer from 0 to 7
        """
        # Return False if there is no piece at the given position
        if self.board[x][y] is None:
            return False

        # Get the piece at the given position
        piece = self.board[x][y]

        # Return False if the red piece is off the board
        if piece.color == "red" and (x < 0 or x > 7 or y < 0 or y > 7):
            return False

        # Return False if the black piece is off the board
        if piece.color == "black" and (x < 0 or x > 7 or y < 0 or y > 7):
            return False

        # Return False if the end position is not a valid square
        if (x + y) % 2 == 0:
            return False

        # Return False if the piece is not moving diagonally
        if abs(x - y) != 1:
            return False

        # If all checks pass, return True
        return True


class CheckersApp(tk.Tk):
    def __init__(self):
        # Create the main window
        super().__init__()

        # Set the window title
        self.title("Checkers")

        # Disable resizing of the window
        self.resizable(False, False)

        # Create a board
        self.board = Board()

        # Create a canvas to draw the board on
        self.canvas = tk.Canvas(self, width=400, height=400)

        # Create a button to reset the game and a button to quit the game
        self.reset_button = tk.Button(self, text="Reset", command=self.reset_board)
        self.quit_button = tk.Button(self, text="Quit", command=self.destroy)

        # Create a variable to store the current player and the corresponding label
        self.current_player_var = tk.StringVar()
        self.current_player_label = tk.Label(self, textvariable=self.current_player_var, font=("Arial", 16))

        # Create a variable to store the current selected piece coordinates and the corresponding label
        self.selected_piece_var = tk.StringVar()
        self.selected_piece_label = tk.Label(self, textvariable=self.selected_piece_var, font=("Arial", 16))

        # Create a variable to store the red score and the corresponding label
        self.red_score_var = tk.StringVar()
        self.red_score_label = tk.Label(self, textvariable=self.red_score_var, font=("Arial", 16))

        # Create a variable to store the black score and the corresponding label
        self.black_score_var = tk.StringVar()
        self.black_score_label = tk.Label(self, textvariable=self.black_score_var, font=("Arial", 16))

        # Set the initial current player to red
        self.current_player_var.set(f"Current player: {self.board.current_player}")

        # Set the initial current selected piece coordinates to empty
        self.selected_piece_var.set("Selected piece: ( , )")

        # Set the initial scores to 0
        self.red_score_var.set("Red Wins: 0")
        self.black_score_var.set("Black Wins: 0")

        # Add each element to the window in a specific location
        self.red_score_label.grid(row=0, column=0)
        self.black_score_label.grid(row=0, column=2)
        self.current_player_label.grid(row=1, column=0)
        self.selected_piece_label.grid(row=1, column=2)
        self.canvas.grid(row=2, column=0, columnspan=3)
        self.reset_button.grid(row=3, column=0)
        self.quit_button.grid(row=3, column=2)

        # Draw the board
        self.draw_board()

        # Bind all clicks to the handle click function
        self.bind("<Button-1>", self.handle_click)

        # Enter event loop until all idle callbacks have been called
        self.update_idletasks()

    def reset_board(self):
        """
        Clears the board and resets its status to the initial state
        """
        # Re-initialize the board
        self.board = Board()

        # Draw the board
        self.draw_board()

    def draw_board(self):
        """
        Draw the Checkers board and all pieces
        """
        # Create the Checkers board background
        self.canvas.create_rectangle(0, 0, 400, 400, fill="#ddaa77")

        # Iterate through the rows
        for i in range(8):

            # Iterate through each column in the row
            for j in range(8):

                # Skip drawing squares that are not valid positions for pieces
                if (i + j) % 2 == 0:
                    continue

                # Calculate the coordinates for the top left and bottom right corners of the square
                x1 = i * 50
                y1 = j * 50
                x2 = x1 + 50
                y2 = y1 + 50

                # Draw the square
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#442211")

        # Iterate through the rows again
        for i in range(8):

            # Iterate through each column in the row
            for j in range(8):

                # Get the piece at the current position
                piece = self.board.board[i][j]

                # Skip the current position if there is no piece
                if piece is None:
                    continue

                # Calculate the center coordinates of the square
                x = i * 50 + 25
                y = j * 50 + 25

                # Set the fill color based on the piece color
                color = "#aa0000" if piece.color == "red" else "#0000aa"

                # Draw the piece as an oval
                self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=color)

                # If the piece is a king, draw the "K" over it
                if piece.king:
                    self.canvas.create_text(x, y, text="K", font=("Arial", 20), fill="white")

    def handle_click(self, event):
        """
        Handles a click on the Checkers board. If a piece is selected, the click is treated as a move.

        If no piece is selected, the click is treated as a piece selection.
        """
        # Calculate the (x, y) coordinates of the clicked square
        x = event.x // 50
        y = event.y // 50

        # Get the piece at the clicked square
        piece = self.board.board[x][y]

        # If the game is already over, ignore the click
        if self.board.game_over:
            return

        # If no piece is currently selected
        if self.board.selected_piece is None:

            # Ignore the click if no piece is present or the piece is not the current player's
            if piece is None or piece.color != self.board.current_player:
                return

            # Select the piece
            self.board.selected_piece = piece
            self.board.selected_x = x
            self.board.selected_y = y

            # Update the selected piece label
            self.selected_piece_var.set(f"Selected piece: ({x}, {y})")

        # If a piece is already selected
        else:

            # Ignore the click if it is on the same square as the selected piece
            if self.board.selected_x == x and self.board.selected_y == y:
                return

            # Change the selected piece if a new piece was selected that belongs to the current player
            if piece and piece.color == self.board.selected_piece.color:

                # Select the new piece
                self.board.selected_piece = piece
                self.board.selected_x = x
                self.board.selected_y = y

                # Update the selected piece label
                self.selected_piece_var.set(f"Selected piece: ({x}, {y})")
                return

            # Make the move
            self.board.make_move(self.board.selected_x, self.board.selected_y, x, y)

            # Set the current player label to the next player
            self.current_player_var.set(f"Current player: {self.board.current_player}")

            # Reset the selected piece label
            self.selected_piece_var.set("Selected piece: ( , )")

            # Redraw the board
            self.draw_board()

            # Check if the game is over
            self.board.check_game_over()

            # If the game is over, display the "Game Over" message and update the scores
            if self.board.game_over:
                self.canvas.create_text(200, 200, text="Game Over", font=("Arial", 32), fill="white")
                self.red_score_var.set(f"Red Wins: {self.board.red_wins}")
                self.black_score_var.set(f"Black Wins: {self.board.black_wins}")


if __name__ == "__main__":
    # Initialize the Checkers App
    app = CheckersApp()

    # Start the event loop
    app.mainloop()
