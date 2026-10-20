# ship_select.py
import pygame
from ships import SHIP_ROSTER
from config import (get_screen_size, get_col_bg, get_col_ui_text, get_col_ui_highlight,
                    get_col_ui_border, get_col_ui_bg)

class ShipSelect:
    def __init__(self, max_unlocked: int):
        """max_unlocked = highest level the player has cleared (0-indexed)."""
        self.unlocked = [s for s in SHIP_ROSTER if s.unlock_level <= max_unlocked]
        self.cursor = 0
        self.confirmed = False
        self.font_big  = pygame.font.SysFont("monospace", 28, bold=True)
        self.font_small= pygame.font.SysFont("monospace", 16)

    def handle(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return "quit"
                if e.key in (pygame.K_RIGHT, pygame.K_d):
                    self.cursor = (self.cursor + 1) % len(self.unlocked)
                elif e.key in (pygame.K_LEFT, pygame.K_a):
                    self.cursor = (self.cursor - 1) % len(self.unlocked)
                elif e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.confirmed = True
        return None

    def draw(self, screen):
        screen.fill(get_col_bg())
        title = self.font_big.render("SELECT YOUR SHIP", True, get_col_ui_highlight())
        screen.blit(title, (get_screen_size()[0]//2 - title.get_width()//2, 50))

        ship = self.unlocked[self.cursor]
        cx, cy = get_screen_size()[0]//2, get_screen_size()[1]//2 - 20

        # draw ship large (scaled ×3)
        scale = 3
        pts = [(cx + dx*scale, cy + dy*scale) for dx, dy in ship.shape]
        pygame.draw.polygon(screen, ship.color, pts)
        pygame.draw.polygon(screen, get_col_ui_border(), pts, 2)

        # stats panel
        panel_y = cy + 60
        stats = [
            ("THRUST",    ship.thrust,       0.5),
            ("TURN",      ship.turn_speed,   7.0),
            ("BULLET SPD",ship.bullet_speed,10.0),
            ("FIRE RATE", 10/ship.bullet_cooldown, 2.0),
            ("MAX BULLETS",ship.max_bullets, 8),
        ]
        for i, (label, val, maxv) in enumerate(stats):
            y = panel_y + i * 26
            screen.blit(self.font_small.render(label, True, get_col_ui_text()), (cx - 140, y))
            # bar
            bar_w = int(min(1.0, val / maxv) * 120)
            pygame.draw.rect(screen, get_col_ui_border(), (cx + 10, y + 4, 120, 10))
            pygame.draw.rect(screen, get_col_ui_highlight(), (cx + 10, y + 4, bar_w, 10))

        name = self.font_big.render(ship.name, True, get_col_ui_text())
        screen.blit(name, (cx - name.get_width()//2, panel_y + len(stats)*26 + 20))

        hint = self.font_small.render("← → select    ENTER confirm", True, (120,120,130))
        screen.blit(hint, (get_screen_size()[0]//2 - hint.get_width()//2, get_screen_size()[1] - 40))

        # lock indicator
        locked = [s.name for s in SHIP_ROSTER if s not in self.unlocked]
        if locked:
            lock_txt = self.font_small.render(f"Locked: {', '.join(locked)}", True, (90,90,100))
            screen.blit(lock_txt, (get_screen_size()[0]//2 - lock_txt.get_width()//2, 200))

    @property
    def selected_ship(self):
        return self.unlocked[self.cursor]