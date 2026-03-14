# Imports
import pygame
from src.core.animations import sprites_func_items
from src.core.config import (width, height, grey_dark, grey_light, grey,
                            inventory_squares, squares_size, squares_padding)

# Initialize Pygame
pygame.init()


# * Class Inventory
class Inventory:
    # * __init__
    def __init__(self):
        # * Define the width and height of the inventory
        bar_width  = (squares_size + squares_padding) * inventory_squares + squares_padding
        bar_height = squares_size + squares_padding * 2
        bar_x = (width - bar_width) // 2 # * Inventory X axis
        bar_y = height - bar_height - 10 # * Inventory Y axis

        self.bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height) # * Inventory Skeleton
        self.items = [None] * inventory_squares # * List with the Items
        self.items_sprites = sprites_func_items(squares_size - 8, squares_size - 8) # * Items' Sprites

    # * Get the items to draw them later (Max 10 items)
    def put_images(self, item_name):
        for i in range(inventory_squares):
            if self.items[i] is None:
                self.items[i] = item_name
                return True
        return False  # ? Inventory Full

    # * Draw the 
    def draw(self, wn):
        # ? Border of the Inventory
        pygame.draw.rect(wn, grey_dark, self.bar_rect, border_radius=6)
        pygame.draw.rect(wn, grey, self.bar_rect, width=2, border_radius=6)

        for i in range(inventory_squares):
            slot_x = self.bar_rect.x + squares_padding + i * (squares_size + squares_padding)
            slot_y = self.bar_rect.y + squares_padding
            slot_rect = pygame.Rect(slot_x, slot_y, squares_size, squares_size)

            pygame.draw.rect(wn, grey_light, slot_rect, border_radius=3)
            pygame.draw.rect(wn, grey, slot_rect, width=2, border_radius=3)

            if self.items[i] is not None:
                img = self.items_sprites["item_sprites"].get(self.items[i])
                if img:
                    wn.blit(img, (slot_x + 4, slot_y + 4))
