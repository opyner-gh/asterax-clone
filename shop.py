# shop.py
import pygame
from upgrades import UPGRADES, cost_for
from config import (get_screen_size, get_col_bg, get_col_ui_bg, get_col_ui_border,
                    get_col_ui_text, get_col_ui_highlight, get_col_ui_purchased, get_col_danger)

class Shop:
    def __init__(self, credits: int, owned: dict[str, int], level_cleared: int):
        self.credits = credits
        self.owned = dict(owned)          # copy so we don't mutate the game's dict
        self.level_cleared = level_cleared
        self.cursor = 0
        self.done = False
        self.font = pygame.font.SysFont("monospace", 17)
        self.font_big = pygame.font.SysFont("monospace", 22, bold=True)

    def handle(self, events):
        row_count = len(UPGRADES) + 1
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self._continue()
                elif e.key == pygame.K_UP or e.key == pygame.K_w:
                    self.cursor = (self.cursor - 1) % row_count
                elif e.key == pygame.K_DOWN or e.key == pygame.K_s:
                    self.cursor = (self.cursor + 1) % row_count
                elif e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if self.cursor == len(UPGRADES):
                        self._continue()
                    else:
                        self._buy()
        return None

    def _buy(self):
        upg = UPGRADES[self.cursor]
        cur = self.owned.get(upg.key, 0)
        if cur >= upg.max_level:
            return
        cost = cost_for(upg, cur)
        if self.credits >= cost:
            self.credits -= cost
            self.owned[upg.key] = cur + 1

    def _continue(self):
        self.done = True

    def draw(self, screen):
        screen.fill(get_col_bg())

        # header
        hdr = self.font_big.render(f"LEVEL {self.level_cleared + 1} CLEAR — UPGRADE SHOP", True, get_col_ui_highlight())
        screen.blit(hdr, (get_screen_size()[0]//2 - hdr.get_width()//2, 30))
        cred = self.font_big.render(f"Credits: {self.credits}", True, get_col_ui_text())
        screen.blit(cred, (get_screen_size()[0] - cred.get_width() - 20, 30))

        # rows
        y = 90
        row_h = 52
        for i, upg in enumerate(UPGRADES):
            cur = self.owned.get(upg.key, 0)
            maxed = cur >= upg.max_level
            cost = 0 if maxed else cost_for(upg, cur)
            can_buy = (not maxed) and self.credits >= cost
            selected = (i == self.cursor)

            # row bg
            bg = get_col_ui_bg() if not selected else (45, 50, 65)
            pygame.draw.rect(screen, bg, (60, y, get_screen_size()[0] - 120, row_h), border_radius=4)
            if selected:
                pygame.draw.rect(screen, get_col_ui_highlight(), (60, y, get_screen_size()[0] - 120, row_h), 2, border_radius=4)

            # name + desc
            name_color = get_col_ui_purchased() if maxed else get_col_ui_text()
            screen.blit(self.font.render(f"{upg.name}  Lv {cur}/{upg.max_level}", True, name_color), (80, y + 6))
            screen.blit(self.font.render(upg.desc, True, (130,130,140)), (80, y + 28))

            # cost / status (right-aligned)
            if maxed:
                tag = "MAXED"
                screen.blit(self.font.render(tag, True, get_col_ui_purchased()),
                            (get_screen_size()[0] - 180 - self.font.render(tag, True, get_col_ui_purchased()).get_width(), y + 16))
            else:
                tag = f"{cost} cr"
                tc = get_col_ui_highlight() if can_buy else get_col_danger()
                screen.blit(self.font.render(tag, True, tc),
                            (get_screen_size()[0] - 180 - self.font.render(tag, True, tc).get_width(), y + 16))

            y += row_h + 6

        # "continue" row
        cont_selected = (self.cursor == len(UPGRADES))
        bg = (45, 50, 65) if cont_selected else get_col_ui_bg()
        pygame.draw.rect(screen, bg, (60, y, get_screen_size()[0] - 120, row_h), border_radius=4)
        if cont_selected:
            pygame.draw.rect(screen, get_col_ui_highlight(), (60, y, get_screen_size()[0] - 120, row_h), 2, border_radius=4)
        screen.blit(self.font.render("CONTINUE TO NEXT LEVEL →", True, get_col_ui_text()), (80, y + 16))

        # footer
        hint = self.font.render("↑↓ navigate    ENTER buy / confirm    ESC skip", True, (100,100,110))
        screen.blit(hint, (get_screen_size()[0]//2 - hint.get_width()//2, get_screen_size()[1] - 30))

    @property
    def final_owned(self) -> dict[str, int]:
        return self.owned

    @property
    def remaining_credits(self) -> int:
        return self.credits
