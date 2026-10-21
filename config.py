# config.py
def get_screen_size():
    return (1280, 720)

def get_fps():
    return 60

def get_max_bullet():
    return 30

BULLET_LIFE = 55

def get_bullet_life():
    return BULLET_LIFE

def get_col_bg():           return ( 12,  14,  22)   # 0c0e16
def get_col_star():         return ( 80,  85, 105)   # 505569
def get_col_ship():         return (224, 230, 240)   # e0e6f0
def get_col_ship_outline(): return (144, 154, 175)   # 909aaf
def get_col_rock():         return (160, 155, 150)   # a09b96
def get_col_rock_outline(): return (100,  95,  90)   # 645f5a
def get_col_bullet():       return (255, 236, 120)   # ffec78
def get_col_thrust():       return (255, 150,  30)   # ff961e
def get_col_ui_bg():        return ( 28,  30,  38)   # 1c1e26
def get_col_ui_border():    return ( 90, 101, 120)   # 5a6578
def get_col_ui_text():      return (210, 213, 225)   # d2d5e1
def get_col_ui_highlight(): return (255, 204,  60)   # ffcc3c
def get_col_ui_purchased(): return (100, 200, 124)   # 64c87c
def get_col_danger():       return (220,  80,  70)   # dc5046
def get_col_shield():       return ( 80, 160, 255)   # 50a0ff

# ── last-asteroid rainbow mist ─────────────────────────────────
MIST_HUE_SPEED   = 60     # degrees of rainbow shift per second
MIST_DRIFT_SPEED = 1.0    # how fast the fog layers drift
MIST_WAVE_SPEED  = 1.6    # how fast the ripples travel
MIST_WAVE_AMP    = 18     # ripple strength (px of sideways warp)
MIST_PULSE_HZ    = 2.0    # glow pulses per second
MIST_GLOW_MIN    = 0.55   # fog glow at pulse low (0-1)
MIST_GLOW_MAX    = 1.0    # fog glow at pulse peak (0-1)
MIST_DENSITY     = 95     # peak brightness of each fog layer (0-255)
MIST_SATURATION  = 55     # rainbow colour strength (0-100, lower = paler)
MIST_GRID_STEP   = 64     # px between overlay grid lines
MIST_GRID_ALPHA  = 22     # overlay grid opacity (0-255)

# (radius, size_key, points)
ROCK_SIZES = [
    (30, "big",   100),
    (18, "med",    50),
    (10, "small",  25),
]

ROCK_RADIUS = {k: r for r, k, _ in ROCK_SIZES}
ROCK_POINTS = {k: p for _, k, p in ROCK_SIZES}
ROCK_CREDITS = {
    "big":   10,
    "med":    5,
    "small":  3,
}
ROCK_NEXT_SIZE = {
    ROCK_SIZES[i][1]: (ROCK_SIZES[i + 1][1] if i + 1 < len(ROCK_SIZES) else None)
    for i in range(len(ROCK_SIZES))
}
