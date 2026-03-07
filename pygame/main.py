# imports
import pygame
from src.config import (height, width, f_size, f_type, bg_color, fps_pos,
                        fps_cap, fps_f_color, x_player, y_player, widht_player,
                        height_player, run)
from player import Player

# * init
pygame.init()

# * screen
wn = pygame.display.set_mode((width , height))

# * Player
hero = Player(widht_player, height_player, x_player, y_player, "player")

# * clock
clock = pygame.time.Clock()

# * font
font = pygame.font.SysFont(f_type, f_size)

# * main loop
while run:
    # * Control de 
    keys_pressed = pygame.key.get_pressed()
    # * control quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # * background
    wn.fill(bg_color)

    # * fps write
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, fps_f_color)

    # * Player
    hero.update(keys_pressed)
    hero.draw(wn)

    # * draw
    wn.blit(fps_text, fps_pos)

    # * update
    pygame.display.flip()

    # * fps
    clock.tick(fps_cap)

pygame.quit()
