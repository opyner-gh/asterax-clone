# entity.py
import math
from config import get_screen_size

class GameObject:
    def __init__(self, x, y, vx=0.0, vy=0.0, angle=0.0, size=10):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.angle, self.size, self.active = angle, size, True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self._wrap()

    def _wrap(self):
        if self.x < -self.size:    self.x += get_screen_size()[0] + self.size * 2
        elif self.x > get_screen_size()[0] + self.size: self.x -= get_screen_size()[0] + self.size * 2
        if self.y < -self.size:    self.y += get_screen_size()[1] + self.size * 2
        elif self.y > get_screen_size()[1] + self.size: self.y -= get_screen_size()[1] + self.size * 2

    def dist_to(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    def collides(self, other):
        return self.dist_to(other) < (self.size + other.size)

    def to_screen(self):
        return (int(self.x), int(self.y))