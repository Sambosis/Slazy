C:\mygit\Slazy\repo\pygamedemo\main.py
Language detected: python
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side-Scrolling Platformer")

# Basic color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game states
GAME_STATE_MENU = "menu"
GAME_STATE_PLAYING = "playing"
GAME_STATE_GAME_OVER = "game_over"

# Initialize game state
current_game_state = GAME_STATE_MENU

# Clock/FPS control
clock = pygame.time.Clock()
FPS = 60

# Function to display text
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Main menu
def show_menu():
    screen.fill(BLUE)
    font = pygame.font.Font(None, 74)
    draw_text("Main Menu", font, WHITE, 250, 250)
    font = pygame.font.Font(None, 36)
    draw_text("Press SPACE to Start", font, WHITE, 280, 350)
    pygame.display.flip()

# Playing state
def play_game():
    screen.fill(GREEN)
    font = pygame.font.Font(None, 36)
    draw_text("Playing Game...", font, BLACK, 300, 250)
    pygame.display.flip()

# Game over state
def show_game_over():
    screen.fill(RED)
    font = pygame.font.Font(None, 74)
    draw_text("Game Over", font, WHITE, 250, 250)
    font = pygame.font.Font(None, 36)
    draw_text("Press ESC to Quit", font, WHITE, 280, 350)
    pygame.display.flip()

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Game state transitions
    if current_game_state == GAME_STATE_MENU:
        show_menu()
        if keys[pygame.K_SPACE]:
            current_game_state = GAME_STATE_PLAYING

    elif current_game_state == GAME_STATE_PLAYING:
        play_game()
        if keys[pygame.K_ESCAPE]:  # Temporary shortcut to game over
            current_game_state = GAME_STATE_GAME_OVER

    elif current_game_state == GAME_STATE_GAME_OVER:
        show_game_over()
        if keys[pygame.K_ESCAPE]:
            running = False

    # FPS control
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
