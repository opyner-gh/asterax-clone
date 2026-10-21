# mist.py
import math
import random
import pygame
from config import (get_screen_size, MIST_HUE_SPEED, MIST_DRIFT_SPEED, MIST_WAVE_SPEED,
                    MIST_WAVE_AMP, MIST_PULSE_HZ, MIST_GLOW_MIN, MIST_GLOW_MAX,
                    MIST_DENSITY, MIST_SATURATION, MIST_GRID_STEP, MIST_GRID_ALPHA)

FOG_RES   = 12     # px per noise sample (fog is generated small, then scaled up)
FOG_OVER  = 1.5    # fog layers are this much bigger than the screen so they can drift
STRIP_H   = 6      # row height for the wavy horizontal warp
RAINBOW_CELL = 40  # px per rainbow-light sample


def _smooth(t):
    return t * t * (3 - 2 * t)


def _value_noise(lw, lh, px, py, rng):
    """lw×lh grid of smooth noise in 0..1 with px×py lattice cells."""
    lat = [[rng.random() for _ in range(px + 1)] for _ in range(py + 1)]
    out = []
    for y in range(lh):
        gy = y / lh * py
        iy, fy = int(gy), _smooth(gy - int(gy))
        row = []
        for x in range(lw):
            gx = x / lw * px
            ix, fx = int(gx), _smooth(gx - int(gx))
            a = lat[iy][ix]     + (lat[iy][ix + 1]     - lat[iy][ix])     * fx
            b = lat[iy + 1][ix] + (lat[iy + 1][ix + 1] - lat[iy + 1][ix]) * fx
            row.append(a + (b - a) * fy)
        out.append(row)
    return out


def _fog_layer(w, h, seed):
    """Wispy greyscale fog texture: fractal noise with clear gaps between the clouds."""
    rng = random.Random(seed)
    lw, lh = w // FOG_RES, h // FOG_RES
    total = [[0.0] * lw for _ in range(lh)]
    amp, norm = 1.0, 0.0
    for octave in range(5):
        n = _value_noise(lw, lh, 3 * 2 ** octave, 2 * 2 ** octave, rng)
        for y in range(lh):
            for x in range(lw):
                total[y][x] += n[y][x] * amp
        norm += amp
        amp *= 0.5

    small = pygame.Surface((lw, lh))
    for y in range(lh):
        for x in range(lw):
            d = max(0.0, (total[y][x] / norm - 0.42) / 0.58) ** 1.4
            v = int(min(1.0, d * 1.8) * MIST_DENSITY)
            small.set_at((x, y), (v, v, v))
    return pygame.transform.smoothscale(small, (w, h))


class Mist:
    """Rainbow-lit drifting fog with a wavy grid — shown while one asteroid remains."""

    def __init__(self):
        w, h = get_screen_size()
        self.margin = int(MIST_WAVE_AMP * 1.4) + 2   # covers the two summed ripples in draw()
        self.fog_w, self.fog_h = w + 2 * self.margin, h
        big = (int(self.fog_w * FOG_OVER), int(h * FOG_OVER))
        self.layers = [_fog_layer(*big, seed) for seed in (11, 23, 37)]
        # (x speed, y speed, phase) for each layer's lissajous drift
        self.paths = [(0.13, 0.21, 0.0), (0.19, 0.11, 2.1), (0.09, 0.17, 4.3)]

        self.density = pygame.Surface((self.fog_w, self.fog_h))
        self.light   = pygame.Surface((self.fog_w, self.fog_h))
        self.rainbow = pygame.Surface((self.fog_w // RAINBOW_CELL + 2, h // RAINBOW_CELL + 2))
        self.grid    = pygame.Surface((w, h), pygame.SRCALPHA)

    def draw(self, screen):
        t  = pygame.time.get_ticks() / 1000
        dt = t * MIST_DRIFT_SPEED
        wt = t * MIST_WAVE_SPEED
        w, h = get_screen_size()

        # 1. stack the drifting fog layers into one density map
        self.density.fill((0, 0, 0))
        for layer, (sx, sy, ph) in zip(self.layers, self.paths):
            room_x = layer.get_width()  - self.fog_w
            room_y = layer.get_height() - self.fog_h
            ox = (0.5 + 0.5 * math.sin(dt * sx + ph)) * room_x
            oy = (0.5 + 0.5 * math.sin(dt * sy + ph * 1.7)) * room_y
            self.density.blit(layer, (0, 0), (ox, oy, self.fog_w, self.fog_h),
                              special_flags=pygame.BLEND_RGB_ADD)

        # 2. pulse the glow
        pulse = 0.5 + 0.5 * math.sin(t * MIST_PULSE_HZ * math.tau)
        g = int(255 * (MIST_GLOW_MIN + (MIST_GLOW_MAX - MIST_GLOW_MIN) * pulse))
        self.density.fill((g, g, g), special_flags=pygame.BLEND_RGB_MULT)

        # 3. light the fog with a soft, shifting rainbow
        hue0 = t * MIST_HUE_SPEED
        col = pygame.Color(0)
        rw, rh = self.rainbow.get_size()
        for y in range(rh):
            for x in range(rw):
                hue = hue0 + x * 9 + y * 6 + 40 * math.sin(x * 0.25 + y * 0.2 + wt * 0.5)
                col.hsva = (hue % 360, MIST_SATURATION, 100, 100)
                self.rainbow.set_at((x, y), col)
        pygame.transform.smoothscale(self.rainbow, (self.fog_w, self.fog_h), self.light)
        self.light.blit(self.density, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

        # 4. add it over the starfield in rippling horizontal strips
        for y in range(0, h, STRIP_H):
            ox = MIST_WAVE_AMP * math.sin(y / 140 + wt) + 0.4 * MIST_WAVE_AMP * math.sin(y / 53 - wt * 1.7)
            screen.blit(self.light, (ox - self.margin, y), (0, y, self.fog_w, STRIP_H),
                        special_flags=pygame.BLEND_RGB_ADD)

        # 5. faint wavy "technical" grid
        self.grid.fill((0, 0, 0, 0))
        line_col = (255, 255, 255, MIST_GRID_ALPHA)
        for gx in range(0, w + MIST_GRID_STEP, MIST_GRID_STEP):
            pts = [(gx + 10 * math.sin(gy / 90 + wt * 1.5), gy) for gy in range(0, h + 24, 24)]
            pygame.draw.lines(self.grid, line_col, False, pts)
        for gy in range(0, h + MIST_GRID_STEP, MIST_GRID_STEP):
            pts = [(gx, gy + 10 * math.sin(gx / 110 - wt * 1.2)) for gx in range(0, w + 24, 24)]
            pygame.draw.lines(self.grid, line_col, False, pts)
        screen.blit(self.grid, (0, 0))
