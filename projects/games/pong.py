import pygame


# Initialize pygame
pygame.init()

# Set the window size
window_size = (600, 400)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the window title
pygame.display.set_caption("Pong")

# Set the background color
bg_color = (0, 0, 0)

# Set the ball properties
ball_color = (255, 255, 255)
ball_radius = 10
ball_pos = (300, 200)
ball_vel = (2, 2)

# Set the paddle properties
paddle_speed = 5
paddle_color = (255, 255, 255)
paddle_width = 20
paddle_height = 100
paddle_1_pos = (50, 150)
paddle_2_pos = (550, 150)

# Set the score properties
score_color = (255, 255, 255)
score_font = pygame.font.Font(None, 36)
score_1 = 0
score_2 = 0

# Set the game loop flag
running = True

# Run the game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check the state of the keys
    keys = pygame.key.get_pressed()

    # Update the paddle positions
    if keys[pygame.K_w]:
        paddle_1_pos = (paddle_1_pos[0], paddle_1_pos[1] - paddle_speed)
    if keys[pygame.K_s]:
        paddle_1_pos = (paddle_1_pos[0], paddle_1_pos[1] + paddle_speed)
    if keys[pygame.K_UP]:
        paddle_2_pos = (paddle_2_pos[0], paddle_2_pos[1] - paddle_speed)
    if keys[pygame.K_DOWN]:
        paddle_2_pos = (paddle_2_pos[0], paddle_2_pos[1] + paddle_speed)

    # Calculate the top-left corner coordinates of the paddles
    paddle_1_rect = (
        paddle_1_pos[0] - paddle_width // 2,
        paddle_1_pos[1] - paddle_height // 2,
        paddle_width, paddle_height
    )
    paddle_2_rect = (
        paddle_2_pos[0] - paddle_width // 2,
        paddle_2_pos[1] - paddle_height // 2,
        paddle_width, paddle_height
    )

    # Update the ball position
    ball_pos = (ball_pos[0] + ball_vel[0], ball_pos[1] + ball_vel[1])

    # Check for ball collision with top and bottom walls
    if ball_pos[1] - ball_radius < 0 or ball_pos[1] + ball_radius > 400:
        ball_vel = (ball_vel[0], -ball_vel[1])

    # Check for ball collision with paddles
    if (
            ball_pos[0] - ball_radius < paddle_1_pos[0] + paddle_width
            and paddle_1_pos[1] < ball_pos[1] < paddle_1_pos[1] + paddle_height
    ):
        ball_vel = (-ball_vel[0], ball_vel[1])
    elif ball_pos[0] - ball_radius < 0:
        score_2 += 1
        ball_pos = (300, 200)
        ball_vel = (2, 2)

    if ball_pos[0] + ball_radius > paddle_2_pos[0] and ball_pos[1] + ball_vel[1] > paddle_2_pos[1] and ball_pos[1] + \
            ball_vel[1] < paddle_2_pos[1] + paddle_height:
        ball_vel = (-ball_vel[0], ball_vel[1])
    elif ball_pos[0] + ball_radius > 600:
        score_1 += 1
        ball_pos = (300, 200)
        ball_vel = (-2, -2)

    # Clear the screen
    screen.fill(bg_color)

    # Draw the ball
    pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)

    # Draw the paddles
    pygame.draw.rect(screen, paddle_color, paddle_1_rect)
    pygame.draw.rect(screen, paddle_color, paddle_2_rect)

    # Draw the scores
    score_1_text = score_font.render(str(score_1), True, score_color)
    score_2_text = score_font.render(str(score_2), True, score_color)
    screen.blit(score_1_text, (250, 10))
    screen.blit(score_2_text, (350, 10))

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
