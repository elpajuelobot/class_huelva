# Imports
import pygame
from src.core.animations import *
from src.core.animations import sprites_func_player, sprites_func_shot, sprites_func_items
from src.core.config import (shot_width, shot_height, shot_cooldown)
from src.core.inventory import Inventory

# * Player's class
class Player:
    # * __Init__
    def __init__(self, width_player, height_player, x_player, y_player, sprites_player):
        self.width = width_player # * Player's width
        self.height = height_player # * Player's height
        self.sprites = sprites_func_player(self.width, self.height)
        self.x = x_player # * Player's x
        self.y = y_player # * Player's y
        self.hitbox_player = pygame.Rect(self.x, self.y, self.width, self.height) # * Player's hitbox
        self.player_state = "right" # * Player's state
        self.sprites_dict = self.sprites[sprites_player] # * Player's sprites
        self.anim_count = 0 # * A counter for the frames of the player's animation
        self.is_move = False # * Can't move in the begining
        self.show_hitbox = False # * Don't show the hitbox
        self.is_shot = False # * If the player throwing a fire ball?
        self.projectiles = [] # * List with all the projectiles that the player creates
        self.can_create_shot = False # * If the player can create a projectiles
        self.last_shot_time = 0 # * The time of the last fire ball
        self.shot_count_down = shot_cooldown # * Delay for the fire balls
        self.inventory = Inventory() # * Create the inventory

    # * Update function for move the player
    def update(self, keys_pressed, items):
        delta_x = 0
        delta_y = 0
        self.is_move = False

        # ? Horizontal axis configuration
        if keys_pressed[pygame.K_w] and self.hitbox_player.y > 0:
            delta_y -= 5
            self.is_move = True
        elif keys_pressed[pygame.K_s] and self.hitbox_player.y < 515:
            delta_y += 5
            self.is_move = True

        # ? Vertical axis configuration
        if keys_pressed[pygame.K_a] and self.hitbox_player.x > 0:
            delta_x -= 5
            self.is_move = True
        elif keys_pressed[pygame.K_d] and self.hitbox_player.x < 744:
            delta_x += 5
            self.is_move = True

        # ? Show hitbox
        if keys_pressed[pygame.K_r]:
            self.show_hitbox = True
        elif keys_pressed[pygame.K_e]:
            self.show_hitbox = False

        # ? Apply movement
        self.hitbox_player.x += delta_x
        self.hitbox_player.y += delta_y

        # ? Update player_state
        if delta_x < 0 and delta_y < 0:
            self.player_state = "up_left"
        elif delta_x > 0 and delta_y < 0:
            self.player_state = "up_right"
        elif delta_x < 0 and delta_y > 0:
            self.player_state = "down_left"
        elif delta_x > 0 and delta_y > 0:
            self.player_state = "down_right"
        elif delta_y < 0:
            self.player_state = "up"
        elif delta_y > 0:
            self.player_state = "down"
        elif delta_x < 0:
            self.player_state = "left"
        elif delta_x > 0:
            self.player_state = "right"

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
                        x_shot=self.hitbox_player.x,
                        y_shot=self.hitbox_player.centery,
                        speed_shot=8,
                        shot_sprite="shot_sprite",
                        player_state=self.player_state
                    ))

        # ? Update all the prjectiles
        for shot in list(self.projectiles):
            shot.update()
            # ! If the projectiles is not in the window, remove to the list
            if (shot.shot_hitbox.x > 800 or shot.shot_hitbox.x < -80
                    or
                    shot.shot_hitbox.y > 600 or shot.shot_hitbox.y < -80):
                self.projectiles.remove(shot)

        # ? Add item in the inventory
        for item in items:
            if item.visible and self.hitbox_player.colliderect(item.hitbox_item):
                if self.inventory.put_images(item.name):
                    item.visible = False

    # * Draw function for draw the player in the window
    def draw(self, wn):
        if self.show_hitbox:
            pygame.draw.rect(wn, (255, 0, 0), self.hitbox_player, 4)
        if self.player_state and self.is_move:
            self.anim_count += 1
            anim_list = self.sprites_dict["move"][self.player_state]
            # ? Transform the sprites
            current_frame = anim_list[self.anim_count // 5 % len(anim_list)]
            # ! Draw the player
            wn.blit(current_frame, self.hitbox_player)
        elif self.player_state and not self.is_move:
            # ? Transform the sprites
            self.anim_count = 0
            current_frame = self.sprites_dict["not_move"][self.player_state]
            # ! Draw the player
            wn.blit(current_frame, self.hitbox_player)
        # ? Fuck you
        else:
            print("\n\n  FUCK YOU!!!!  \n\n")

        # ? Draw all the prjectiles
        for shot in list(self.projectiles):
            shot.draw(wn)

        # ? Draw the Inventory
        self.inventory.draw(wn)


# * Fire balls' class
class Fire:
    # * __init__
    def __init__(self, x_shot, y_shot, speed_shot, shot_sprite, player_state):
        self.x = x_shot
        self.y = y_shot
        self.width = shot_width
        self.height = shot_height
        self.sprites = sprites_func_shot(self.width, self.height)
        self.speed = speed_shot
        self.shot_hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shot = self.sprites[shot_sprite]["shot"]
        self.visible = True
        self.player_state = player_state

    # * Update the fire ball
    def update(self):
        if self.player_state == "right":
            self.shot_hitbox.x += self.speed
        elif self.player_state == "left":
            self.shot_hitbox.x -= self.speed
        elif self.player_state == "up":
            self.shot_hitbox.y -= self.speed
        elif self.player_state == "down":
            self.shot_hitbox.y += self.speed

        elif self.player_state == "up_left":
            self.shot_hitbox.x -= self.speed
            self.shot_hitbox.y -= self.speed
        elif self.player_state == "up_right":
            self.shot_hitbox.x += self.speed
            self.shot_hitbox.y -= self.speed
        elif self.player_state == "down_left":
            self.shot_hitbox.x -= self.speed
            self.shot_hitbox.y += self.speed
        elif self.player_state == "down_right":
            self.shot_hitbox.x += self.speed
            self.shot_hitbox.y += self.speed

    # * Draw the fire ball
    def draw(self, wn):
        if self.visible:
            wn.blit(self.shot, self.shot_hitbox)


# * Items' class
class Items:
    # * __init__
    def __init__(self, x_item, y_item, width_item, height_item, name_item):
        self.x = x_item
        self.y = y_item
        self.width = width_item
        self.height = height_item
        self.hitbox_item = pygame.Rect(self.x, self.y, self.width, self.height)
        self.sprites = sprites_func_items(self.width, self.height)
        self.name = name_item
        self.item = self.sprites["item_sprites"][self.name]
        self.visible = True

    # * Draw the Items
    def draw(self, wn):
        if self.visible:
            wn.blit(self.item, self.hitbox_item)
