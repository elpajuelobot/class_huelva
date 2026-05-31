import pygame
import random
from src.core.settings.config import (
                        f_size, f_type, fps_pos, MAX_ITEMS_IN_WINDOWS,
                        fps_cap, white, x_player, y_player, width_player,
                        height_player, width_item, height_item, speed_player,
                        TILE_W, TILE_H, last_chunk_clmn, last_chunk_row,
                        MAX_ANIMALS_IN_WINDOWS, show_data, minimum_sed,
                        maximum_sed, soundtrack_path, sed_pos)
from src.core.entities.players import Player
from src.core.entities.items import Items
from src.core.entities.animals import Animals
from src.core.system.animations.animations import items_pool, animals_pool
from src.core.system.world.world_generator import World_generator
from src.core.system.inventory.inventory import Inventory
from src.core.entities.spawn_manager import SpawnManager
from src.core.system.game_states.initial import InitialMenu


class MotorGame:
    def __init__(self, width, height):
        pygame.init()
        pygame.mixer.init()
        self.width = width
        self.height = height
        self.wn = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maincraft")
        self.clock = pygame.time.Clock()
        self.run = True
        self.show_data = show_data
        self.last_chunk_clmn = last_chunk_clmn
        self.last_chunk_row = last_chunk_row
        self.setup_engine()
        self.actual_state = InitialMenu(self)


    def setup_engine(self):
        self.font = pygame.font.SysFont(f_type, f_size)
        self.music()

    def init_game_resources(self, sed):
        self.background(sed)
        self.inventory = Inventory()
        self.entities()
        self.sed_text = self.font.render(f"SED: {self.world.sed}", True, white)

    def background(self, sed):
        # * Background grid overlay — decorative tile grid scaled to fill the window
        self.gride = pygame.transform.scale(
            pygame.image.load("src\\data\\img\\background\\gradillas\\gradilla.png"),
            (self.width, self.height)
        ).convert_alpha()

        if sed:
            # * World generator — seed determines the procedural map (alternative seed: 65723874625)821365812
            self.world = World_generator(sed=sed, tile_w=TILE_W, tile_h=TILE_H)
        else:
            # * World generator — seed determines the procedural map (alternative seed: 65723874625)821365812
            self.world = World_generator(sed=random.randint(minimum_sed, maximum_sed), tile_w=TILE_W, tile_h=TILE_H)
        self.world.update_chunks(0, 0)  # * Queue the chunks around the spawn tile before the first frame

    def change_state(self, state):
        self.actual_state = state

    def entities(self):
        # * Player
        self.hero = Player(
            width=width_player, height=height_player, x=x_player, y=y_player,
            speed_player=speed_player, sprites_player="player", wn_width=self.width,
            wn_height=self.height, inventory=self.inventory, health=20, bubbles=6
        )

        # * Item pool — pre-allocate MAX_ITEMS_IN_WINDOWS slots; all start invisible and get reused as needed
        self.pool_items = [
            Items(x=0, y=0, width=width_item, height=height_item, name_item="banana", durability=0)
            for _ in range(MAX_ITEMS_IN_WINDOWS)
        ]

        # ! Todos los items como invisibles
        for item in self.pool_items:
            item.visible = False

        # * Place initial world items by activating free pool slots
        items_pool(pool=self.pool_items, name="coin",    x=100, y=103, health=1, durability=1)
        items_pool(pool=self.pool_items, name="cookie",  x=200, y=143, health=1, durability=1)
        items_pool(pool=self.pool_items, name="sword",   x=300, y=345, health=5, durability=5)
        items_pool(pool=self.pool_items, name="crystal", x=500, y=123, health=1, durability=1)

        # * Animal pool — same pattern as items: fixed-size pool, slots activated on demand
        self.pool_animals = [
            Animals(width=0, height=0, x=0, y=0, frames=0, animal="stag", world=self.world, visible=False)
            for _ in range(MAX_ANIMALS_IN_WINDOWS)
        ]

        # * Spawner
        self.spawner = SpawnManager(animals_pool, self.world)

    def music(self):
        pygame.mixer.music.load(soundtrack_path)
        #pygame.mixer.music.play(-1)

    def debugMode(self):
        if self.show_data:
            self.wn.blit(self.fps_text, fps_pos)
            self.wn.blit(self.sed_text, sed_pos)
            self.wn.blit(self.animals_text, (fps_pos[0] - 50, fps_pos[1] + 30))

    def loop(self):
        while self.run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False

            self.actual_state.events_(events)
            self.actual_state.update_()
            self.actual_state.draw_(self.wn)
            pygame.display.flip()
            self.clock.tick(fps_cap)
        pygame.quit()
