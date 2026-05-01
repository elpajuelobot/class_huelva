# Imports
import pygame
from src.core.animations import sprites_func_items, items_pool
from src.core.config import (
                            width, height, grey_dark, grey_light,
                            grey, grey_highlight, inventory_squares,
                            squares_size, squares_padding, red, inventory_font,
                            purple, white, width_health_invt, height_health_invt)
import json

# Initialize Pygame
pygame.init()


# * Class Inventory
class Inventory:
    # * __init__
    def __init__(self):
        # * Calculate the total pixel width of the hotbar (N slots + padding on each side)
        bar_width = (
            (squares_size + squares_padding)
            *
            inventory_squares + squares_padding
        )
        bar_height = squares_size + squares_padding * 2
        bar_x = (width - bar_width) // 2  # * Horizontally centred on screen
        bar_y = height - bar_height - 10  # * Pinned to the bottom of the window

        # * Background rectangle of the whole hotbar
        self.bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)

        # * Each slot stores the item name, stack count, rendered count label, durability and current health
        self.items = (
            {i: {"name": None, "count": 0, "text_count": None, "durability": 0, "health": 0}
                for i in range(inventory_squares)}
        )

        # * Pre-load all item sprites at inventory slot size
        self.items_sprites = sprites_func_items(
                            item_width=squares_size - 8,
                            item_height=squares_size - 8
        )
        self.selected_item = None  # * Index of the currently highlighted slot (None = nothing selected)
        self.actual_item   = None  # * Name of the item in the selected slot (used by combat and interaction logic)

    # * Try to add an item to the inventory; returns True on success, False if the inventory is full
    def put_images(self, item_name, item_durability, item_health):
        with open("src\\data\\json\\items_not_duplicated.json", "r", encoding="utf-8") as data:
            not_duplicated = json.load(data)

        # * If the item already exists in a slot, stack it (unless it's in the non-stackable list)
        for i in range(inventory_squares):
            if self.items[i]["name"] == item_name:
                if self.items[i]["name"] not in not_duplicated["not_duplicated"]:
                    # * Stackable: increment count and update the rendered label
                    self.items[i]["count"] += 1
                    self.items[i]["text_count"] = (
                        inventory_font.render(
                            f"x{self.items[i]["count"]}", True, white
                        )
                    )
                    return True
                else:
                    # * Non-stackable: find an empty slot for the duplicate
                    for duplicated in range(inventory_squares):
                        if self.items[duplicated]["name"] is None:
                            self.items[duplicated]["name"] = item_name
                            self.items[duplicated]["count"] = 1
                            self.items[duplicated]["durability"] = item_durability
                            self.items[duplicated]["health"] = item_health
                            return True

        # * Item not already in inventory — place it in the first empty slot
        for i in range(inventory_squares):
            if self.items[i]["name"] is None:
                self.items[i]["name"] = item_name
                self.items[i]["count"] = 1
                self.items[i]["durability"] = item_durability
                self.items[i]["health"] = item_health
                return True

        return False  # * Inventory full — item not added

    # * Handle keyboard input for slot selection, item use and dropping
    def update(self, event, items, player_x, player_y):
        # * Auto-clear a slot if its item has been fully consumed
        if self.selected_item is not None:
            if self.items[self.selected_item]["health"] <= 0:
                self.items[self.selected_item]["health"] = 0
                self.items[self.selected_item]["durability"] = 0
                self.items[self.selected_item]["name"] = None
                self.items[self.selected_item]["count"] = 0
                self.items[self.selected_item]["text_count"] = None
                self.selected_item = None
                self.actual_item = None

        if event.type == pygame.KEYDOWN:
            # * Number keys 1–0 select the corresponding hotbar slot
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
                    self.actual_item = self.items[square]["name"]
                else:
                    # * Pressing a key for an empty slot deselects the current item
                    self.selected_item = None
                    self.actual_item = None

            # * Q drops one copy of the selected item into the world slightly to the right of the player
            if event.key == pygame.K_q and self.selected_item is not None:
                if self.items[self.selected_item]["name"] is not None:
                    items_pool(
                        pool=items,
                        name=self.items[self.selected_item]["name"],
                        x=player_x + 100,
                        y=player_y,
                        health=self.items[self.selected_item]["health"],
                        durability=self.items[self.selected_item]["durability"]
                    )

                    self.items[self.selected_item]["count"] -= 1
                    self.items[self.selected_item]["text_count"] = (
                        inventory_font.render(
                            f"x{self.items[self.selected_item]["count"]}",
                            True, white
                        )
                    )
                    # * Clear the slot when the last copy is dropped
                    if self.items[self.selected_item]["count"] == 0:
                        self.items[self.selected_item]["name"] = None
                        self.items[self.selected_item]["text_count"] = None
                        self.selected_item = None
                        self.actual_item = None

                    # * Hide the "x1" label — a single item doesn't need a count badge
                    elif self.items[self.selected_item]["count"] == 1:
                        self.items[self.selected_item]["text_count"] = None

    # * Draw the hotbar and all its slots each frame
    def draw(self, wn):
        # * Hotbar background and border
        pygame.draw.rect(wn, grey_dark, self.bar_rect, border_radius=6)
        pygame.draw.rect(wn, grey, self.bar_rect, width=2, border_radius=6)

        for i in range(inventory_squares):
            slot_x = (
                self.bar_rect.x + squares_padding + i
                *
                (squares_size + squares_padding)
            )
            slot_y = self.bar_rect.y + squares_padding
            slot_rect = pygame.Rect(slot_x, slot_y, squares_size, squares_size)

            # * Highlight the selected slot with a brighter background
            if self.selected_item == i:
                pygame.draw.rect(wn, grey_highlight, slot_rect, border_radius=3)
            else:
                pygame.draw.rect(wn, grey_light, slot_rect, border_radius=3)
            pygame.draw.rect(wn, grey, slot_rect, width=2, border_radius=3)

            if self.items[i]["name"] is not None:
                img = (
                    self.items_sprites["item_sprites"].get(
                        self.items[i]["name"]
                    )
                )
                if img:
                    wn.blit(img, (slot_x + 4, slot_y + 4))  # * 4px inset padding

                    # * Stack count badge (purple circle + "xN" label) — only shown when count > 1
                    if self.items[i]["text_count"] is not None:
                        axis_x = (
                            slot_x + squares_size
                            -
                            self.items[i]["text_count"].get_width() - 3
                        )
                        axis_y = (
                            slot_y + squares_size
                            -
                            self.items[i]["text_count"].get_height() - 3
                        )
                        pygame.draw.circle(
                            wn, purple,
                            (axis_x + 7, axis_y + 8), 9  # * Circle centred behind the label
                        )
                        wn.blit(self.items[i]["text_count"], (axis_x, axis_y))

                    # * Durability bar along the bottom of the slot
                    health_x = slot_x + 4
                    health_y = slot_y + squares_size - height_health_invt - 4
                    self.barra_healt(wn, health_x, health_y, i)

    # * Consume one use of the selected item (called by the attack system on sword hits)
    def use_item(self):
        self.items[self.selected_item]["health"] -= 1

    # * Draw the durability bar for slot `index` — only shown when the item has more than 1 max use and is damaged
    def barra_healt(self, wn, x, y, index):
        item = self.items[index]
        if item["durability"] > 1:
            if item["health"] > 0:
                if item["health"] < item["durability"]:
                    calculo_barra = int(
                        (
                            item["health"] / item["durability"]
                        ) * width_health_invt
                    )
                    rectangulo = pygame.Rect(x, y, calculo_barra, height_health_invt)
                    pygame.draw.rect(wn, (255, 0, 100), rectangulo)
            else:
                item["health"] = 0  # * Clamp to avoid negative durability
