import pygame
import random

from time import sleep


# Set the window size
window_size = (600, 600)

# Set the colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set the snake and food properties
snake_size = 20
food_size = 20

# Set game properties
first_run = True

# Set the initial score
score = 0

# Set the winning score
winning_score = 50

# Initialize pygame
pygame.init()

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title
pygame.display.set_caption('Snake')

# Set the font for the text captions
score_font = pygame.font.Font(None, 30)
result_font = pygame.font.Font(None, 45)
winning_font = pygame.font.Font(None, 30)

# Create the snake
snake = [(200, 200), (220, 200), (240, 200)]

# Set the initial direction
direction = 'right'

# Set the initial food position
food_pos = (
    random.randint(0, window_size[0] // food_size) * food_size,
    random.randint(0, window_size[1] // food_size) * food_size
)

# Run the game loop
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if score >= winning_score:
        # Draw the winning text
        result_text = result_font.render("You Win!", True, white)
        screen.blit(result_text, (225, 300))

        # Update the display
        pygame.display.flip()
        sleep(2)

        # End the Loop
        running = False

    # Check the state of the keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != 'down':
        direction = 'up'
    if keys[pygame.K_DOWN] and direction != 'up':
        direction = 'down'
    if keys[pygame.K_LEFT] and direction != 'right':
        direction = 'left'
    if keys[pygame.K_RIGHT] and direction != 'left':
        direction = 'right'

    # Update the snake position
    if direction == 'up':
        snake.insert(0, (snake[0][0], snake[0][1] - snake_size))
    if direction == 'down':
        snake.insert(0, (snake[0][0], snake[0][1] + snake_size))
    if direction == 'left':
        snake.insert(0, (snake[0][0] - snake_size, snake[0][1]))
    if direction == 'right':
        snake.insert(0, (snake[0][0] + snake_size, snake[0][1]))

    # Check for snake collision with walls
    if snake[0][0] < 0 or snake[0][0] > window_size[0] or snake[0][1] < 0 or snake[0][1] > window_size[1]:
        # Draw the losing text
        result_text = result_font.render("You Lose!", True, white)
        screen.blit(result_text, (225, 300))

        # Update the display
        pygame.display.flip()
        sleep(2)

        # End the Loop
        running = False

    # Check for snake collision with itself
    if snake[0] in snake[1:]:
        if first_run:
            first_run = False
        else:
            # Draw the losing text
            result_text = result_font.render("You Lose!", True, white)
            screen.blit(result_text, (225, 300))

            # Update the display
            pygame.display.flip()
            sleep(2)

            # End the Loop
            running = False

    # Check for snake eating food
    if snake[0] == food_pos:
        food_pos = (
            random.randint(0, window_size[0] // food_size) * food_size,
            random.randint(0, window_size[1] // food_size) * food_size
        )

        # Increment the score
        score += 1
    else:
        snake.pop()

    # Clear the screen
    screen.fill(black)

    # Draw the snake
    for pos in snake:
        pygame.draw.rect(screen, white, pygame.Rect(pos[0], pos[1], snake_size, snake_size))

    # Draw the food
    pygame.draw.rect(screen, white, pygame.Rect(food_pos[0], food_pos[1], food_size, food_size))

    # Draw the score text
    score_text = score_font.render(f'Score: {score}', True, white)
    screen.blit(score_text, (10, 10))

    # Draw the winning text
    winning_text = winning_font.render(f'Winning Score: {winning_score}', True, white)
    screen.blit(winning_text, (420, 10))

    # Update the display
    pygame.display.flip()

    sleep(0.1)

# Quit pygame
pygame.quit()
