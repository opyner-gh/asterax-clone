# levels.py
from dataclasses import dataclass

@dataclass
class LevelDef:
    index: int
    big_rocks: int
    rock_speed_min: float
    rock_speed_max: float
    rock_split_chance: float = 1.0
    # future: enemy_count, special_rock, time_limit, etc.

LEVELS: list[LevelDef] = [
    LevelDef(0, big_rocks=4, rock_speed_min=0.8, rock_speed_max=2.0),
    LevelDef(1, big_rocks=5, rock_speed_min=1.0, rock_speed_max=2.5),
    LevelDef(2, big_rocks=5, rock_speed_min=1.2, rock_speed_max=2.8),
    LevelDef(3, big_rocks=6, rock_speed_min=1.3, rock_speed_max=3.2),
    LevelDef(4, big_rocks=7, rock_speed_min=1.5, rock_speed_max=3.5),
    LevelDef(5, big_rocks=7, rock_speed_min=1.6, rock_speed_max=3.8),
    LevelDef(6, big_rocks=8, rock_speed_min=1.8, rock_speed_max=4.2),
    LevelDef(7, big_rocks=9, rock_speed_min=2.0, rock_speed_max=4.5),
]
# Loop back with increasing speed past level 7:
def level_for(index: int) -> LevelDef:
    if index < len(LEVELS):
        return LEVELS[index]
    # endless: keep scaling
    base = LEVELS[-1]
    extra = index - len(LEVELS) + 1
    return LevelDef(
        index=index,
        big_rocks=min(base.big_rocks + extra, 14),
        rock_speed_min=base.rock_speed_min + extra * 0.2,
        rock_speed_max=base.rock_speed_max + extra * 0.3,
    )