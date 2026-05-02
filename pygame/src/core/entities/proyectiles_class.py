import pygame
from src.core.entities.sprites_class import Entities
from src.core.animations import sprites_func_shot

# * Fire balls' class
class Fire(Entities):
    # * __init__
    def __init__(self, *groups, width, height, x, y, speed, shot_sprite, player_state):
        super().__init__(*groups, width=width, height=height, x=x, y=y)
        self.sprites = sprites_func_shot(self.width, self.height)
        self.speed = speed
        self.shot = self.sprites[shot_sprite]["shot"]  # * Projectile sprite image
        self.player_state = player_state  # * Direction inherited from the player at the moment of firing
        self.world_x = x
        self.world_y = y
        self.cam_x = 0
        self.cam_y = 0

    # * Move the projectile each frame and update its screen-space hitbox
    def update(self, cam_x, cam_y):
        # * Map player state to a screen-space delta, then convert to isometric movement
        directions = {
            "up_right":   (0,          -self.speed),
            "up_left":    (-self.speed, 0),
            "down_right": (self.speed,  0),
            "down_left":  (0,           self.speed)
        }

        delta_x, delta_y = directions.get(self.player_state, (0, 0))
        iso_x = delta_x - delta_y
        iso_y = (delta_x + delta_y) / 2

        self.world_x += iso_x
        self.world_y += iso_y

        # * Convert world position to screen position using the camera offset
        self.hitbox.x = self.world_x - cam_x
        self.hitbox.y = self.world_y - cam_y

    # * Draw the fire ball
    def draw(self, wn):
        if self.visible:
            wn.blit(self.shot, self.hitbox)
            if self.show_hitbox:
                pygame.draw.rect(wn, (255, 0, 0), self.hitbox, 4)
