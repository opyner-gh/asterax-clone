# bullet.py
from entity import GameObject
from config import BULLET_LIFE, get_col_bullet

class Bullet(GameObject):
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y, vx, vy, size=3)
        self.life = BULLET_LIFE
    def update(self):
        super().update()
        self.life -= 1
        if self.life <= 0: self.active = False