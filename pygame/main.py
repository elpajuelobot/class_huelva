# imports
import pygame
from src.core.config import (
                        height, width, f_size, f_type, fps_pos, MAX_ITEMS_IN_WINDOWS,
                        fps_cap, fps_f_color, x_player, y_player, widht_player,
                        height_player, run, width_item, height_item, speed_player,
                        TILE_W, TILE_H, last_chunk_clmn, last_chunk_row, CHUNK,
                        soundtrack)
from src.core.player import Player, Items, Animals
from src.core.animations import items_pool
from src.core.world_generator import World_generator

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

# * Player
hero = Player(widht_player, height_player, x_player, y_player, speed_player, "player")

# * Items
pool_items = [
    Items(x=0, y=0, width=width_item, height=height_item, name_item="banana")
    for _ in range(MAX_ITEMS_IN_WINDOWS)
]

# ! Todos los items como invisibles
for item in pool_items:
    item.visible = False

items_pool(pool_items, "coin", 100, 103)
items_pool(pool_items, "cookie", 200, 143)
items_pool(pool_items, "coin",   300, 345)
items_pool(pool_items, "crystal", 500, 123, "shoot")

# * Animals
animals = [
    Animals("stag", 75, 85, 110, 113, 2, 24),
    Animals("stag", 75, 85, 300, 200, 2, 24),
]


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
    hero.update(keys_pressed, pool_items, TILE_W, TILE_H)
    hero.draw(wn, width, height)

    # * Animals
    for animal in animals:
        animal.draw(wn, cam_x, cam_y)

    # * Draw Items
    for item in pool_items:
        item.draw(wn, cam_x, cam_y)

    current_time = pygame.time.get_ticks()
    for item in pool_items:
        if item.visible and current_time - item.spawn_time > item.lifetime:
            item.visible = False

    for shot in list(hero.projectiles):
        for animal in animals:
            if animal.alive and shot.hitbox.colliderect(animal.hitbox):
                animal.take_damage()
                hero.projectiles.remove(shot)
                break


    # * Write the FPS in the window
    wn.blit(fps_text, fps_pos)

    # * Update
    pygame.display.flip()

    # * The clock of the game (FPS)
    clock.tick(fps_cap)

pygame.quit()
