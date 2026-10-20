# game.py
import pygame
import random
import math

from config import (SCREEN_W, SCREEN_H, FPS, BULLET_SPEED, BULLET_MAX_ACTIVE,
                    INITIAL_ASTEROID_COUNT, ASTEROID_RESPAWN_FRAMES)
from player import Player
from asteroid import Asteroid
from bullet import Bullet


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()
        self.running = True
        self.reset()

    # ── state ─────────────────────────────────────────────────
    def reset(self):
        self.player = Player(SCREEN_W // 2, SCREEN_H // 2)
        self.player.invuln_timer = 0
        self.asteroids: list[Asteroid] = []
        self.bullets: list[Bullet] = []
        self.score = 0
        self.lives = 3
        self.spawning = False
        self.spawn_timer = 0
        self._spawn_initial_wave()

    def _spawn_initial_wave(self):
        for _ in range(INITIAL_ASTEROID_COUNT):
            x, y = self._safe_spawn_point()
            self.asteroids.append(Asteroid(x, y, "big"))

    def _safe_spawn_point(self) -> tuple:
        """Pick a position at least 120px from the player."""
        for _ in range(200):
            x = random.uniform(0, SCREEN_W)
            y = random.uniform(0, SCREEN_H)
            if math.hypot(x - self.player.x, y - self.player.y) > 150:
                return x, y
        return (50, 50)

    # ── input ─────────────────────────────────────────────────
    def _handle_input(self, events):
        keys = pygame.key.get_pressed()

        self.player.thrusting = keys[pygame.K_UP] or keys[pygame.K_w]
        self.player.turning = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.turning = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.turning = 1
        self.player.firing = keys[pygame.K_SPACE] or keys[pygame.K_s]

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_r:
                    self.reset()

    # ── spawning ──────────────────────────────────────────────
    def _spawn_bullet(self):
        active = len(self.bullets)
        if active >= BULLET_MAX_ACTIVE or self.player.shoot_cooldown > 0:
            return
        angle = self.player.angle
        # spawn at the tip of the ship
        sx = self.player.x + math.cos(angle) * self.player.size
        sy = self.player.y + math.sin(angle) * self.player.size
        vx = math.cos(angle) * BULLET_SPEED + self.player.vx
        vy = math.sin(angle) * BULLET_SPEED + self.player.vy
        self.bullets.append(Bullet(sx, sy, vx, vy))
        self.player.shoot_cooldown = 8

    def _spawn_wave(self):
        """Called after the board is clear, to keep the game going."""
        for _ in range(INITIAL_ASTEROID_COUNT):
            x, y = self._safe_spawn_point()
            self.asteroids.append(Asteroid(x, y, "big"))
        self.spawning = False

    # ── collisions ────────────────────────────────────────────
    def _check_collisions(self):
        # Bullets vs Asteroids
        for b in self.bullets:
            for a in self.asteroids:
                if not b.active or not a.active:
                    continue
                if b.collides(a):
                    b.active = False
                    a.active = False
                    self.score += int(1000 / a.size)
                    # split
                    new_rocks = a.split()
                    self.asteroids.extend(new_rocks)
                    break

        # Player vs Asteroids
        if self.player.alive:
            for a in self.asteroids:
                if a.active and self.player.collides(a):
                    self._player_hit()
                    break

    def _player_hit(self):
        self.lives -= 1
        if self.lives <= 0:
            self.running = False
            return
        self.player.x = SCREEN_W // 2
        self.player.y = SCREEN_H // 2
        self.player.vx = 0
        self.player.vy = 0
        self.player.angle = math.radians(-90)
        self.player.invuln_timer = 120  # brief invuln

    # ── main loop ─────────────────────────────────────────────
    def run(self):
        while self.running:
            events = pygame.event.get()
            self._handle_input(events)

            # Update
            self.player.update()
            if self.player.firing:
                self._spawn_bullet()

            for b in self.bullets:
                b.update()
            for a in self.asteroids:
                a.update()

            self._check_collisions()

            # Cleanup
            self.bullets = [b for b in self.bullets if b.active]
            self.asteroids = [a for a in self.asteroids if a.active]

            # Wave clear → respawn
            if not self.asteroids and not self.spawning:
                self.spawning = True
                self.spawn_timer = ASTEROID_RESPAWN_FRAMES
            if self.spawning:
                self.spawn_timer -= 1
                if self.spawn_timer <= 0:
                    self._spawn_wave()

            self._render()
            self.clock.tick(FPS)

        pygame.quit()

    # ── rendering ─────────────────────────────────────────────
    def _render(self):
        self.screen.fill((0, 0, 0))

        # Asteroids
        for a in self.asteroids:
            self._draw_asteroid(a)

        # Bullets
        for b in self.bullets:
            px, py = b.to_screen_coords()
            pygame.draw.circle(self.screen, (255, 255, 100), (px, py), 2)

        # Player
        self._draw_player()

        # HUD
        font = pygame.font.SysFont(None, 24)
        score_surf = font.render(f"Score: {self.score}", True, (200, 200, 200))
        lives_surf = font.render(f"Lives: {self.lives}", True, (200, 200, 200))
        self.screen.blit(score_surf, (12, 12))
        self.screen.blit(lives_surf, (12, 38))

        if not self.running:
            msg = font.render("GAME OVER — press R to restart", True, (255, 80, 80))
            rect = msg.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
            self.screen.blit(msg, rect)

        pygame.display.flip()

    def _draw_player(self):
        if self.player.invuln_timer > 0 and (self.player.invuln_timer // 4) % 2 == 0:
            return  # blink
        x, y = self.player.to_screen_coords()
        a = self.player.angle
        s = self.player.size
        # simple triangle
        nose = (x + int(math.cos(a) * s), y + int(math.sin(a) * s))
        left = (x + int(math.cos(a + 2.5) * s), y + int(math.sin(a + 2.5) * s))
        right = (x + int(math.cos(a - 2.5) * s), y + int(math.sin(a - 2.5) * s))
        pygame.draw.polygon(self.screen, (255, 255, 255), [nose, left, right])
        if self.player.thrusting:
            flame = (x + int(math.cos(a) * -s * 0.6), y + int(math.sin(a) * -s * 0.6))
            pygame.draw.line(self.screen, (255, 160, 0), flame,
                             (x + int(math.cos(a) * -s * 1.2),
                              y + int(math.sin(a) * -s * 1.2)), 3)

    def _draw_asteroid(self, a: Asteroid):
        x, y = a.to_screen_coords()
        pts = []
        for dx, dy in a._verts:
            # rotate vertex by a.angle
            ca, sa = math.cos(a.angle), math.sin(a.angle)
            rx = dx * ca - dy * sa
            ry = dx * sa + dy * ca
            pts.append((x + int(rx), y + int(ry)))
        if len(pts) >= 3:
            pygame.draw.polygon(self.screen, (180, 180, 180), pts)
            pygame.draw.polygon(self.screen, (120, 120, 120), pts, 2)
