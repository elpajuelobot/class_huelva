# Imports
import pygame
from src.core.animations import (
    sprites_func_player,
    sprites_func_shot,
    sprites_func_items,
)
from src.core.config import (
    shot_width,
    shot_height,
    shot_cooldown,
    lifetime
)
from src.core.inventory import Inventory


class Objetos(pygame.sprite.Sprite):
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


# * Player's class
class Player:
    # * __Init__
    def __init__(
            self, width_player, height_player,
            x_player, y_player, speed_player, sprites_player):
        self.width = width_player  # * Player's width
        self.height = height_player  # * Player's height
        self.sprites = sprites_func_player(self.width, self.height)
        self.x = x_player  # * Player's x
        self.y = y_player  # * Player's y
        self.hitbox_player = pygame.Rect(
            self.x, self.y,
            self.width, self.height)  # * Player's hitbox
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
        self.inventory = Inventory()  # * Create the inventory
        self.world_x = x_player
        self.world_y = y_player
        # ? Update the actual column and row
        self.tile_clmn = 0
        self.tile_row = 0

    # * Update de inventory
    def update_inventory(self, event, items):
        self.inventory.update(
            event,
            items,
            self.world_x,
            self.world_y
        )

    # * Update function for move the player
    def update(self, keys_pressed, items, tile_w, tile_h):
        delta_x = 0
        delta_y = 0
        self.is_move = False
        self.tile_clmn = round(
            ((self.world_x / (tile_w / 2) + self.world_y / (tile_h / 2)) / 2), 2
        )
        self.tile_row = round(
            ((self.world_y / (tile_h / 2) - self.world_x / (tile_w / 2)) / 2), 2
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
                        x=self.hitbox_player.x,
                        y=self.hitbox_player.centery,
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
                    self.hitbox_player.colliderect(item.hitbox)):
                if self.inventory.put_images(item.name):
                    item.visible = False

    # * Draw function for draw the player in the window
    def draw(self, wn, wn_width, wn_height):
        if self.show_hitbox:
            pygame.draw.rect(wn, (255, 0, 0), self.hitbox_player, 4)

        wn_x = wn_width // 2 - self.width // 2
        wn_y = wn_height // 2 - self.height // 2

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

        # ? Draw the Inventory
        self.inventory.draw(wn)

        self.hitbox_player.x = wn_x
        self.hitbox_player.y = wn_y


# * Fire balls' class
class Fire(Objetos):
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
class Items(Objetos):
    # * __init__
    def __init__(self, *groups, width, height, x, y, name_item):
        super().__init__(*groups, width=width, height=height, x=x, y=y)
        self.sprites = sprites_func_items(self.width, self.height)
        self.name = name_item
        self.item = self.sprites["item_sprites"][self.name]
        self.world_x = x
        self.world_y = y
        self.spawn_time = 0
        self.lifetime = lifetime  # * 60*10^4ms (1 min)
        self.pickup_delay = 0

    # * Draw the Items
    def draw(self, wn, cam_x, cam_y):
        if self.visible:
            #pygame.draw.rect(wn, (255, 0, 0), self.hitbox, 4)
            wn_x = self.world_x - cam_x
            wn_y = self.world_y - cam_y
            wn.blit(self.item, (wn_x, wn_y))
            self.hitbox.x = wn_x
            self.hitbox.y = wn_y
