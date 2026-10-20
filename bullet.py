# bullet.py
from entity import Entity
from config import BULLET_LIFE


class Bullet(Entity):
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y, vx=vx, vy=vy, size=3)
        self.life = BULLET_LIFE

    def update(self):
        super().update()
        self.life -= 1
        if self.life <= 0:
            self.active = False
