# player.py
import math
from entity import Entity
from config import (PLAYER_SIZE, PLAYER_THRUST, PLAYER_TURN_SPEED,
                    PLAYER_FRICTION, PLAYER_INVULN_FRAMES)


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, angle=math.radians(-90), size=PLAYER_SIZE)
        self.thrusting = False
        self.turning = 0            # -1 left, 0 none, +1 right
        self.firing = False
        self.invuln_timer = 0
        self.shoot_cooldown = 0

    def update(self):
        # Turning
        if self.turning == -1:
            self.angle -= math.radians(PLAYER_TURN_SPEED)
        elif self.turning == 1:
            self.angle += math.radians(PLAYER_TURN_SPEED)

        # Thrust
        if self.thrusting:
            self.vx += math.cos(self.angle) * PLAYER_THRUST
            self.vy += math.sin(self.angle) * PLAYER_THRUST

        # Friction / drag
        self.vx *= PLAYER_FRICTION
        self.vy *= PLAYER_FRICTION

        # Cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.invuln_timer > 0:
            self.invuln_timer -= 1

        super().update()

    @property
    def alive(self) -> bool:
        return self.invuln_timer <= 0

    def kill(self):
        self.invuln_timer = PLAYER_INVULN_FRAMES
        self.vx = 0
        self.vy = 0
