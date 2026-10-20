# ships.py
from dataclasses import dataclass, field

def default_shape(size):
    return [
        (size, 0),
        (-size * 0.7,  size * 0.6),
        (-size * 0.4,  0),
        (-size * 0.7, -size * 0.6),
    ]

@dataclass
class ShipDef:
    name: str
    thrust: float
    turn_speed: float
    bullet_speed: float
    bullet_cooldown: int
    max_bullets: int
    size: int
    color: tuple = (220, 230, 240)
    shape: list[tuple] = field(default_factory=list)
    unlock_level: int = 0

    def __post_init__(self):
        if not self.shape:
            self.shape = default_shape(self.size)

SHIP_ROSTER: list[ShipDef] = [
    ShipDef(
        name="Vanguard",
        thrust=0.32, turn_speed=4.5,
        bullet_speed=7.0, bullet_cooldown=7, max_bullets=5,
        size=14,
        color=(220, 230, 240),
        unlock_level=0,
    ),
    ShipDef(
        name="Manta",
        thrust=0.42, turn_speed=5.5,
        bullet_speed=6.0, bullet_cooldown=5, max_bullets=4,
        size=12,
        color=(180, 220, 255),
        unlock_level=3,   # unlock after clearing level 3
        shape=[(12,0),(-4,10),(-10,4),(-10,-4),(-4,-10)],  # angular dart
    ),
    ShipDef(
        name="Brutus",
        thrust=0.22, turn_speed=3.0,
        bullet_speed=8.5, bullet_cooldown=10, max_bullets=3,
        size=20,
        color=(255, 210, 160),
        unlock_level=6,   # heavy tank
        shape=[(20,0),(0,12),(-14,10),(-14,-10),(0,-12)],
    ),
]
