import pygame
import sys

# --- Configuration & Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Create a basic triangle for the ship
        # Facing RIGHT as requested (this is 0 degrees in our logic)
        surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(surf, WHITE, [(40, 20), (0, 0), (0, 40)])
        self.base_image = surf
        
        # State variables as Vector2 and floats
        self.pos = pygame.math.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.vel = pygame.math.Vector2(0, 0)
        self.angle = 0.0
        
        # Update visual representation
        self.image = self.base_image
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        keys = pygame.key.get_pressed()

        # 1. Rotation Logic: Left/Right arrows rotate the ship
        if keys[pygame.K_LEFT]:
            self.angle += 3
        if keys[pygame.K_RIGHT]:
            self.angle -= 3

        # 2. Thrust Logic: Up arrow applies thrust based on current angle
        if keys[pygame.K_UP]:
            # Use Vector2.rotate() to calculate direction without using the math module
            # Note: We use -self.angle because Pygame's Y-axis is inverted compared to standard math
            thrust = pygame.math.Vector2(1, 0).rotate(-self.angle)
            self.vel += thrust

        # 3. Friction logic: Multiply velocity by 0.98 every frame
        self.vel *= 0.98

        # 4. Movement Logic: Update position based on velocity
        self.pos += self.vel

        # 5. Screen Wrapping Logic
        if self.pos.x < 0:
            self.pos.x += SCREEN_WIDTH
        elif self.pos.x > SCREEN_WIDTH:
            self.pos.x -= SCREEN_WIDTH
        
        if self.pos.y < 0:
            self.pos.y += SCREEN_HEIGHT
        elif self.pos.y > SCREEN_HEIGHT:
            self.pos.y -= SCREEN_HEIGHT

        # 6. Rotation & Drawing Logic
        # FIX: Use pygame.transform.rotate() instead of .rotate() on the surface object
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids - Vector Logic")
    clock = pygame.time.Clock()

    # Sprite Groups
    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    running = True
    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Update Logic
        all_sprites.update()

        # Rendering logic
        screen.fill(BLACK)
        all_sprites.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
