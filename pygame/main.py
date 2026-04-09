# imports
import pygame
from src.core.config import (
                        height, width, f_size, f_type, fps_pos,
                        fps_cap, fps_f_color, x_player, y_player, widht_player,
                        height_player, run, width_item, height_item, speed_player)
from src.core.player import Player, Items

# * Initialize Pygame
pygame.init()

# * Window
wn = pygame.display.set_mode((width, height))
gride = pygame.transform.scale(pygame.image.load("src\\data\\img\\background\\gradilla.png"), (width, height)).convert_alpha()

# * Player
hero = Player(widht_player, height_player, x_player, y_player, speed_player, "player")

# * Items
items = [
    Items(
        x_item=100, y_item=103,
        width_item=width_item,
        height_item=height_item,
        name_item="banana"),
    Items(
        x_item=200, y_item=143,
        width_item=width_item,
        height_item=height_item,
        name_item="cookie"),
    Items(
        x_item=300, y_item=345,
        width_item=width_item,
        height_item=height_item,
        name_item="coin"),
    Items(
        x_item=500, y_item=123,
        width_item=width_item,
        height_item=height_item,
        name_item="crystal")
]

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

        hero.update_inventory(event, items, Items)

    # * Background
    wn.blit(gride, (0,0))

    # * FPS write
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, fps_f_color)

    # * Player
    hero.update(keys_pressed, items)
    hero.draw(wn)

    # * Draw Items
    for item in items:
        item.draw(wn)
        if not item.visible:
            items.remove(item)

    # * Write the FPS in the window
    wn.blit(fps_text, fps_pos)

    # * Update
    pygame.display.flip()

    # * The clock of the game (FPS)
    clock.tick(fps_cap)

pygame.quit()
