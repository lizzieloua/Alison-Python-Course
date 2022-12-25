import random
import pygame

from time import sleep


# Initialize pygame
pygame.init()

# Set the window size
window_size = (800, 600)

# Set the background color
bg_color = (0, 0, 0)
white = (255, 255, 255)

# Set the paddle size
paddle_width = 100
paddle_height = 20

# Set the paddle color
paddle_color = white

# Set the ball size
ball_size = 20

# Set the ball color
ball_color = white

# Set the initial ball position
ball_pos = (random.randint(200, 600), 300)

# Set the initial ball velocity
ball_vel = (3, 3)

# Set the initial paddle position
paddle_pos = (350, 550)

# Set the brick size
brick_width = 75
brick_height = 20

# Set the brick color iter
brick_iter = 0

# Set the initial score
score = 0

# Set the font for the text captions
score_font = pygame.font.Font(None, 30)
result_font = pygame.font.Font(None, 45)

# Set the initial running state
running = True

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title
pygame.display.set_caption('Brick Breaker')

# Create the list of bricks
bricks = []
brick_colors = []
brick_color_options = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

for i in range(11):
    for j in range(9):
        bricks.append((j*brick_width + 50, i*brick_height + 50, brick_width, brick_height))
        brick_colors.append(brick_color_options[brick_iter % 3])

        if brick_iter % 9 == 0:
            brick_iter += 2
        else:
            brick_iter += 1

# Run the game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if the bricks are gone
    if len(bricks) == 0:
        # Draw the winning text
        result_text = result_font.render("You Win!", True, white)
        screen.blit(result_text, (330, 300))

        # Update the display
        pygame.display.flip()
        sleep(2)

        # End the Loop
        running = False
        break

    # Update the ball position
    ball_pos = (ball_pos[0] + ball_vel[0], ball_pos[1] + ball_vel[1])

    # Check for ball collision with walls
    if ball_pos[0] < 0 or ball_pos[0] > window_size[0] - ball_size:
        ball_vel = (-ball_vel[0], ball_vel[1])
    if ball_pos[1] < 0:
        ball_vel = (ball_vel[0], -ball_vel[1])
    if ball_pos[1] > window_size[1] - ball_size:
        # Draw the losing text
        result_text = result_font.render("You Lose!", True, white)
        screen.blit(result_text, (330, 300))

        # Update the display
        pygame.display.flip()
        sleep(2)

        # End the Loop
        running = False
        break

    # Check for ball collision with bricks
    for brick in bricks:
        if (
                brick[0] < ball_pos[0] < brick[0] + brick_width and
                brick[1] < ball_pos[1] < brick[1] + brick_height
        ):
            brick_colors.pop(bricks.index(brick))
            bricks.remove(brick)
            score += 1
            ball_vel = (ball_vel[0], -ball_vel[1])

    # Check for ball collision with paddle
    if (
            paddle_pos[0] < ball_pos[0] < paddle_pos[0] + paddle_width and
            paddle_pos[1] < ball_pos[1] < paddle_pos[1] + paddle_height
    ):
        ball_vel = (ball_vel[0], -ball_vel[1])

    # Clear the screen
    screen.fill(bg_color)

    # Draw the bricks
    brick_iter = 0
    for brick in bricks:
        pygame.draw.rect(screen, brick_colors[brick_iter], brick)
        brick_iter += 1

    # Draw the ball
    pygame.draw.circle(screen, ball_color, ball_pos, ball_size)

    # Draw the paddle
    pygame.draw.rect(screen, paddle_color, (paddle_pos[0], paddle_pos[1], paddle_width, paddle_height))

    # Check the state of the keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_pos = (paddle_pos[0] - 5, paddle_pos[1])
    if keys[pygame.K_RIGHT]:
        paddle_pos = (paddle_pos[0] + 5, paddle_pos[1])

    # Check for paddle collision with walls
    if paddle_pos[0] < 0:
        paddle_pos = (0, paddle_pos[1])
    if paddle_pos[0] > window_size[0] - paddle_width:
        paddle_pos = (window_size[0] - paddle_width, paddle_pos[1])

    # Render the score text
    score_text = score_font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
