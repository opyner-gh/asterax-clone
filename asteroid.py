# asteroid.py
import math
import random
from entity import Entity
from config import ASTEROID_SIZES, ASTEROID_BASE_SPEED


class Asteroid(Entity):
    def __init__(self, x, y, size_key: str = "big"):
        radius = ASTEROID_SIZES[0][0]
        for r, k in ASTEROID_SIZES:
            if k == size_key:
                radius = r
                break

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(*ASTEROID_BASE_SPEED)

        super().__init__(x, y,
                         vx=math.cos(angle) * speed,
                         vy=math.sin(angle) * speed,
                         size=radius)
        self.size_key = size_key
        self.spin = random.uniform(-1.5, 1.5)  # visual rotation
        # Pre-generate a wobbly polygon so it looks like a rock
        self._generate_shape()

    def _generate_shape(self):
        self._verts = []
        n = random.randint(7, 12)
        for i in range(n):
            a = 2 * math.pi * i / n
            r = self.size * random.uniform(0.7, 1.15)
            self._verts.append((math.cos(a) * r, math.sin(a) * r))

    def update(self):
        self.angle += self.spin * 0.02
        super().update()

    def split(self):
        """Return a list of smaller asteroids, or [] if this was the smallest."""
        idx = next(i for i, (_, k) in enumerate(ASTEROID_SIZES) if k == self.size_key)
        if idx >= len(ASTEROID_SIZES) - 1:
            return []  # smallest, no further split
        next_key = ASTEROID_SIZES[idx + 1][1]
        return [
            Asteroid(self.x + random.uniform(-10, 10),
                     self.y + random.uniform(-10, 10),
                     size_key=next_key)
            for _ in range(2)
        ]
