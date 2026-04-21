# Imports
import pygame
from src.core.animations import (
    sprites_func_player,
    sprites_func_shot,
    sprites_func_items,
    sprites_func_animals
)
from src.core.config import (
    shot_width,
    shot_height,
    shot_cooldown,
    lifetime,
    width_health,
    height_health,
    font,
    white
)
from src.core.inventory import Inventory
import json


class Entities(pygame.sprite.Sprite):
    def __init__(self, *groups, width, height, x, y):
        super().__init__(*groups)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(
            self.x, self.y,
            self.width, self.height
        )
        self.visible = True


class Player(Entities):
    def __init__(self, *groups, width, height, x, y, speed_player, sprites_player, wn_width, wn_height, inventory):
        super().__init__(*groups, width=width, height=height, x=x, y=y)
        self.sprites = sprites_func_player(self.width, self.height)
        self.speed = speed_player  # * Player's speed
        self.player_state = "right"  # * Player's state
        self.sprites_dict = self.sprites[sprites_player]  # * Player's sprites
        self.anim_count = 0  # * Counter for the animations' frames
        self.is_move = False  # * Can't move in the begining
        self.show_hitbox = False  # * Don't show the hitbox
        self.is_shot = False  # * If the player throwing a fire ball?
        self.projectiles = []  # * List with all the projectiles
        self.can_create_shot = False  # * when player can create a projectiles
        self.last_shot_time = 0  # * The time of the last fire ball
        self.shot_count_down = shot_cooldown  # * Delay for the fire balls
        self.inventory = inventory  # * Create the inventory
        self.world_x = x
        self.world_y = y
        # ? Update the actual column and row
        self.tile_clmn = 0
        self.tile_row = 0
        self.depth = self.tile_clmn + self.tile_row
        self.wn_width = wn_width
        self.wn_height = wn_height
        self.name = "Scot"

    # * Update de inventory
    def update_inventory(self, event, items):
        self.inventory.update(
            event,
            items,
            self.world_x,
            self.world_y
        )

    # * Update function for move the player
    def update(self, keys_pressed, items, tile_w, tile_h, entities):
        delta_x = 0
        delta_y = 0
        base_y = self.world_y + self.height
        self.is_move = False
        self.tile_clmn = round(
            ((self.world_x / (tile_w / 2) + base_y / (tile_h / 2)) / 2), 2
        )
        self.tile_row = round(
            ((base_y / (tile_h / 2) - self.world_x / (tile_w / 2)) / 2), 2
        )

        # ? Horizontal axis configuration
        if keys_pressed[pygame.K_w]:
            delta_y -= self.speed
            self.is_move = True
        elif keys_pressed[pygame.K_s]:
            delta_y += self.speed
            self.is_move = True

        # ? Vertical axis configuration
        if keys_pressed[pygame.K_a]:
            delta_x -= self.speed
            self.is_move = True
        elif keys_pressed[pygame.K_d]:
            delta_x += self.speed
            self.is_move = True

        # ? Show hitbox
        if keys_pressed[pygame.K_r]:
            self.show_hitbox = True
        elif keys_pressed[pygame.K_e]:
            self.show_hitbox = False

        # ? Apply movement
        iso_x = delta_x - delta_y
        iso_y = (delta_x + delta_y) / 2

        length = (iso_x**2 + iso_y**2) ** 0.5
        if length > 0:
            iso_x = (iso_x / length) * self.speed
            iso_y = (iso_y / length) * self.speed

        self.world_x += iso_x
        self.world_y += iso_y

        self.depth = (self.tile_clmn + self.tile_row) - 0.5

        # ? Update player_state
        if delta_x < 0 and delta_y < 0:
            pass
        elif delta_x > 0 and delta_y < 0:
            pass
        elif delta_x < 0 and delta_y > 0:
            pass
        elif delta_x > 0 and delta_y > 0:
            pass
        elif delta_y < 0:
            self.player_state = "up_right"
        elif delta_y > 0:
            self.player_state = "down_left"
        elif delta_x < 0:
            self.player_state = "up_left"
        elif delta_x > 0:
            self.player_state = "down_right"

        # ? Shot a fire ball
        if keys_pressed[pygame.K_SPACE]:
            # ! Get the time of the shot
            current_time = pygame.time.get_ticks()

            # ! Compare the time of the shot with the delay
            if current_time - self.last_shot_time > self.shot_count_down:
                self.last_shot_time = current_time

                # ! Create the projectile
                if len(self.projectiles) < 10:
                    self.projectiles.append(Fire(
                        width=shot_width,
                        height=shot_height,
                        x=self.hitbox.x,
                        y=self.hitbox.centery,
                        speed=8,
                        shot_sprite="shot_sprite",
                        player_state=self.player_state
                    ))

        # ? Update all the prjectiles
        for shot in list(self.projectiles):
            shot.update()
            # ! If the projectiles is not in the window, remove to the list
            if (shot.hitbox.x > 800 or shot.hitbox.x < -80
                    or
                    shot.hitbox.y > 600 or shot.hitbox.y < -80):
                self.projectiles.remove(shot)

        # ? Add item in the inventory
        current_time = pygame.time.get_ticks()
        for item in items:
            if (
                    item.visible
                    and
                    current_time > item.pickup_delay
                    and
                    self.hitbox.colliderect(item.hitbox)):
                if self.inventory.put_images(item.name, item.durability, item.health):
                    item.visible = False

    # * Draw function for draw the player in the window
    def draw(self, wn):
        if self.show_hitbox:
            pygame.draw.rect(wn, (255, 0, 0), self.hitbox, 4)

        wn_x = self.wn_width // 2 - self.width // 2
        wn_y = self.wn_height // 2 - self.height // 2

        if self.player_state and self.is_move:
            self.anim_count += 1
            anim_list = self.sprites_dict["move"][self.player_state]
            current_frame = anim_list[self.anim_count // 5 % len(anim_list)]
            wn.blit(current_frame, (wn_x, wn_y))
        elif self.player_state and not self.is_move:
            # ? Transform the sprites
            self.anim_count = 0
            current_frame = self.sprites_dict["not_move"][self.player_state]
            wn.blit(current_frame, (wn_x, wn_y))
        # ? Fuck you
        else:
            print("\n\n  FUCK YOU!!!!  \n\n")

        # ? Draw all the prjectiles
        for shot in list(self.projectiles):
            shot.draw(wn)

        self.hitbox.x = wn_x
        self.hitbox.y = wn_y

    def attack(self, entities, events):
        for entity in entities:
            if events.type == pygame.MOUSEBUTTONDOWN and events.button == 1:
                if (
                        entity.life and
                        self.hitbox.colliderect(entity.hitbox) and
                        self.inventory.actual_item == "sword"):
                    self.inventory.use_item()
                    entity.take_damage()
                    break


# * Fire balls' class
class Fire(Entities):
    # * __init__
    def __init__(self, *groups, width, height, x, y, speed, shot_sprite, player_state):
        super().__init__(*groups, width=width, height=height, x=x, y=y)
        self.sprites = sprites_func_shot(self.width, self.height)
        self.speed = speed
        self.shot = self.sprites[shot_sprite]["shot"]
        self.player_state = player_state

    # * Update the fire ball
    def update(self):
        if self.player_state == "up_left":
            self.hitbox.x -= self.speed
            self.hitbox.y -= self.speed
        elif self.player_state == "up_right":
            self.hitbox.x += self.speed
            self.hitbox.y -= self.speed
        elif self.player_state == "down_left":
            self.hitbox.x -= self.speed
            self.hitbox.y += self.speed
        elif self.player_state == "down_right":
            self.hitbox.x += self.speed
            self.hitbox.y += self.speed

    # * Draw the fire ball
    def draw(self, wn):
        if self.visible:
            wn.blit(self.shot, self.hitbox)


# * Items' class
class Items(Entities):
    # * __init__
    def __init__(self, *groups, width, height, x, y, name_item, durability, item_power=None):
        super().__init__(*groups, width=width, height=height, x=x, y=y)
        self.sprites = sprites_func_items(self.width, self.height)
        self.name = name_item
        self.item = self.sprites["item_sprites"][self.name]
        self.world_x = x
        self.world_y = y
        self.spawn_time = 0
        self.lifetime = lifetime  # * 60*10^4ms (1 min)
        self.pickup_delay = 0
        self.power = item_power
        self.durability = durability
        self.health = durability

    # * Draw the Items
    def draw(self, wn, cam_x, cam_y):
        if self.visible:
            #pygame.draw.rect(wn, (255, 0, 0), self.hitbox, 4)
            wn_x = self.world_x - cam_x
            wn_y = self.world_y - cam_y
            wn.blit(self.item, (wn_x, wn_y))
            self.hitbox.x = wn_x
            self.hitbox.y = wn_y


# * Animals' class
class Animals(Entities):
    def __init__(self, width, height, x, y, speed, frames, animal, visible=True, health=3):
        super().__init__(width=width, height=height, x=x, y=y)
        self.speed = speed
        self.frames = frames
        self.animal = animal
        self.sprites_dic = {"animal_sprites": {}}
        self.anim_count = 0
        self.health = health
        self.initial_health = health
        self.life = True
        self.tile_clmn = 0
        self.tile_row = 0
        self.depth = self.tile_clmn + self.tile_row
        self.cam_x = 0
        self.cam_y = 0
        self.world_x = self.x
        self.world_y = self.y
        self.visible = visible

    def load_sprites(self):
        with open("src\\data\\json\\animals_path.json", "r", encoding="utf-8") as data:
            self.animals_paths = json.load(data)
        sprites_func_animals(
            self.animals_paths[self.animal]["idle"]["down"],
            self.frames, "down", self.width, self.height,
            self.animal, "idle", self.sprites_dic
        )

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.life = False

    def update(self, tile_w, tile_h, cam_x, cam_y):
        if not self.life:
            self.visible = False
        if self.visible:
            self.base_y = self.world_y + self.height
            self.tile_clmn = round(
                ((self.world_x / (tile_w / 2) + self.base_y / (tile_h / 2)) / 2), 2
            )
            self.tile_row = round(
                ((self.base_y / (tile_h / 2) - self.world_x / (tile_w / 2)) / 2), 2
            )

            self.depth = self.tile_clmn + self.tile_row

            self.cam_x = cam_x
            self.cam_y = cam_y

    def draw(self, wn):
        if self.visible:
            wn_x = self.world_x - self.cam_x
            wn_y = self.world_y - self.cam_y
            #pygame.draw.rect(wn, (255, 0, 0), self.hitbox, 4)
            frames = self.sprites_dic["animal_sprites"][self.animal]["idle"]["down"]
            current_frame = frames[self.anim_count // 5 % len(frames)]
            wn.blit(current_frame, (wn_x, wn_y))
            self.anim_count += 1

            if self.anim_count >= len(frames) * 5:
                self.anim_count = 0

            self.hitbox.x = wn_x
            self.hitbox.y = wn_y

    def barra_healt(self, wn, x, y):
        if self.health > 0:
            health_x = x - self.cam_x
            health_y = y - self.cam_y
            calculo_barra = int((self.health / self.initial_health) * width_health)
            rectangulo = pygame.Rect(health_x, health_y, calculo_barra, height_health)
            pygame.draw.rect(wn, (255, 0, 100), rectangulo)
        else:
            self.health = 0
