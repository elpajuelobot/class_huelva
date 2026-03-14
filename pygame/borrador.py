import pygame
from src.core.animations import sprites_func_items

pygame.init()

SLOT_COUNT = 10
SLOT_SIZE = 50
SLOT_PADDING = 4

COLOR_BG     = (80,  80,  80)
COLOR_SLOT   = (198, 198, 198)
COLOR_BORDER = (85,  85,  85)


class Inventory:
    def __init__(self, screen_width=800, screen_height=600):
        bar_width  = (SLOT_SIZE + SLOT_PADDING) * SLOT_COUNT + SLOT_PADDING
        bar_height = SLOT_SIZE + SLOT_PADDING * 2
        bar_x = (screen_width - bar_width) // 2
        bar_y = screen_height - bar_height - 10

        self.bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        self.items = [None] * SLOT_COUNT
        self.items_sprites = sprites_func_items(SLOT_SIZE - 8, SLOT_SIZE - 8)

    def put_images(self, item_name):
        for i in range(SLOT_COUNT):
            if self.items[i] is None:
                self.items[i] = item_name
                return True
        return False  # Inventario lleno

    def draw(self, wn):
        pygame.draw.rect(wn, COLOR_BG, self.bar_rect, border_radius=6)
        pygame.draw.rect(wn, COLOR_BORDER, self.bar_rect, width=2, border_radius=6)

        for i in range(SLOT_COUNT):
            slot_x = self.bar_rect.x + SLOT_PADDING + i * (SLOT_SIZE + SLOT_PADDING)
            slot_y = self.bar_rect.y + SLOT_PADDING
            slot_rect = pygame.Rect(slot_x, slot_y, SLOT_SIZE, SLOT_SIZE)

            pygame.draw.rect(wn, COLOR_SLOT, slot_rect, border_radius=3)
            pygame.draw.rect(wn, COLOR_BORDER, slot_rect, width=2, border_radius=3)

            if self.items[i] is not None:
                img = self.items_sprites["item_sprites"].get(self.items[i])
                if img:
                    wn.blit(img, (slot_x + 4, slot_y + 4))
