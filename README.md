# ASTERAX

A fast-paced arcade space shooter and roguelite built with **Python** and **Pygame**, inspired by classic *Asteroids*. Pilot unlockable ships, blast through escalating asteroid waves, earn credits, and customize your build in the between-wave upgrade shop.

---

## Features

- **3 Playable Ships with Meta-Progression Unlocks**:
  - **Vanguard** *(Unlocked by default)* — Balanced cruiser with steady handling and firepower.
  - **Manta** *(Unlocks after clearing Level 4)* — High-speed, agile dart with rapid fire.
  - **Brutus** *(Unlocks after clearing Level 7)* — Heavy armored hull with high-velocity cannons.
- **Between-Wave Upgrade Shop**:
  - **Engine** *(3 Tiers)* — Increases thrust and top speed (`+12%` thrust, `+10%` max speed per tier).
  - **Gyro Stabiliser** *(3 Tiers)* — Increases turn rate (`+10%` per tier).
  - **Reinforced Hull** *(2 Tiers)* — Grants an extra life/respawn (`+1` life per tier).
  - **Weapon Mod** *(3 Tiers)* — Reduces firing cooldown for faster fire rate.
  - **Spread Shot** *(2 Tiers)* — Fires `+1` additional bullet per volley in a spread pattern.
  - **Aegis Shield** *(2 Tiers)* — Absorbs `1` free hit per level per tier before losing lives.
- **Endless Wave Scaling**:
  - 8 hand-tuned waves followed by endless scaling with increasing asteroid counts and speeds.

---

## Controls

| Screen | Input | Action |
| :--- | :--- | :--- |
| **Ship Select** | `←` / `→` or `A` / `D` | Cycle unlocked ships |
| | `ENTER` or `SPACE` | Confirm ship & launch |
| | `ESC` | Quit game |
| **Gameplay** | `↑` or `W` | Thrust forward |
| | `←` / `→` or `A` / `D` | Rotate ship left / right |
| | `SPACE` | Fire weapons |
| **Upgrade Shop** | `↑` / `↓` or `W` / `S` | Navigate upgrades / Continue |
| | `ENTER` or `SPACE` | Purchase upgrade / Continue |
| | `ESC` | Skip shop & start next level |
| **Game Over** | `ENTER` | Start a new run (keeps ship unlocks) |
| | `ESC` | Quit game |

---

## Getting Started

### Prerequisites
- Python `3.10+`
- `pygame` (`2.x`)

### Installation & Running

```bash
# Clone the repository
git clone https://github.com/opyner-gh/asterax-clone.git
cd asterax-clone

# Create and activate a virtual environment (optional)
python -m venv venv
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

# Install Pygame
pip install pygame

# Launch the game
python main.py
```

---

## Project Structure

| File | Description |
| :--- | :--- |
| `main.py` | Application entry point |
| `game.py` | Core game loop, state machine (`select`, `play`, `shop`, `over`), HUD, and collision handling |
| `config.py` | Display settings, color palette, and asteroid size/score/credit tables |
| `entity.py` | `GameObject` base class for movement, screen wrapping, and circle collisions |
| `player.py` | `Player` physics, controls, shield rendering, and respawn invulnerability |
| `asteroid.py` | Procedural rock polygon generation, rotation, and splitting logic |
| `bullet.py` | `Bullet` projectile lifetime and movement |
| `ships.py` | `ShipDef` dataclass and `SHIP_ROSTER` definitions |
| `upgrades.py` | `Upgrade` definitions, exponential cost scaling, and stat modifiers |
| `levels.py` | `LevelDef` wave definitions and endless scaling |
| `ship_select.py` | Ship selection screen and stat bar comparison UI |
| `shop.py` | Between-wave upgrade shop UI |
