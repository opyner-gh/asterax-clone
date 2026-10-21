# upgrades.py
from dataclasses import dataclass

@dataclass
class Upgrade:
    key: str
    name: str
    desc: str
    base_cost: int
    max_level: int          # how many times you can buy it
    cost_scale: float = 1.85 # each purchase multiplies cost

# ── the catalogue ─────────────────────────────────────────────
UPGRADES: list[Upgrade] = [
    Upgrade("engine",   "Engine",       "+Thrust & top speed",       150, 3),
    Upgrade("gym",      "Gyro Stabiliser","+Turn rate",              120, 3),
    Upgrade("hull",     "Reinforced Hull","Extra hit (respawn)",     400, 2),
    Upgrade("weapon",   "Weapon Mod",   "Faster fire rate",          220, 3),
    Upgrade("multishot","Spread Shot",  "+1 bullet per shot",        500, 2),
    Upgrade("shield",   "Aegis Shield", "1 free hit per level",      450, 2),
]

# ── helper ────────────────────────────────────────────────────
def cost_for(upg: Upgrade, current_level: int) -> int:
    return int(upg.base_cost * (upg.cost_scale ** current_level))

def apply_upgrades(ship, owned: dict[str, int]):
    """Return a dict of effective stats after upgrades applied."""
    s = {
        "thrust":           ship.thrust,
        "max_speed":        ship.max_speed,
        "turn_speed":       ship.turn_speed,
        "bullet_speed":     ship.bullet_speed,
        "bullet_cooldown":  ship.bullet_cooldown,
        "max_bullets":      ship.max_bullets,
        "bullets_per_shot": 1,
        "extra_lives":      0,
        "shield_charges":   0,
    }
    if "engine" in owned:
        s["thrust"]       *= (1 + 0.12 * owned["engine"])
        s["max_speed"]    *= (1 + 0.10 * owned["engine"])
    if "gym" in owned:
        s["turn_speed"]   *= (1 + 0.10 * owned["gym"])
    if "hull" in owned:
        s["extra_lives"]  = owned["hull"]
    if "weapon" in owned:
        s["bullet_cooldown"] = max(2, s["bullet_cooldown"] - owned["weapon"])
    if "multishot" in owned:
        s["bullets_per_shot"] += owned["multishot"]
        s["max_bullets"]      += owned["multishot"] * 2
    if "shield" in owned:
        s["shield_charges"] = owned["shield"]
    return s
