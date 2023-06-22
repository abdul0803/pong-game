import pygame
import sys
import random

# Initialize the game
pygame.init()
screen_width, screen_height = 800, 600  # Set your desired screen size
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
fps = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Paddle settings
paddle_width, paddle_height = 10, 80
paddle_speed = 5

# Ball settings
ball_width, ball_height = 20, 20  # Increase ball size
ball_speed_x = 3
ball_speed_y = 3

# Create the paddles
player_paddle = pygame.Rect(50, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)
opponent_paddle = pygame.Rect(screen_width - 50 - paddle_width, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)

# Create the ball
ball = pygame.Rect(screen_width // 2 - ball_width // 2, screen_height // 2 - ball_height // 2, ball_width, ball_height)

ball_speed = [ball_speed_x, ball_speed_y]
initial_ball_speed_x = ball_speed_x

# Load the menu image
menu_image = pygame.image.load("pong.png")
menu_image = pygame.transform.scale(menu_image, (300, 200))

# Game state
game_started = False
game_over = False
player_score = 0
opponent_score = 0

# Timer variables
timer_event = pygame.USEREVENT + 1
timer_interval = 10000  # Time interval in milliseconds
pygame.time.set_timer(timer_event, timer_interval)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
            mouse_pos = pygame.mouse.get_pos()
            play_button_rect = pygame.Rect(screen_width // 2 - 75, 300, 150, 50)
            if play_button_rect.collidepoint(mouse_pos):
                if game_over:
                    game_started = False
                    game_over = False
                    player_score = 0
                    opponent_score = 0
                    ball_speed[0] = initial_ball_speed_x
                    ball_speed[1] = ball_speed_y
                    ball.x = screen_width // 2 - ball_width // 2
                    ball.y = screen_height // 2 - ball_height // 2
                else:
                    game_started = True

        if event.type == timer_event and game_started:
            ball_speed[0] *= 1.1  # Increase ball speed
            ball_speed[1] *= 1.1

    if game_started and not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_paddle.y -= paddle_speed
            player_paddle.y = max(player_paddle.y, 0)  # Limit the paddle within the screen boundary
        if keys[pygame.K_DOWN]:
            player_paddle.y += paddle_speed
            player_paddle.y = min(player_paddle.y, screen_height - paddle_height)  # Limit the paddle within the screen boundary

        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Simple AI logic
        if ball.y < opponent_paddle.y + paddle_height / 2:
            opponent_paddle.y -= paddle_speed
            opponent_paddle.y = max(opponent_paddle.y, 0)  # Limit the paddle within the screen boundary
        if ball.y > opponent_paddle.y + paddle_height / 2:
            opponent_paddle.y += paddle_speed
            opponent_paddle.y = min(opponent_paddle.y, screen_height - paddle_height)  # Limit the paddle within the screen boundary

        # Ball collision with paddles
        if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
            ball_speed[0] = -ball_speed[0]

        # Ball collision with walls
        if ball.y <= 0 or ball.y >= screen_height - ball_height:
            ball_speed[1] = -ball_speed[1]

        # Score tracking
        if ball.x <= 0:
            opponent_score += 1
            ball_speed[0] = abs(initial_ball_speed_x)
            ball_speed[1] = random.choice([-3, 3])
            ball.x = screen_width // 2 - ball_width // 2
            ball.y = screen_height // 2 - ball_height // 2
        elif ball.x >= screen_width - ball_width:
            player_score += 1
            ball_speed[0] = -abs(initial_ball_speed_x)
            ball_speed[1] = random.choice([-3, 3])
            ball.x = screen_width // 2 - ball_width // 2
            ball.y = screen_height // 2 - ball_height // 2

        if player_score >= 12 or opponent_score >= 12:
            game_over = True

    # Update the screen
    screen.fill(BLACK)

    if not game_started:
        screen.blit(menu_image, (screen_width // 2 - menu_image.get_width() // 2, 50))
        pygame.draw.rect(screen, BLACK, (screen_width // 2 - 73, 302, 146, 46))
        font = pygame.font.Font(None, 36)
        text = font.render("Play Game", True, WHITE)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, 310))
    else:
        pygame.draw.rect(screen, WHITE, player_paddle)
        pygame.draw.rect(screen, WHITE, opponent_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (screen_width // 2, 0), (screen_width // 2, screen_height))

        # Display scores
        score_font = pygame.font.Font(None, 48)
        player_score_text = score_font.render(str(player_score), True, WHITE)
        opponent_score_text = score_font.render(str(opponent_score), True, WHITE)
        screen.blit(player_score_text, (screen_width // 4 - player_score_text.get_width() // 2, 10))
        screen.blit(opponent_score_text, (3 * screen_width // 4 - opponent_score_text.get_width() // 2, 10))

    # Game over condition
    if game_over:
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2 - 100))
        pygame.draw.rect(screen, WHITE, (screen_width // 2 - 75, 300, 150, 50))
        pygame.draw.rect(screen, BLACK, (screen_width // 2 - 73, 302, 146, 46))
        font = pygame.font.Font(None, 36)
        restart_text = font.render("Play Again", True, WHITE)
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, 310))

    pygame.display.flip()
    clock.tick(fps)
