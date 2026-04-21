# imports
import pygame
from src.core.config import (
                        height, width, f_size, f_type, fps_pos, MAX_ITEMS_IN_WINDOWS,
                        fps_cap, fps_f_color, x_player, y_player, width_player,
                        height_player, run, width_item, height_item, speed_player,
                        TILE_W, TILE_H, last_chunk_clmn, last_chunk_row, CHUNK,
                        MAX_ANIMALS_IN_WINDOWS, stag_width, stag_height)
from src.core.player import Player, Items, Animals
from src.core.animations import items_pool, animals_pool
from src.core.world_generator import World_generator
from src.core.inventory import Inventory

# * Initialize Pygame
pygame.init()
pygame.mixer.init()


# * Window
wn = pygame.display.set_mode((width, height))
gride = pygame.transform.scale(
    pygame.image.load("src\\data\\img\\background\\gradillas\\gradilla.png"),
    (width, height)
).convert_alpha()
world = World_generator(sed=821365812, tile_w=TILE_W, tile_h=TILE_H) # 821365812, 65723874625
world.update_chunks(0, 0)  # * Upload the first chunk

# * Inventory
inventory = Inventory()

# * Player
hero = Player(
    width=width_player, height=height_player, x=x_player, y=y_player,
    speed_player=speed_player, sprites_player="player", wn_width=width,
    wn_height=height, inventory=inventory
)

# * Items
pool_items = [
    Items(x=0, y=0, width=width_item, height=height_item, name_item="banana", durability=0)
    for _ in range(MAX_ITEMS_IN_WINDOWS)
]

# ! Todos los items como invisibles
for item in pool_items:
    item.visible = False

items_pool(pool_items, "sword", 100, 103, 5)
items_pool(pool_items, "cookie", 200, 143, 1)
items_pool(pool_items, "sword",   300, 345, 5)
items_pool(pool_items, "crystal", 500, 123, 1)

# * Animals
pool_animals = [
    Animals(width=0, height=0, x=0, y=0, speed=0, frames=0, animal="stag", visible=False)
    for _ in range(MAX_ANIMALS_IN_WINDOWS)
]

animals_pool(pool_animals, "stag", 310, 413, stag_width, stag_height, 2, 24)
animals_pool(pool_animals, "stag", 110, 113, stag_width, stag_height, 2, 24)

# TODO: IMPORTANTE. METER EN ESTA LISTA TODAS LAS ENTIDADES CREADAS
entities_list = [e for e in pool_animals if e.visible]

players_list = [hero]

sprites_list = entities_list + players_list

# * Clock
clock = pygame.time.Clock()

# * Font
font = pygame.font.SysFont(f_type, f_size)

# * Play music
pygame.mixer.music.play(-1)

# * Main loop
while run:
    # * Keys Control
    keys_pressed = pygame.key.get_pressed()
    # * Events control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        hero.update_inventory(event, pool_items)
        hero.attack(entities_list, event)

    # * Camera
    cam_x = hero.world_x - width // 2
    cam_y = hero.world_y - height // 2

    # * Background
    world.process_queue()
    wn.blit(gride, (0,0))
    current_chunk_clmn = round(hero.tile_clmn) // CHUNK
    current_chunk_row = round(hero.tile_row) // CHUNK

    if current_chunk_clmn != last_chunk_clmn or current_chunk_row != last_chunk_row:
        world.update_chunks(round(hero.tile_clmn), round(hero.tile_row))
        last_chunk_clmn = current_chunk_clmn
        last_chunk_row = current_chunk_row
    world.draw(wn, cam_x, cam_y)

    # * FPS write
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, fps_f_color)

    # * Player
    hero.update(keys_pressed, pool_items, TILE_W, TILE_H, 1)

    # * Animals
    #stag.update(TILE_W, TILE_H, cam_x, cam_y)
    #stag2.update(TILE_W, TILE_H, cam_x, cam_y)

    sprites_list.sort(key=lambda x: x.depth)
    for entity in sprites_list:
        entity.draw(wn)
    for entity in entities_list:
        entity.update(TILE_W, TILE_H, cam_x, cam_y)
        entity.barra_healt(wn, entity.world_x, entity.world_y)


    # * Draw Items
    for item in pool_items:
        item.draw(wn, cam_x, cam_y)

    current_time = pygame.time.get_ticks()
    for item in pool_items:
        if item.visible and current_time - item.spawn_time > item.lifetime:
            item.visible = False

    # * Draw the Inventory
    inventory.draw(wn)

    # * Write the FPS in the window
    wn.blit(fps_text, fps_pos)

    # * Update
    pygame.display.flip()

    # * The clock of the game (FPS)
    clock.tick(fps_cap)

pygame.quit()
