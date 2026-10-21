# game.py
import pygame
import math
import random
from config import (ROCK_POINTS, ROCK_CREDITS, get_screen_size, get_fps,
                    get_col_bg, get_col_star, get_col_bullet, get_col_ui_text, get_col_danger)
from player import Player
from asteroid import Asteroid
from bullet import Bullet
from ships import SHIP_ROSTER
from levels import level_for
from ship_select import ShipSelect
from shop import Shop

# ── tiny starfield ────────────────────────────────────────────
def make_stars(n=80):
    return [(random.randint(0, get_screen_size()[0]), random.randint(0, get_screen_size()[1]),
             random.choice([get_col_star(), (40,40,50)])) for _ in range(n)]

class Game:
    # states
    SELECT = "select"
    PLAY   = "play"
    SHOP   = "shop"
    OVER   = "over"

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(get_screen_size())
        pygame.display.set_caption("ASTERAX")
        self.clock = pygame.time.Clock()
        self.stars = make_stars()
        self.font  = pygame.font.SysFont("monospace", 20)
        self.font_big = pygame.font.SysFont("monospace", 32, bold=True)

        self.state = self.SELECT
        self.high_level = 0          # highest level cleared (for ship unlocks)

        # current sub-state object (ShipSelect or Shop)
        self.select_ui: ShipSelect | None = None
        self.shop_ui: Shop | None = None

        self._reset_run()
        self._enter_select()

    def _reset_run(self):
        """Reset all per-run gameplay state while preserving meta-progression (high_level)."""
        self.ship = SHIP_ROSTER[0]
        self.upgrades: dict[str, int] = {}
        self.credits = 0
        self.level = 0
        self.score = 0
        self.lives = 3
        self.player: Player | None = None
        self.asteroids: list[Asteroid] = []
        self.bullets: list[Bullet] = []

    # ── state transitions ─────────────────────────────────────
    def _enter_select(self):
        self.state = self.SELECT
        self.select_ui = ShipSelect(max_unlocked=self.high_level)

    def _enter_play(self):
        self.state = self.PLAY
        self.player = Player(self.ship, self.upgrades, get_screen_size()[0]//2, get_screen_size()[1]//2)
        self.player.invuln = 0
        self.asteroids = []
        self.bullets = []
        if self.level == 0:
            self.lives = 3 + self.player.stats["extra_lives"]
        self._spawn_wave()

    def _enter_shop(self):
        self.state = self.SHOP
        self.shop_ui = Shop(self.credits, self.upgrades, self.level)

    def _enter_over(self):
        self.state = self.OVER

    # ── spawning ──────────────────────────────────────────────
    def _spawn_wave(self):
        lvl = level_for(self.level)
        for _ in range(lvl.big_rocks):
            x, y = self._safe_point()
            self.asteroids.append(Asteroid(x, y, "big",
                                           (lvl.rock_speed_min, lvl.rock_speed_max)))

    def _safe_point(self):
        for _ in range(200):
            x, y = random.uniform(40, get_screen_size()[0]-40), random.uniform(40, get_screen_size()[1]-40)
            if self.player and math.hypot(x-self.player.x, y-self.player.y) > 160:
                return x, y
        return (60, 60)

    # ── input ─────────────────────────────────────────────────
    def _handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                return "quit"
        result = None
        if self.state == self.SELECT:
            result = self.select_ui.handle(events)
            if result == "quit":
                return "quit"
            if self.select_ui.confirmed:
                self.ship = self.select_ui.selected_ship
                self.level = 0
                self._enter_play()
        elif self.state == self.SHOP:
            result = self.shop_ui.handle(events)
            if self.shop_ui.done:
                old_hull = self.upgrades.get("hull", 0)
                new_hull = self.shop_ui.final_owned.get("hull", 0)
                if new_hull > old_hull:
                    self.lives += (new_hull - old_hull)
                self.upgrades = self.shop_ui.final_owned
                self.credits = self.shop_ui.remaining_credits
                self.level += 1
                self._enter_play()
        elif self.state == self.OVER:
            for e in events:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        self._reset_run()
                        self._enter_select()
                    elif e.key == pygame.K_ESCAPE:
                        return "quit"
        return result

    def _play_input(self):
        keys = pygame.key.get_pressed()
        p = self.player
        p.thrusting = keys[pygame.K_UP] or keys[pygame.K_w]
        p.turning = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  p.turning = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  p.turning =  1
        p.firing = keys[pygame.K_SPACE]

    # ── play update ───────────────────────────────────────────
    def _update_play(self):
        self.player.update()

        if self.player.firing and self.player.shoot_cd <= 0:
            self._fire()

        for b in self.bullets: b.update()
        for a in self.asteroids: a.update()

        self._collisions()
        self.bullets   = [b for b in self.bullets if b.active]
        self.asteroids = [a for a in self.asteroids if a.active]

        # wave cleared?
        if not self.asteroids:
            self.score += 500 + self.level * 100
            self.credits += 75 + self.level * 25
            self.high_level = max(self.high_level, self.level)
            self._enter_shop()

    def _fire(self):
        p = self.player
        max_active = p.stats["max_bullets"]
        if len(self.bullets) >= max_active:
            return
        count = p.stats.get("bullets_per_shot", 1)
        spread_step = math.radians(10)
        bs = p.stats["bullet_speed"]
        for i in range(count):
            if len(self.bullets) >= max_active:
                break
            offset = (i - (count - 1) / 2.0) * spread_step
            a = p.angle + offset
            bx = p.x + math.cos(a) * p.size
            by = p.y + math.sin(a) * p.size
            self.bullets.append(Bullet(bx, by,
                                       math.cos(a)*bs + p.vx,
                                       math.sin(a)*bs + p.vy))
        p.shoot_cd = p.stats["bullet_cooldown"]

    def _collisions(self):
        lvl = level_for(self.level)
        # bullet ↔ rock
        new_rocks: list[Asteroid] = []
        for b in self.bullets:
            if not b.active:
                continue
            for a in self.asteroids:
                if a.active and b.collides(a):
                    b.active = False
                    a.active = False
                    pts = ROCK_POINTS[a.size_key]
                    self.score += pts
                    self.credits += ROCK_CREDITS[a.size_key]
                    new_rocks.extend(a.split(
                        (lvl.rock_speed_min, lvl.rock_speed_max),
                        lvl.rock_split_chance))
                    break
        if new_rocks:
            self.asteroids.extend(new_rocks)
        # player ↔ rock
        if self.player.alive:
            for a in self.asteroids:
                if a.active and self.player.collides(a):
                    self._player_hit()
                    break

    def _player_hit(self):
        p = self.player
        if p.shield_charges > 0:
            p.shield_charges -= 1
            p.invuln = 60
            return
        self.lives -= 1
        if self.lives <= 0:
            self._enter_over()
            return
        p.reset_position(get_screen_size()[0]//2, get_screen_size()[1]//2, invuln=120)

    # ── render ────────────────────────────────────────────────
    def _draw_bg(self):
        self.screen.fill(get_col_bg())
        for sx, sy, sc in self.stars:
            pygame.draw.rect(self.screen, sc, (sx, sy, 2, 2))

    def _draw_play(self):
        for a in self.asteroids: a.draw(self.screen)
        for b in self.bullets:
            px, py = b.to_screen()
            pygame.draw.circle(self.screen, get_col_bullet(), (px, py), 2)
        self.player.draw(self.screen, self.font)

        # HUD
        shield_str = f"   Shield {'◆'*self.player.shield_charges}" if self.player.shield_charges > 0 else ""
        hud = self.font.render(f"LV {self.level+1}   Score {self.score}   "
                               f"Lives {'♥'*self.lives}{shield_str}   Cr {self.credits}",
                               True, get_col_ui_text())
        self.screen.blit(hud, (12, 10))
        ship_tag = self.font.render(f"[{self.ship.name}]", True, (120,120,130))
        self.screen.blit(ship_tag, (get_screen_size()[0] - ship_tag.get_width() - 12, 10))

    def _draw_over(self):
        self._draw_bg()
        t1 = self.font_big.render("GAME OVER", True, get_col_danger())
        t2 = self.font.render(f"Score {self.score}   Level reached {self.level+1}", True, get_col_ui_text())
        t3 = self.font.render("ENTER: new game    ESC: quit", True, (130,130,140))
        cx = get_screen_size()[0] // 2
        self.screen.blit(t1, (cx - t1.get_width()//2, get_screen_size()[1]//2 - 60))
        self.screen.blit(t2, (cx - t2.get_width()//2, get_screen_size()[1]//2))
        self.screen.blit(t3, (cx - t3.get_width()//2, get_screen_size()[1]//2 + 40))

    def render(self):
        if self.state == self.SELECT:
            self.select_ui.draw(self.screen)
        elif self.state == self.PLAY:
            self._draw_bg()
            self._draw_play()
        elif self.state == self.SHOP:
            self.shop_ui.draw(self.screen)
        elif self.state == self.OVER:
            self._draw_over()
        pygame.display.flip()

    # ── main loop ─────────────────────────────────────────────
    def run(self):
        while True:
            events = pygame.event.get()
            quit_signal = self._handle_events(events)
            if quit_signal == "quit":
                pygame.quit(); return

            if self.state == self.PLAY:
                self._play_input()
                self._update_play()
                if self.state != self.PLAY:
                    pass  # state changed (e.g. entered shop) — skip render below
            self.render()
            self.clock.tick(get_fps())
