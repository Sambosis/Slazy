C:\mygit\Slazy\repo\pygamedemo\game.py
Language detected: python
# Import necessary libraries
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game states
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
current_state = MENU

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game")

# Clock setup
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)  # Using red color for the player for now
        self.rect = self.image.get_rect()
        self.rect.x = 50 
        self.rect.y = 50 

        # Movement attributes
        self.velocity = [0, 0]
        self.jumping = False

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.velocity[0] = -5
        elif keys[pygame.K_RIGHT]:
            self.velocity[0] = 5
        else:
            self.velocity[0] = 0

        if not self.jumping and keys[pygame.K_SPACE]:
            self.velocity[1] = -10
            self.jumping = True

        # Gravity effect
        self.velocity[1] += 0.5

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def update(self):
        global current_state
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = 0
            self.rect.x = 50
            self.velocity[1] = 0
            self.velocity[0] = 0
            self.jumping = False

        if self.rect.colliderect(pygame.Rect(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20)):
            self.jumping = False
        else:
            self.jumping = True

# Game initialization
def initialize_game():
    global player
    player = Player()
    player.rect.x = 400
    player.rect.y = 500

# Main game loop
def main_loop():
    global current_state, running
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        
        if current_state == MENU:
            pass  # Placeholder for menu actions

        if current_state == PLAYING:
            player.move()
            screen.blit(player.image, player.rect.topleft)

        pygame.display.flip()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
    sys.exit()

# Initialization
initialize_game()

# Start the main loop
main_loop()
C:\mygit\Slazy\repo\pygamedemo\enemy.py
Language detected: python
# enemy_manager.py

# Import necessary libraries
import pygame
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Enemy base class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))  # Using green color for enemies
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = [random.choice([-2, 2]), 0]  # Random horizontal velocity
    
    def move(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.bounce_off_edges()
    
    def bounce_off_edges(self):
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.velocity[0] *= -1

# Different types of enemies
class WalkingEnemy(Enemy):
    def update(self):
        self.move()

class FlyingEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocity[1] = random.choice([-2, 2])  # Add vertical motion
    
    def update(self):
        self.move()

# Enemy collision detection and behavior patterns
def handle_collision(enemy, player):
    if enemy.rect.colliderect(player.rect):
        print(f"Collision detected with {type(enemy).__name__}")
        enemy.velocity[0] *= -1  # Bounce back on collision

# Enemy sprite management
def create_enemy_group():
    enemy_group = pygame.sprite.Group()
    for _ in range(10):
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 100)
        if random.random() < 0.5:
            enemy_group.add(WalkingEnemy(x, y))
        else:
            enemy_group.add(FlyingEnemy(x, y))
    return enemy_group

# Sample usage in the main game loop
def main_loop():
    global current_state, running
    running = True
    enemies = create_enemy_group()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        
        if current_state == MENU:
            pass  # Placeholder for menu actions

        if current_state == PLAYING:
            for enemy in enemies:
                enemy.update()
                screen.blit(enemy.image, enemy.rect.topleft)
            
            # Check player-enemy collision
            for enemy in enemies:
                handle_collision(enemy, player)
        
        pygame.display.flip()
        clock.tick(FPS)

    # Cleanup
    enemies.empty()
    pygame.quit()
    sys.exit()

initialize_game()
main_loop()
C:\mygit\Slazy\repo\pygamedemo\items.py
Language detected: python
# item_manager.py

# Import necessary libraries
import pygame
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
POWER_UP_DURATION = 10000  # Duration in milliseconds for how long the power-up lasts

# Item base class
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))  # Yellow color for items
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.duration = POWER_UP_DURATION  # Default duration for power-up
        self.activation_time = None

    def move(self):
        self.rect.y += 5  # Simply fall downwards

    def update(self):
        self.move()
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()  # Remove item from game if it falls off the screen

