# config.py
SCREEN_W, SCREEN_H = 800, 600
FPS = 60

# Player
PLAYER_SIZE = 16
PLAYER_THRUST = 0.35
PLAYER_TURN_SPEED = 4.0          # degrees per frame
PLAYER_FRICTION = 0.99          # 1.0 = no friction (classic); <1.0 = drag
PLAYER_INVULN_FRAMES = 120      # brief invulnerability after respawn

# Bullets
BULLET_SPEED = 7.0
BULLET_LIFE = 55               # frames before despawn
BULLET_COOLDOWN = 8            # frames between shots
BULLET_MAX_ACTIVE = 5          # classic limit

# Asteroids
ASTEROID_SIZES = [(50, "big"), (30, "med"), (15, "small")]  # radius, key
ASTEROID_BASE_SPEED = (1.0, 3.0)  # random range
SPLIT_CHANCE = 1.0             # probability a hit asteroid splits

# Spawning
INITIAL_ASTEROID_COUNT = 4
ASTEROID_RESPAWN_FRAMES = 90   # pause between new waves

# Collision
COLLISION_SLOP = 0.0           # extra pixel margin (tune to taste)
