C:\mygit\BLazy\repo\executable\platformer_game.py
```python
import pygame
import sys

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
PLATFORM_HEIGHT = 50
GRAVITY = 1

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Platformer")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.jumping = False

    def update(self):
        # Apply gravity
        self.change_y += GRAVITY
        
        # Move left/right
        self.rect.x += self.change_x
        
        # Check for collisions
        platform_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
        for platform in platform_hit_list:
            if self.change_x > 0:
                self.rect.right = platform.rect.left
            elif self.change_x < 0:
                self.rect.left = platform.rect.right
        
        # Move up/down
        self.rect.y += self.change_y
        
        # Check and handle collisions for vertical movement
        platform_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
        for platform in platform_hit_list:
            if self.change_y > 0:
                self.rect.bottom = platform.rect.top
                self.jumping = False
            elif self.change_y < 0:
                self.rect.top = platform.rect.bottom
            
            self.change_y = 0

    def jump(self):
        if not self.jumping:
            self.change_y = -10
            self.jumping = True


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create sprite lists
all_sprites_list = pygame.sprite.Group()
platform_list = pygame.sprite.Group()

# Create the player and platforms
player = Player()
player.rect.x = 345
player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE - PLATFORM_HEIGHT
all_sprites_list.add(player)

platform = Platform(300, SCREEN_HEIGHT - PLATFORM_HEIGHT, 150, PLATFORM_HEIGHT)
platform_list.add(platform)
all_sprites_list.add(platform)

# Game loop flag
done = False

# Main game loop
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.change_x = -5
            elif event.key == pygame.K_RIGHT:
                player.change_x = 5
            elif event.key == pygame.K_SPACE:
                player.jump()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change_x = 0

    # Update player position
    all_sprites_list.update()

    # Draw everything
    screen.fill(BLACK)
    all_sprites_list.draw(screen)

    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)

# Exit pygame
pygame.quit()
```
C:\mygit\BLazy\repo\executable\build_executable.py
```python
# filepath: C:\mygit\BLazy\repo\executable\build_game.bat
import os
import sys
from PyInstaller.__main__ import run

def build_executable():
    # Set the current working directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Configure PyInstaller options
    opts = ['platformer_game.py', '--onefile', '--noconsole']
    
    try:
        # Run PyInstaller with the specified options
        run(opts)
        print("Build process completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    build_executable()
```

This script performs the following steps:
1. Imports the required modules.
2. Sets the current working directory to the location of the script.
3. Configures PyInstaller to create a single-file executable without showing a console window.
4. Runs PyInstaller with the configured options.
5. Prints status messages to indicate the success or failure of the build process.

To execute this script, save it as `build_game.py` in the same directory as your `platformer_game.py` and ensure you have PyInstaller installed. You can then run it using the batch command provided:

```batch
# filepath: C:\mygit\BLazy\repo\executable\build_game.bat
python build_game.py
```
