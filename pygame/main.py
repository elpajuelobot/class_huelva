# imports
import pygame
from src.core.config import (
                        height, width, f_size, f_type, fps_pos, MAX_ITEMS_IN_WINDOWS,
                        fps_cap, fps_f_color, x_player, y_player, widht_player,
                        height_player, run, width_item, height_item, speed_player,
                        COLUMNS, ROWS, TILE_W, TILE_H)
from src.core.player import Player, Items
from src.core.animations import items_pool
from src.core.world_generator import World_generator

# * Initialize Pygame
pygame.init()

# * Window
wn = pygame.display.set_mode((width, height))
gride = pygame.transform.scale(
    pygame.image.load("src\\data\\img\\background\\gradilla.png"),
    (width, height)
).convert_alpha()
world = World_generator(sed=821365812, columns=COLUMNS, rows=ROWS, tile_w=TILE_W, tile_h=TILE_H)
world.generate_map()

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

#items_pool(pool_items, "banana", 100, 103)
#items_pool(pool_items, "cookie", 200, 143)
#items_pool(pool_items, "coin",   300, 345)
#items_pool(pool_items, "crystal", 500, 123)

# * Clock
clock = pygame.time.Clock()

# * Font
font = pygame.font.SysFont(f_type, f_size)

# * Main loop
while run:
    # * Keys Control
    keys_pressed = pygame.key.get_pressed()
    # * Control quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        hero.update_inventory(event, pool_items)

    cam_x = hero.world_x - width // 2
    cam_y = hero.world_y - height // 2

    # * Background
    wn.blit(gride, (0,0))
    world.draw(wn, cam_x, cam_y)

    # * FPS write
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, fps_f_color)

    # * Player
    hero.update(keys_pressed, pool_items, TILE_W, TILE_H)
    hero.draw(wn, width, height)

    print(f"({hero.tile_row}, {hero.tile_clmn})")

    # * Draw Items
    for item in pool_items:
        item.draw(wn)

    # * Write the FPS in the window
    wn.blit(fps_text, fps_pos)

    # * Update
    pygame.display.flip()

    # * The clock of the game (FPS)
    clock.tick(fps_cap)

pygame.quit()
