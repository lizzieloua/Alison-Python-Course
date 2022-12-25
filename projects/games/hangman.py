import random
import tkinter as tk


class Hangman(tk.Tk):
    def __init__(self):
        # Set up the window
        tk.Tk.__init__(self)
        self.title("Hangman")

        # Calculate the center of the screen
        center_x = self.winfo_screenwidth() // 2
        center_y = self.winfo_screenheight() // 2

        # Set the window size and position
        self.geometry(f"400x300+{center_x - 200}+{center_y - 150}")

        # Set up the word list and pick a random word
        self.word_list = ["apple", "banana", "cherry", "durian", "elderberry"]
        self.word = random.choice(self.word_list)

        # Set up the game variables
        self.guesses = 0
        self.max_guesses = 6
        self.guessed_letters = []
        self.game_over = False

        # Set up the label to display the word
        self.word_label = tk.Label(text="_" * len(self.word), font=("Arial", 24))
        self.word_label.pack()

        # Set up the label to display the number of guesses remaining
        self.guesses_label = tk.Label(text=f"Guesses remaining: {self.max_guesses - self.guesses}", font=("Arial", 12))
        self.guesses_label.pack()

        # Set up the entry field to enter a letter
        self.letter_entry = tk.Entry(width=10)
        self.letter_entry.pack()

        # Set up the label to display the result of the guess
        self.result_label = tk.Label(text="", font=("Arial", 12))
        self.result_label.pack()

        # Clear the entry field
        self.letter_entry.delete(0, "end")

        # Set up the button to submit a letter
        submit_button = tk.Button(text="Guess", command=self.guess_letter)
        submit_button.pack()

        # Set up the button to reset the game
        reset_button = tk.Button(text="Reset", command=self.reset_game)
        reset_button.pack()

        # Set up the button to quit the game
        quit_button = tk.Button(text="Quit", command=self.destroy)
        quit_button.pack()

    def reset_game(self):
        """ Set up the function to reset the game """

        # Pick a new random word
        self.word = random.choice(self.word_list)

        # Reset the game variables
        self.guesses = 0
        self.guessed_letters = []
        self.game_over = False

        # Update the word label
        self.word_label.config(text="_" * len(self.word))

        # Update the guesses label
        self.guesses_label.config(text=f"Guesses remaining: {self.max_guesses - self.guesses}")

        # Update the result label
        self.result_label.config(text="")

    def guess_letter(self):
        """ Set up the function to handle guessing a letter """

        # Get the letter from the entry field
        letter = self.letter_entry.get()
        letter = letter.lower()

        # Check if the game is over
        if self.game_over:
            return

        if len(letter) < 1 or len(letter) > 1:
            self.result_label.config(text="Your guess must be 1 character.")
            return

        # Check if the letter has already been guessed
        if letter in self.guessed_letters:
            self.result_label.config(text="You have already guessed that letter.")
            return

        # Add the letter to the list of guessed letters
        self.guessed_letters.append(letter)

        # Check if the letter is in the word
        if letter in self.word:
            self.result_label.config(text="Correct!")
        else:
            self.result_label.config(text="Incorrect.")
            self.guesses += 1

        # Update the word label to show any correctly guessed letters
        word_display = ""
        for char in self.word:
            if char in self.guessed_letters:
                word_display += char
            else:
                word_display += "_"
        self.word_label.config(text=word_display)

        # Update the guesses label
        self.guesses_label.config(text=f"Guesses remaining: {self.max_guesses - self.guesses}")

        # Check if the player has won or lost
        if "_" not in word_display:
            self.result_label.config(text="You win! Click the Reset button to play again.")
            self.game_over = True
        elif self.guesses == self.max_guesses:
            self.result_label.config(text="You lose. The word was " + self.word +
                                          ". Click the Reset button to play again.")
            self.game_over = True

        # Clear the entry field
        self.letter_entry.delete(0, "end")


if __name__ == "__main__":
    game = Hangman()
    game.mainloop()