# Different types of power-ups
class SpeedBoost(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill((0, 255, 255))  # Cyan color for speed boost
        self.duration = POWER_UP_DURATION // 2  # Half the default duration

    def apply_effect(self, player):
        print("Speed boost activated!")
        player_speed = player.velocity[0]
        player.velocity[0] = player_speed * 1.5
        self.activation_time = pygame.time.get_ticks()

    def check_duration(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.activation_time
        if elapsed_time >= self.duration:
            return False
        return True

class JumpBoost(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill((255, 0, 255))  # Magenta color for jump boost

    def apply_effect(self, player):
        print("Jump boost activated!")
        player_jump = player.velocity[1]
        player.velocity[1] = -player_jump * 1.5
        self.activation_time = pygame.time.get_ticks()

    def check_duration(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.activation_time
        if elapsed_time >= self.duration:
            return False
        return True

class Invincibility(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill((255, 0, 0))  # Red color for Invincibility

    def apply_effect(self, player):
        print("Invincibility activated!")
        self.activation_time = pygame.time.get_ticks()

    def check_duration(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.activation_time
        if elapsed_time >= self.duration:
            return False
        return True

# Power-up collection and activation system
def check_power_up(player, item):
    item.apply_effect(player)

def create_power_up_group():
    item_group = pygame.sprite.Group()
    for _ in range(5):
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        power_up_type = random.choice([SpeedBoost, JumpBoost, Invincibility])
        item = power_up_type(x, y)
        item_group.add(item)
    return item_group

# Sample usage in the main game loop
def main_loop():
    global current_state, running
    running = True
    players = pygame.sprite.GroupSingle(Player())
    items = create_power_up_group()
    last_item_activation_time = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        
        if current_state == MENU:
            pass  # Placeholder for menu actions

        if current_state == PLAYING:
            for item in items:
                if pygame.sprite.spritecollideany(item, players):
                    current_time = pygame.time.get_ticks()
                    if current_time - last_item_activation_time > 2000:  # Cooldown
                        last_item_activation_time = current_time
                        check_power_up(players.sprite, item)
                        if not item.check_duration():  # Deactivate if duration ends
                            item.kill()
                item.update()
                screen.blit(item.image, item.rect.topleft)

        if current_state == GAME_OVER:
            pass  # Placeholder for game over actions

        players.update()
        players.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    # Cleanup
    items.empty()
    pygame.quit()
    sys.exit()

initialize_game()
main_loop()
C:\mygit\Slazy\repo\pygamedemo\stats.py
Language detected: python
# Import necessary libraries
import pygame
import json
import os
from datetime import datetime

# Constants
STATS_FILE_PATH = "game_stats.json"

# GameStats class manages current game stats, session stats, and all-time high scores with persistent storage.
class GameStats:
    def __init__(self):
        # Initialize game data
        self.current_score = 0
        self.high_scores = []
        self.session_start_time = datetime.now()

        # Load existing stats from file if available
        self.load_from_file()

    def load_from_file(self):
        """Load game stats from a JSON file."""
        try:
            if os.path.exists(STATS_FILE_PATH):
                with open(STATS_FILE_PATH, 'r') as f:
                    data = json.load(f)
                    self.current_score = data.get("current_score", 0)
                    self.high_scores = data.get("high_scores", [])
        except Exception as e:
            print(f"Error loading stats: {e}")

    def save_to_file(self):
        """Save game stats to a JSON file."""
        try:
            data = {
                "current_score": self.current_score,
                "high_scores": self.high_scores
            }
            with open(STATS_FILE_PATH, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving stats: {e}")

    def update_current_score(self, points):
        """Update the current score by adding the specified points."""
        self.current_score += points
        self.save_to_file()

    def add_high_score(self, score, date, details=""):
        """Add a new high score to the list of high scores."""
        self.high_scores.append({"score": score, "date": date.strftime("%Y-%m-%d %H:%M:%S"), "details": details})
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep only top 10 scores
        self.save_to_file()

    def get_high_score(self):
        """Get the highest score from the high scores list."""
        if self.high_scores:
            return self.high_scores[0]["score"]
        return 0

    def display_high_scores(self, screen, font):
        """Display high scores on the screen."""
        y_offset = 50
        font_size = 24
        line_height = font_size + 10
        header_text = font.render("High Scores:", True, (255, 255, 255))
        screen.blit(header_text, (10, y_offset))
        y_offset += line_height

        for idx, entry in enumerate(self.high_scores):
            text = font.render(f"{idx+1}. Score: {entry['score']} Date: {entry['date']}", True, (255, 255, 255))
            screen.blit(text, (10, y_offset))
            y_offset += line_height

# Example usage in the main game loop
def main_loop(stats):
    global current_state, running
    running = True
    player = Player()
    player.rect.x = 400
    player.rect.y = 500

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        if current_state == MENU:
            pass  # Placeholder for menu actions

        if current_state == PLAYING:
            player.move()
            screen.blit(player.image, player.rect.topleft)
            player_score_display = font.render(f"Score: {stats.current_score}", True, WHITE)
            screen.blit(player_score_display, (10, 10))

        if current_state == GAME_OVER:
            if stats.current_score > stats.get_high_score():
                stats.add_high_score(stats.current_score, datetime.now())
            pass  # Placeholder for game over actions

        pygame.display.flip()
        clock.tick(FPS)

    # Cleanup
    pygame.quit()
    sys.exit()

# Initialize game stats
stats = GameStats()

# Initialize Pygame and start the main loop
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
current_state = PLAYING

# Start the main loop
initialize_game()
main_loop(stats)
C:\mygit\Slazy\repo\pygamedemo\main.py
Language detected: python
# filepath: C:\mygit\Slazy\repo\pygamedemo\main.py

# Import necessary modules
import pygame
import sys
from game import initialize_game, Player, MENU, PLAYING, GAME_OVER, screen, clock
from enemy import Enemy, WalkingEnemy, FlyingEnemy, create_enemy_group
from items import Item, SpeedBoost, JumpBoost, Invincibility, create_power_up_group
from stats import GameStats

# Initialize game window and states
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
current_state = MENU

# Initialize game components
initialize_game()
stats = GameStats()

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Main game loop
run = True
while run:
    clock.tick(60)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if current_state == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_state = PLAYING
        elif current_state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    initialize_game()
                    current_state = PLAYING
                    stats.current_score = 0

    # Menu
    if current_state == MENU:
        draw_text('Press SPACE to start', font, (255, 255, 255), screen, 250, 275)
        stats.display_high_scores(screen, font)

    # Playing state
    if current_state == PLAYING:
        # Player actions
        player = pygame.sprite.GroupSingle(Player())
        player.update()

        # Player drawing
        screen.fill(BLACK)
        player.draw(screen)
        player_score_display = font.render(f"Score: {stats.current_score}", True, (255, 255, 255))
        screen.blit(player_score_display, (10, 10))

        # Enemy actions
        enemies = create_enemy_group()
        enemies.update()

        # Enemies drawing
        for enemy in enemies:
            screen.blit(enemy.image, enemy.rect.topleft)

        # Items management
        items = create_power_up_group()
        items.update()
        for sprite in pygame.sprite.groupcollide(player, items, dokilla=False, dokillb=False, collided=pygame.sprite.collide_rect):
            spr_type = sprite.__class__.__name__
            if spr_type == 'SpeedBoost' or spr_type == 'JumpBoost' or spr_type == 'Invincibility':
                sprite.apply_effect(player.sprite)

        for item in items:
            screen.blit(item.image, item.rect.topleft)

        # Check game-over condition (for demonstration, let's assume falling off screen ends the game)
        if not player.sprite.rect.colliderect(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)):
            stats.current_score = 0
            current_state = GAME_OVER

    # Game Over
    if current_state == GAME_OVER:
        draw_text('Game Over! Press SPACE to play again', font, (255, 255, 255), screen, 250, 275)

    # Update display
    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()
C:\mygit\Slazy\repo\pygamedemo\game.py
Language detected: python
# game.py

import pygame
import sys

# Game state constants
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)  # Using red color for the player for now
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 

        # Movement attributes
        self.velocity = [0, 0]
        self.acceleration = pygame.math.Vector2(0, 0.5)
        self.is_jumping = False
        self.is_falling = False
        self.ground_y = y

        # Animation and attack variables (placeholder)
        self.animation_index = 0
        self.attack_active = False

    def move_left(self):
        self.velocity[0] = -5

    def move_right(self):
        self.velocity[0] = 5

    def stop_moving(self):
        self.velocity[0] = 0

    def jump(self):
        if not self.is_jumping and not self.is_falling:
            self.velocity[1] = -10
            self.is_jumping = True
            self.is_falling = False

    def handle_physics(self):
        self.velocity[1] += self.acceleration.y

        # Ground collision detection
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.velocity[1] = 0
            self.is_jumping = False
            self.is_falling = False
        else:
            if self.velocity[1] > 0:
                self.is_falling = True
            else:
                self.is_jumping = True

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def animate(self):
        self.animation_index += 1

    def update(self):
        self.handle_physics()
        self.animate()

def initialize_game():
    global player
    player = Player(400, 500)

def main_loop(screen, clock):
    global current_state, running
    running = True
    player = Player(400, 500)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if current_state == PLAYING:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    player.move_left()
                elif keys[pygame.K_RIGHT]:
                    player.move_right()
                else:
                    player.stop_moving()

                if keys[pygame.K_SPACE]:
                    player.jump()

        if current_state == PLAYING:
            screen.fill(BLACK)
            player.update()
            screen.blit(player.image, player.rect.topleft)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

initialize_game()
