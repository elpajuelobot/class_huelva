# Imports
import pygame
from animations import *
from animations import sprites_func

# * Player's class
class Player:
    # * __Init__
    def __init__(self, width_player, height_player, x_player, y_player, sprites_player):
        self.width = width_player # * Player's width
        self.height = height_player # * Player's height
        self.x = x_player # * Player's x
        self.y = y_player # * Player's y
        self.hitbox_player = pygame.Rect(self.x, self.y, self.width, self.height) # * Player's hitbox
        self.player_state = "right" # * Player's state
        self.sprites_dict_func = sprites_func(self.width, self.height)
        self.sprites_dict = self.sprites_dict_func[sprites_player] # * Player's sprites
        self.anim_count = 0
        self.is_move = False
        self.show_hitbox = False

    # * Update function for move the player
    def update(self, keys_pressed):
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
