from src.core.entities.sprites_class import Entities
from src.core.config import ISO_H, ISO_W, width_health, height_health
from src.core.animations import sprites_func_animals
import pygame
import json
import math

# * Animals' class
class Animals(Entities):
    def __init__(self, width, height, x, y, speed, frames, animal, visible=True, health=3):
        super().__init__(width=width, height=height, x=x, y=y)
        self.speed = speed
        self.frames = frames  # * Total number of animation frames in the sprite sheet
        self.animal = animal  # * Animal type key, used to look up sprites and JSON paths
        self.sprites_dic = {"animal_sprites": {}}  # * Populated by load_sprites()
        self.anim_count = 0
        self.health = health
        self.initial_health = health
        self.life = True  # * False when health reaches 0; triggers hide on next update
        self.tile_clmn = 0
        self.tile_row = 0
        self.depth = self.tile_clmn + self.tile_row
        self.cam_x = 0
        self.cam_y = 0
        self.world_x = self.x
        self.world_y = self.y
        self.visible = visible

    # * Load the animal's sprite sheet from the JSON path registry
    def load_sprites(self):
        with open("src\\data\\json\\animals_path.json", "r", encoding="utf-8") as data:
            self.animals_paths = json.load(data)
        sprites_func_animals(
            self.animals_paths[self.animal]["idle"]["down"],
            self.frames, "down", self.width, self.height,
            self.animal, "idle", self.sprites_dic
        )

    # * Reduce health; mark as dead when it hits zero
    def take_damage(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            self.life = False

    # * Update tile position, depth and camera each frame
    def update(self, cam_x, cam_y):
        if not self.life:
            self.visible = False  # * Hide the animal one frame after death
        if self.visible:
            self.base_y = self.world_y + self.height * 0.5
            self.tile_clmn = math.floor((self.world_x / (ISO_W / 2) + self.base_y / (ISO_H / 2)) / 2)
            self.tile_row  = math.floor((self.base_y / (ISO_H / 2) - self.world_x / (ISO_W / 2)) / 2)

            self.depth = self.tile_clmn + self.tile_row

            self.cam_x = cam_x
            self.cam_y = cam_y

    def draw(self, wn):
        if self.visible:
            if self.show_hitbox:
                pygame.draw.rect(wn, (255, 0, 0), self.hitbox, 4)
            wn_x = self.world_x - self.cam_x
            wn_y = self.world_y - self.cam_y
            frames = self.sprites_dic["animal_sprites"][self.animal]["idle"]["down"]
            # * Advance one animation frame every 5 game ticks
            current_frame = frames[self.anim_count // 5 % len(frames)]
            wn.blit(current_frame, (wn_x, wn_y))
            self.anim_count += 1

            # * Reset counter once a full animation cycle completes
            if self.anim_count >= len(frames) * 5:
                self.anim_count = 0

            self.hitbox.x = wn_x
            self.hitbox.y = wn_y

    # * Draw the animal's health bar directly above it in world space
    def barra_healt(self, wn, x, y):
        if self.health > 0:
            health_x = x - self.cam_x
            health_y = y - self.cam_y
            calculo_barra = int((self.health / self.initial_health) * width_health)
            rectangulo = pygame.Rect(health_x, health_y, calculo_barra, height_health)
            pygame.draw.rect(wn, (255, 0, 100), rectangulo)
        else:
            self.health = 0  # * Clamp to avoid negative health
