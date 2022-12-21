import random
import tkinter as tk

# Set up the window
window = tk.Tk()
window.title("Hangman")

# Get the width and height of the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the center of the screen
center_x = screen_width // 2
center_y = screen_height // 2

# Set the window size and position
window.geometry(f"400x300+{center_x - 200}+{center_y - 150}")

# Set up the word list and pick a random word
word_list = ["apple", "banana", "cherry", "durian", "elderberry"]
word = random.choice(word_list)

# Set up the game variables
guesses = 0
max_guesses = 6
guessed_letters = []

# Set up the label to display the word
word_label = tk.Label(text="_" * len(word), font=("Arial", 24))
word_label.pack()

# Set up the label to display the number of guesses remaining
guesses_label = tk.Label(text=f"Guesses remaining: {max_guesses - guesses}", font=("Arial", 12))
guesses_label.pack()


# Set up the function to reset the game
def reset_game():
    global word, guesses, guessed_letters

    # Pick a new random word
    word = random.choice(word_list)

    # Reset the game variables
    guesses = 0
    guessed_letters = []

    # Update the word label
    word_label.config(text="_" * len(word))

    # Update the guesses label
    guesses_label.config(text=f"Guesses remaining: {max_guesses - guesses}")

    # Update the result label
    result_label.config(text="")


# Set up the function to handle guessing a letter
def guess_letter():
    global guesses

    # Get the letter from the entry field
    letter = letter_entry.get()
    letter = letter.lower()

    # Check if the letter has already been guessed
    if letter in guessed_letters:
        result_label.config(text="You have already guessed that letter.")
        return

    # Add the letter to the list of guessed letters
    guessed_letters.append(letter)

    # Check if the letter is in the word
    if letter in word:
        result_label.config(text="Correct!")
    else:
        result_label.config(text="Incorrect.")
        guesses += 1

    # Update the word label to show any correctly guessed letters
    word_display = ""
    for char in word:
        if char in guessed_letters:
            word_display += char
        else:
            word_display += "_"
    word_label.config(text=word_display)

    # Update the guesses label
    guesses_label.config(text=f"Guesses remaining: {max_guesses - guesses}")

    # Check if the player has won or lost
    if "_" not in word_display:
        result_label.config(text="You win! Click the Reset button to play again.")
    elif guesses == max_guesses:
        result_label.config(text="You lose. The word was " + word + ". Click the Reset button to play again.")

        # Clear the entry field
    letter_entry.delete(0, "end")


# Set up the entry field to enter a letter
letter_entry = tk.Entry(width=10)
letter_entry.pack()

# Set up the button to submit a letter
submit_button = tk.Button(text="Guess", command=guess_letter)
submit_button.pack()

# Set up the button to reset the game
reset_button = tk.Button(text="Reset", command=reset_game)
reset_button.pack()

# Set up the button to quit the game
quit_button = tk.Button(text="Quit", command=window.destroy)
quit_button.pack()

# Set up the label to display the result of the guess
result_label = tk.Label(text="", font=("Arial", 12))
result_label.pack()

# Clear the entry field
letter_entry.delete(0, "end")

# Run the window loop
window.mainloop()
