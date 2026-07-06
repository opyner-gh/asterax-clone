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

# --- Constants ---
PLAYER_ANGLE = 0  # Rotation in degrees

# --- Classes ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a surface and rotate it (keeping original size for logic)
        self.original_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.original_image.fill(CYAN)
        # Draw a simple "front" indicator so we can see the rotation
        pygame.draw.rect(self.original_image, WHITE, (15, 10, 10, 20)) 
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.angle = 0

    def update(self):
        # Rotation logic (Degrees)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += 3
        if keys[pygame.K_RIGHT]:
            self.angle -= 3

        # Clamp angle to keep it tidy (optional, but good for logic)
        self.angle = (self.angle + 360) % 360

        # Update the visual rotation
        # Note: Rotate rotates counter-clockwise by default
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center) # Keep center fixed

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Convert degrees to radians for math functions
        rads = math.radians(angle)
        # Calculate velocity based on rotation
        self.vx = math.cos(rads) * 8
        self.vy = math.sin(rads) * 8

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        # Remove if off-screen
        if not (0 <= self.rect.x <= WIDTH and 0 <= self.rect.y <= HEIGHT):
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Calculate direction toward the center/player
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist == 0:
            self.vx, self.vy = 0, 0
        else:
            self.vx = (dx / dist) * 4
            self.vy = (dy / dist) * 4

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if not (0 <= self.rect.x <= WIDTH and 0 <= self.rect.y <= HEIGHT):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        
        # Spawn at random locations outside or near the edges
        side = random.randint(0, 3)
        if side == 0: # Top
            self.rect.centerx = random.randint(0, WIDTH)
            self.rect.centery = random.randint(-50, 50)
        elif side == 1: # Bottom
            self.rect.centerx = random.randint(0, WIDTH)
            self.rect.centery = random.randint(HEIGHT-100, HEIGHT+50)
        elif side == 2: # Left
            self.rect.centerx = random.randint(-100, 50)
            self.rect.centery = random.randint(0, HEIGHT)
        else: # Right
            self.rect.centerx = random.randint(WIDTH-50, WIDTH+100)
            self.rect.centery = random.randint(0, HEIGHT)

        # Movement toward center
        target_x, target_y = WIDTH // 2, HEIGHT // 2
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            self.vx, self.vy = 0, 0
        else:
            # Move at a random speed toward the player
            speed = random.uniform(1, 3)
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed
            
        self.shoot_timer = random.randint(30, 90)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            # Fire toward the player center
            eb = EnemyBullet(self.rect.centerx, self.rect.centery, WIDTH//2, HEIGHT//2)
            all_sprites.add(eb)
            enemy_bullets.add(eb)
            self.shoot_timer = random.randint(40, 100)

# --- Main Game Loop ---

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Asterax - Top Down Mode")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
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
                    # Bullet spawns at player's current rotation angle
                    bullet = Bullet(player.rect.centerx, player.rect.centery, player.angle)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        # 2. Update logic
        all_sprites.update() # This updates bullets, enemies, and the player
        
        # Spawn enemies randomly from edges
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
            print(f"Game Over! Hit by enemy fire! Score: {score}")
            running = False

        # Player colliding with enemies
        if pygame.sprite.spritecollideany(player, enemies):
            print(f"Game Over! Crashed into an enemy! Score: {score}")
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
