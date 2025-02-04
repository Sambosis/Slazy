C:\mygit\BLazy\repo\webappdemo\game.py
Language detected: python
import pygame

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 1
PLAYER_JUMP_VELOCITY = -15
PLATFORM_COLOR = GREEN
ENEMY_COLOR = RED
ITEM_COLOR = BLUE
BACKGROUND_COLOR = WHITE

# Sprite Sheets (Placeholders - Replace with actual sprites)
PLAYER_SPRITESHEET = "player_spritesheet.png"  # Placeholder
ENEMY_SPRITESHEET = "enemy_spritesheet.png"    # Placeholder
ITEM_SPRITESHEET = "item_spritesheet.png"     # Placeholder

# --- Helper Functions ---
def load_sprite_sheet(filename, rows, cols):
    sprite_sheet = pygame.image.load(filename).convert_alpha()
    width = sprite_sheet.get_width() // cols
    height = sprite_sheet.get_height() // rows
    sprite_list = []
    for row in range(rows):
        for col in range(cols):
            x = col * width
            y = row * height
            image = pygame.Surface([width, height], pygame.SRCALPHA, 32).convert_alpha()
            image.blit(sprite_sheet, (0, 0), (x, y, width, height))
            sprite_list.append(image)
    return sprite_list

# --- Classes ---

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Placeholder sprite - Replace with actual plumber spritesheet loading and animation
        self.image = pygame.Surface([30, 50], GREEN)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.is_jumping = False
        self.powerup_state = None # e.g., 'mushroom', 'star'
        self.score = 0

    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY

        # Movement based on keys (Example - refine movement logic)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = PLAYER_JUMP_VELOCITY
            self.is_jumping = True

        # Update vertical position
        self.rect.y += self.velocity_y

        # Keep player within screen bounds (basic - refine as needed)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.is_jumping = False # Reset jump when landing on ground

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = PLAYER_JUMP_VELOCITY
            self.is_jumping = True

    def power_up(self, powerup_type):
        if powerup_type == 'mushroom':
            self.powerup_state = 'mushroom' # Example effect - can change player size or abilities
            print("Mushroom Power-up!")
        elif powerup_type == 'star':
            self.powerup_state = 'star' # Example effect - invincibility or speed boost
            print("Star Power-up!")

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Placeholder sprite
        self.image = pygame.Surface([30, 30], RED)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = 2 # Basic horizontal movement
        self.is_alive = True
        self.death_animation_frame = 0 # For death animation

    def update(self):
        if self.is_alive:
            self.rect.x += self.velocity_x
            if self.rect.right > SCREEN_WIDTH or self.rect.left < 0: # Basic screen edge turning
                self.velocity_x *= -1
        else:
            # Death animation - placeholder
            self.death_animation_frame += 1
            if self.death_animation_frame > 10: # Example - remove after 10 frames
                self.kill() # Remove from all sprite groups

    def die(self):
        if self.is_alive:
            self.is_alive = False
            self.velocity_x = 0 # Stop movement
            # Implement death animation logic here (e.g., change sprite, play animation)
            print("Enemy Died!")


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height], PLATFORM_COLOR)
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type): # item_type: 'mushroom', 'star', etc.
        super().__init__()
        self.item_type = item_type
        self.image = pygame.Surface([25, 25], ITEM_COLOR) # Placeholder
        self.image.fill(ITEM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer Game")
        self.clock = pygame.time.Clock()
        self.player = Player(50, SCREEN_HEIGHT - 100)
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.all_sprites.add(self.player)

        # Create some platforms
        platform = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50) # Ground
        self.platforms.add(platform)
        self.all_sprites.add(platform)
        platform = Platform(200, SCREEN_HEIGHT - 200, 200, 30)
        self.platforms.add(platform)
        self.all_sprites.add(platform)

        # Create some enemies
        enemy = Enemy(400, SCREEN_HEIGHT - 70)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

        # Create some items
        item = Item(300, SCREEN_HEIGHT - 250, 'mushroom')
        self.items.add(item)
        self.all_sprites.add(item)
        item = Item(350, SCREEN_HEIGHT - 250, 'star')
        self.items.add(item)
        self.all_sprites.add(item)


        self.scroll_x = 0
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.game_over = False


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

            self.update()
            self.draw()
            self.clock.tick(60) # Limit to 60 FPS

        pygame.quit()

    def update(self):
        if self.game_over:
            return

        self.player.update()
        self.enemies.update() # Update enemies

        # --- Collision Detection ---
        # Platform collision
        platform_collisions = pygame.sprite.spritecollide(self.player, self.platforms, False)
        for platform in platform_collisions:
            if self.player.velocity_y > 0: # Falling down
                self.player.rect.bottom = platform.rect.top
                self.player.velocity_y = 0
                self.player.is_jumping = False # Reset jump when landing
            elif self.player.velocity_y < 0: # Jumping up and hitting platform
                self.player.rect.top = platform.rect.bottom
                self.player.velocity_y = 0

        # Enemy collision (Player stomping on enemy)
        enemy_collisions = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in enemy_collisions:
            if self.player.rect.bottom <= enemy.rect.top + 10 and self.player.velocity_y >= 0: # Stomping condition
                self.player.velocity_y = PLAYER_JUMP_VELOCITY / 2 # Bounce slightly off enemy
                enemy.die()
                self.score += 100 # Example score increase
            else:
                # Player touches enemy from side or below - Game Over (Example)
                self.game_over = True
                print("Game Over!")


        # Item collision
        item_collisions = pygame.sprite.spritecollide(self.player, self.items, True) # True to remove item
        for item in item_collisions:
            self.player.power_up(item.item_type)
            if item.item_type == 'mushroom' or item.item_type == 'star':
                self.score += 200


        # --- Scrolling (Basic horizontal scrolling) ---
        scroll_speed = 0
        if self.player.rect.right > SCREEN_WIDTH * 0.75 and self.scroll_x < 1000:  # Example scroll boundary
            scroll_speed = self.player.rect.right - SCREEN_WIDTH * 0.75
            self.scroll_x += scroll_speed
            for sprite in self.all_sprites:
                sprite.rect.x -= scroll_speed
        elif self.player.rect.left < SCREEN_WIDTH * 0.25 and self.scroll_x > 0:
            scroll_speed = SCREEN_WIDTH * 0.25 - self.player.rect.left
            self.scroll_x -= scroll_speed
            for sprite in self.all_sprites:
                sprite.rect.x += scroll_speed


    def draw(self):
        self.screen.fill(BACKGROUND_COLOR) # Clear screen

        # Draw all sprites
        for entity in self.all_sprites:
            self.screen.blit(entity.image, entity.rect)

        # Display score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = self.font.render("Game Over", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip() # Update the display


if __name__ == '__main__':
    game = Game()
    game.run()
