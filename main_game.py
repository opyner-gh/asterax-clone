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
        # Create a surface and rotate it. We use a slightly larger size to account for rotation.
        self.original_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.original_image.fill(CYAN)
        # Draw a "front" indicator (a small white rectangle) so you can see the direction
        pygame.draw.rect(self.original_image, WHITE, (15, 10, 10, 20))
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.angle = 0

    def update(self):
        keys = pygame.key.get_pressed()
        # Rotate based on Left/Right keys
        if keys[pygame.K_LEFT]:
            self.angle += 3
        if keys[pygame.K_RIGHT]:
            self.angle -= 3

        # Clamp the angle
        self.angle = (self.angle + 360) % 360
        
        # Update image and rect based on rotation
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        # Fix the rectangle position so it doesn't "wobble" when rotating
        self.rect = self.image.get_rect(center=self.rect.center)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Calculate trajectory using trigonometry
        rads = math.radians(angle)
        self.vx = math.cos(rads) * 8
        self.vy = math.sin(rads) * 8

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if not (0 <= self.rect.x <= WIDTH and 0 <= self.rect.y <= HEIGHT):
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Calculate vector towards the player (the center of the screen)
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
        
        # Random spawn point on the edges
        side = random.randint(0, 3)
        if side == 0: # Top
            self.rect.centerx = random.randint(0, WIDTH)
            self.rect.centery = random.randint(-50, 50)
        elif side == 1: # Bottom
            self.rect.centerx = random.randint(0, WIDTH)
            self.rect.centery = random.randint(HEIGHT-50, HEIGHT+50)
        elif side == 2: # Left
            self.rect.centerx = random.randint(-100, 50)
            self.rect.centery = random.randint(0, HEIGHT)
        else: # Right
            self.rect.centerx = random.randint(WIDTH-50, WIDTH+100)
            self.rect.centery = random.randint(0, HEIGHT)

        # Movement towards center
        target_x, target_y = WIDTH // 2, HEIGHT // 2
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            self.vx, self.vy = 0, 0
        else:
            speed = random.uniform(1, 3)
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed
            
        self.shoot_timer = random.randint(40, 90)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.shoot_timer -= 1
        return self.shoot_timer <= 0

# --- Main Game Loop ---

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Asterax - Circular Combat")
    clock = pygame.time.Clock()

    # Sprite Groups
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
                    # Player bullet follows current rotation
                    new_bullet = Bullet(player.rect.centerx, player.rect.centery, player.angle)
                    all_sprites.add(new_bullet)
                    bullets.add(new_bullet)

        # 2. Update logic
        all_sprites.update()

        # Spawn enemies
        if random.random() < 0.03:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Handle enemy shooting (Logic moved here to fix Scope Error)
        for enemy in enemies:
            if enemy.shoot_timer <= 0:
                eb = EnemyBullet(enemy.rect.centerx, enemy.rect.centery, WIDTH//2, HEIGHT//2)
                all_sprites.add(eb)
                enemy_bullets.add(eb)
                # Reset the timer specifically for this enemy object
                enemy.shoot_timer = random.randint(40, 100)

        # 3. Collision Detection
        # Player bullets hitting enemies
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10

        # Enemy bullets hitting player
        if pygame.sprite.spritecollideany(player, enemy_bullets):
            print(f"Game Over! Hit by enemy fire! Final Score: {score}")
            running = False

        # Player colliding with enemies
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
