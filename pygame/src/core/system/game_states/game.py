import pygame
from src.core.system.game_states.fatherClass import GameState
from src.core.system.game_states.defeat import Defeat
from src.core.entities.proyectiles import Fire
from src.core.settings.config import (
    white, CHUNK, stag_width, stag_height, player_health_x, player_health_y
)


class GamingState(GameState):
    def __init__(self, motor, sed=None):
        super().__init__(motor)
        self.motor.init_game_resources(sed)
        self.cam_x = 0
        self.cam_y = 0

    def events_(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.motor.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    self.motor.show_data = not self.motor.show_data
                    for entity in self.motor.pool_animals + [self.motor.hero] + self.motor.pool_items:
                        entity.show_hitbox = self.motor.show_data

                elif event.key == pygame.K_ESCAPE:
                    from src.core.system.game_states.pause import PauseMenu
                    self.motor.change_state(PauseMenu(self.motor, self))

            self.motor.hero.update_inventory(event, self.motor.pool_items)
            self.motor.hero.attack(event)


    def update_(self):
        self.motor.keys_pressed = pygame.key.get_pressed()

        # * Camera — offset so the player is always centred on screen
        self.cam_x = self.motor.hero.world_x - self.motor.width  // 2
        self.cam_y = self.motor.hero.world_y - self.motor.height // 2

        result = self.motor.world.process_queue()  # * Generate one pending chunk per frame
        if result:
            chunk_clmn, chunk_row = result
            self.motor.spawner.create_animals(self.motor.pool_animals, chunk_clmn, chunk_row, "stag", stag_width, stag_height, 24, 4)

        # * Check if the player has crossed into a new chunk and trigger a chunk update if so
        current_chunk_clmn = round(self.motor.hero.tile_clmn) // CHUNK
        current_chunk_row = round(self.motor.hero.tile_row) // CHUNK

        if current_chunk_clmn != self.motor.last_chunk_clmn or current_chunk_row != self.motor.last_chunk_row:
            self.motor.world.update_chunks(round(self.motor.hero.tile_clmn), round(self.motor.hero.tile_row), self.motor.pool_animals)
            self.motor.last_chunk_clmn = current_chunk_clmn
            self.motor.last_chunk_row  = current_chunk_row

        # * Pre-render FPS text (blit happens later, only if show_data is True)
        self.motor.fps_text = self.motor.font.render(f"FPS: {int(self.motor.clock.get_fps())}", True, white)
        active_animals = sum(1 for a in self.motor.pool_animals if a.visible)
        self.motor.animals_text = self.motor.font.render(f"Animals: {active_animals}", True, white)

        # * Update the animals
        for entity in self.motor.pool_animals:
            if entity.visible:
                entity.update(self.cam_x, self.cam_y, self.motor.hero.world_x, self.motor.hero.world_y)

        self.motor.hero.update(self.motor.keys_pressed, self.motor.pool_items, self.cam_x, self.cam_y, self.motor.pool_animals, self.motor.world, Fire)

        # * Expire items that have exceeded their lifetime
        current_time = pygame.time.get_ticks()
        for item in self.motor.pool_items:
            if item.visible:
                item.update(self.cam_x, self.cam_y)  # * Recalculate screen position; draw() is handled via sprites_list
                if current_time - item.spawn_time > item.lifetime:
                    item.visible = False

        if self.motor.hero.health <= 0:
            self.motor.change_state(Defeat(self.motor, self))


    def draw_(self, wn):
        wn.blit(self.motor.gride, (0, 0))  # * Draw the grid overlay first (bottommost layer)

        self.motor.world.draw(wn, self.cam_x, self.cam_y)

        # * Sort sprites back-to-front by isometric depth before drawing
        sprites_list = [self.motor.hero] + \
                        [a for a in self.motor.pool_animals if a.visible] + \
                        [i for i in self.motor.pool_items if i.visible]
        sprites_list.sort(key=lambda x: x.depth)
        for entity in sprites_list:
            entity.draw(wn)
            if hasattr(entity, 'animal') and entity.visible:
                entity.barra_healt(wn, entity.world_x, entity.world_y)  # * Health bar drawn in world space above the entity

        self.motor.hero.barra_healt(wn, player_health_x, player_health_y)
        self.motor.hero.bubbles_bar(wn, 5, 50)
        self.motor.inventory.draw(wn)

        self.motor.debugMode()
