import pygame

# * Base class for all entities in the game (player, animals, items, projectiles)
class Entities(pygame.sprite.Sprite):
    def __init__(self, *groups, width, height, x, y):
        super().__init__(*groups)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        # * Collision rectangle, starts at spawn position
        self.hitbox = pygame.Rect(
            self.x, self.y,
            self.width, self.height
        )
        self.show_hitbox = False  # * Toggle with F3 to debug collisions
        self.visible = True
        self.health_bar = True  # * Whether to draw the health bar above this entity
