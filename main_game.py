import pygame
import random
import math

# --- Configuration ---
WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# --- Classes ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

# New class for bullets fired by enemies
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED) # Red color to distinguish from player bullets
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -7 # Negative because they fly left

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # Spawn randomly on the right side
        self.rect.x = WIDTH + random.randint(10, 300)
        self.rect.y = random.randint(50, HEIGHT - 50)
        self.speed = random.randint(2, 5)
        # New property: Timer to control how often they shoot
        self.shoot_timer = 0

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# --- Main Game Loop ---

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Asterax Clone - Enemy Fire Active")
    clock = pygame.time.Clock()

    # Sprite Groups
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group() # New group for enemy bullets
    enemies = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    score = 0
    font = pygame.font.SysFont("Arial", 24)

    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.right, player.rect.centery)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        # 2. Update logic
        keys = pygame.key.get_pressed()
        player.update(keys)
        
        for bullet in bullets:
            bullet.update()
        
        for eb in enemy_bullets:
            eb.update()
        
        # Update enemies and handle their shooting logic
        for enemy in enemies:
            enemy.update()
            # Each frame, check if the enemy should shoot
            enemy.shoot_timer -= 1
            if enemy.shoot_timer <= 0:
                # Random chance to fire when timer hits zero (roughly every 1 second)
                if random.random() < 0.5: 
                    eb = EnemyBullet(enemy.rect.left, enemy.rect.centery)
                    all_sprites.add(eb)
                    enemy_bullets.add(eb)
                enemy.shoot_timer = 60 # Reset timer (60 frames = ~1 second)

        # Spawn enemies randomly
        if random.random() < 0.03: 
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # 3. Collision Detection
        # Player bullets hitting enemies
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10

        # Enemy bullets hitting player
        if pygame.sprite.spritecollideany(player, enemy_bullets):
            print(f"Game Over! Enemy hit you! Final Score: {score}")
            running = False

        # If player touches any enemy directly
        if pygame.sprite.spritecollideany(player, enemies):
            print(f"Game Over! Crashed into an enemy! Final Score: {score}")
            running = False

        # 4. Rendering
        screen.fill(BLACK)
        all_sprites.draw(screen)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()