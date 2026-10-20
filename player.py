# player.py
import math, pygame
from entity import GameObject
from ships import ShipDef
from upgrades import apply_upgrades
from config import get_col_thrust, get_col_shield, get_col_ship_outline

class Player(GameObject):
    def __init__(self, ship: ShipDef, upgrades: dict[str, int], x: float, y: float):
        self.ship = ship
        self.upgrades = upgrades
        self.stats = apply_upgrades(ship, upgrades)

        super().__init__(x, y, angle=math.radians(-90), size=ship.size)

        self.thrusting = False
        self.turning = 0
        self.firing = False
        self.shoot_cd = 0
        self.invuln = 0
        self.shield_charges = self.stats["shield_charges"]

    # ── reset for a new level (keep upgrades, reset position) ──
    def reset_position(self, x, y, invuln=120):
        self.x, self.y, self.vx, self.vy = x, y, 0, 0
        self.angle = math.radians(-90)
        self.invuln = invuln

    def update(self):
        rad = math.radians(self.stats["turn_speed"])
        if self.turning == -1: self.angle -= rad
        elif self.turning == 1: self.angle += rad

        if self.thrusting:
            self.vx += math.cos(self.angle) * self.stats["thrust"]
            self.vy += math.sin(self.angle) * self.stats["thrust"]

        self.vx *= 0.985
        self.vy *= 0.985

        if self.shoot_cd > 0: self.shoot_cd -= 1
        if self.invuln > 0:   self.invuln   -= 1
        super().update()

    @property
    def alive(self):
        return self.invuln <= 0

    # ── render ────────────────────────────────────────────────
    def draw(self, screen, font):
        if self.invuln > 0 and (self.invuln // 4) % 2:
            return
        x, y = self.to_screen()
        pts = []
        for dx, dy in self.ship.shape:
            ca, sa = math.cos(self.angle), math.sin(self.angle)
            pts.append((x + int(dx*ca - dy*sa), y + int(dx*sa + dy*ca)))
        if len(pts) >= 3:
            pygame.draw.polygon(screen, self.ship.color, pts)
            pygame.draw.polygon(screen, get_col_ship_outline(), pts, 1)
        if self.shield_charges > 0:
            pygame.draw.circle(screen, get_col_shield(), (x, y), int(self.size * 1.45), 2)
        if self.thrusting:
            bx = x + int(math.cos(self.angle) * -self.size * 1.3)
            by = y + int(math.sin(self.angle) * -self.size * 1.3)
            pygame.draw.line(screen, get_col_thrust(),
                             (x + int(math.cos(self.angle)*-self.size*0.5),
                              y + int(math.sin(self.angle)*-self.size*0.5)),
                             (bx, by), 3)
