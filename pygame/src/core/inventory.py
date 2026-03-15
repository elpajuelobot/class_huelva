# Imports
import pygame
from src.core.animations import sprites_func_items
from src.core.config import (width, height, grey_dark, grey_light, grey, grey_highlight,
                            inventory_squares, squares_size, squares_padding, red, inventory_font,
                            black, width_item, height_item)

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
        self.items = {i: {"name": None, "count": 0, "text_count": None} for i in range(inventory_squares)} # * Dict with the Items
        self.items_sprites = sprites_func_items(squares_size - 8, squares_size - 8) # * Items' Sprites
        self.selected_item = None

    # * Get the items to draw them later (Max 10 items)
    def put_images(self, item_name):
        for i in range(inventory_squares):
            if self.items[i]["name"] == item_name:
                self.items[i]["count"] += 1
                self.items[i]["text_count"] = inventory_font.render(f"x{self.items[i]["count"]}", True, black)
                print(f"{self.items[i]['name']}\n{self.items[i]['count']}")
                return True
        for i in range(inventory_squares):
            if self.items[i]["name"] is None:
                self.items[i]["name"] = item_name
                self.items[i]["count"] = 1
                return True
        return False  # ? Inventory Full

    # * Update the inventory
    def update(self, event, items, player_x, player_y, items_creator):
        if event.type == pygame.KEYDOWN:
            key_map = {
                pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2,
                pygame.K_4: 3, pygame.K_5: 4, pygame.K_6: 5,
                pygame.K_7: 6, pygame.K_8: 7, pygame.K_9: 8,
                pygame.K_0: 9
            }

            if event.key in key_map:
                square = key_map[event.key]
                if self.items[square]["name"] is not None:
                    self.selected_item = square
                else:
                    self.selected_item = None

            if event.key == pygame.K_q and self.selected_item is not None:
                if self.items[self.selected_item]["name"] is not None:
                    items.append(items_creator(
                        x_item=player_x + 100,
                        y_item=player_y,
                        width_item=width_item,
                        height_item=height_item,
                        name_item=self.items[self.selected_item]["name"]
                    ))

                    self.items[self.selected_item]["count"] -= 1
                    self.items[self.selected_item]["text_count"] = inventory_font.render(f"x{self.items[self.selected_item]["count"]}", True, black)
                    if self.items[self.selected_item]["count"] == 0:
                        self.items[self.selected_item]["name"] = None
                        self.items[self.selected_item]["text_count"] = None
                        self.selected_item = None

    # * Draw the Inventory
    def draw(self, wn):
        # ? Border of the Inventory
        pygame.draw.rect(wn, grey_dark, self.bar_rect, border_radius=6)
        pygame.draw.rect(wn, grey, self.bar_rect, width=2, border_radius=6)

        for i in range(inventory_squares):
            slot_x = self.bar_rect.x + squares_padding + i * (squares_size + squares_padding)
            slot_y = self.bar_rect.y + squares_padding
            slot_rect = pygame.Rect(slot_x, slot_y, squares_size, squares_size)

            if self.selected_item == i:
                pygame.draw.rect(wn, grey_highlight, slot_rect, border_radius=3)
                pygame.draw.rect(wn, red, slot_rect, width=5, border_radius=3)
            else:
                pygame.draw.rect(wn, grey_light, slot_rect, border_radius=3)
            pygame.draw.rect(wn, grey, slot_rect, width=2, border_radius=3)

            if self.items[i]["name"] is not None:
                img = self.items_sprites["item_sprites"].get(self.items[i]["name"])
                if img:
                    wn.blit(img, (slot_x + 4, slot_y + 4))
                    if self.items[i]["text_count"] is not None:
                        axis_x = slot_x + squares_size - self.items[i]["text_count"].get_width() - 3
                        axis_y = slot_y + squares_size - self.items[i]["text_count"].get_height() - 3
                        wn.blit(self.items[i]["text_count"], (axis_x, axis_y))
