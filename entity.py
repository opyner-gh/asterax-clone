# entity.py
import math
from config import SCREEN_W, SCREEN_H


class Entity:
    """Base class for anything that moves on screen."""

    def __init__(self, x: float, y: float, vx: float = 0.0, vy: float = 0.0,
                 angle: float = 0.0, size: float = 10):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.angle = angle          # radians
        self.size = size
        self.active = True          # set False to remove from world

    # ── movement ──────────────────────────────────────────────
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self._wrap()

    def _wrap(self):
        """Wrap around screen edges."""
        if self.x < -self.size:
            self.x += SCREEN_W + self.size * 2
        elif self.x > SCREEN_W + self.size:
            self.x -= SCREEN_W + self.size * 2
        if self.y < -self.size:
            self.y += SCREEN_H + self.size * 2
        elif self.y > SCREEN_H + self.size:
            self.y -= SCREEN_H + self.size * 2

    # ── helpers ───────────────────────────────────────────────
    def dist_to(self, other: "Entity") -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return math.hypot(dx, dy)

    def collides(self, other: "Entity") -> bool:
        return self.dist_to(other) < (self.size + other.size)

    def to_screen_coords(self) -> tuple:
        """Return (x, y) clipped to screen for rendering."""
        return (int(self.x), int(self.y))
