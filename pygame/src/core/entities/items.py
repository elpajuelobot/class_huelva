import pygame
from src.core.entities.sprites_class import Entities
import math
from src.core.settings.config import lifetime, ISO_H, ISO_W
from src.core.system.animations.animations import sprites_func_items

# * Items' class
class Items(Entities):
    # * __init__
    def __init__(self, *groups, width, height, x, y, name_item, durability, item_power=None):
        super().__init__(*groups, width=width, height=height, x=x, y=y)
        self.sprites = sprites_func_items(self.width, self.height)
        self.name = name_item
        self.item = self.sprites["item_sprites"][self.name]  # * Item sprite image
        self.world_x = x
        self.world_y = y
        self.spawn_time = 0  # * Tick when this item became visible (used for lifetime expiry)
        self.lifetime = lifetime # * 60*10^4ms (1 min) — item disappears after this
        self.pickup_delay = 0  # * Tick before which the player cannot pick up this item
        self.power = item_power  # * Optional stat bonus (reserved for future use)
        self.durability = durability  # * Max uses before the item breaks
        self.health = durability  # * Current uses remaining
        self.tile_clmn = 0
        self.tile_row = 0
        self.depth = self.tile_clmn + self.tile_row  # * Draw order
        self.health_bar = False  # * Items don't show a health bar in the world
        self.cam_x = 0
        self.cam_y = 0

    # * Recalculate tile position and depth each frame (items can be dropped anywhere)
    def update(self, cam_x, cam_y):
        if self.visible:
            self.base_y = self.world_y + self.height * 0.5
            self.tile_clmn = math.floor((self.world_x / (ISO_W / 2) + self.base_y / (ISO_H / 2)) / 2)
            self.tile_row  = math.floor((self.base_y / (ISO_H / 2) - self.world_x / (ISO_W / 2)) / 2)

            self.depth = self.tile_clmn + self.tile_row

            self.cam_x = cam_x
            self.cam_y = cam_y

    # * Draw the Items
    def draw(self, wn):
        if self.visible:
            if self.show_hitbox:
                pygame.draw.rect(wn, (255, 0, 0), self.hitbox, 4)
            wn_x = self.world_x - self.cam_x
            wn_y = self.world_y - self.cam_y
            wn.blit(self.item, (wn_x, wn_y))
            # * Keep hitbox in sync with screen position for pickup collision detection
            self.hitbox.x = wn_x
            self.hitbox.y = wn_y
