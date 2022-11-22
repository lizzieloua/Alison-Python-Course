from random import randint


# Create a list of play options
options = ["Rock", "Paper", "Scissors"]


def main():

    while True:
        # Assign a random play to the computer
        computer = options[randint(0, 2)]

        # Gather player input
        player = input("Rock, Paper, Scissors, or Exit?")

        # Check player's input for invalid choice or desire to exit

        # Check who won this round


if __name__ == "__main__":
    # Run the main function
    main()
