# asteroid.py
import math, random, pygame
from entity import GameObject
from config import ROCK_SIZES, ROCK_RADIUS, ROCK_NEXT_SIZE, get_col_rock, get_col_rock_outline

class Asteroid(GameObject):
    def __init__(self, x, y, size_key="big", speed_range=(1.0, 3.0)):
        ang = random.uniform(0, 2 * math.pi)
        spd = random.uniform(*speed_range)
        radius = ROCK_RADIUS.get(size_key, ROCK_SIZES[0][0])
        super().__init__(x, y, math.cos(ang)*spd, math.sin(ang)*spd, size=radius)
        self.size_key = size_key
        self.spin = random.uniform(-1.5, 1.5)
        self._verts = self._gen_shape()

    def _gen_shape(self):
        n = random.randint(7, 12)
        return [(math.cos(2*math.pi*i/n)*self.size*random.uniform(.7,1.15),
                 math.sin(2*math.pi*i/n)*self.size*random.uniform(.7,1.15))
                for i in range(n)]

    def update(self):
        self.angle += self.spin * 0.02
        super().update()

    def split(self, speed_range, split_chance=1.0):
        nk = ROCK_NEXT_SIZE.get(self.size_key)
        if nk is None or random.random() > split_chance:
            return []
        return [Asteroid(self.x+random.uniform(-10,10), self.y+random.uniform(-10,10),
                         nk, speed_range) for _ in range(2)]

    def draw(self, screen):
        x, y = self.to_screen()
        ca, sa = math.cos(self.angle), math.sin(self.angle)
        pts = [(x+int(dx*ca-dy*sa), y+int(dx*sa+dy*ca)) for dx,dy in self._verts]
        if len(pts) >= 3:
            pygame.draw.polygon(screen, get_col_rock(), pts)
            pygame.draw.polygon(screen, get_col_rock_outline(), pts, 2)
