# Imports
import pygame

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# ? Window/World
height = 600
width = 800
MAX_ITEMS_IN_WINDOWS = 10
MAX_ANIMALS_IN_WINDOWS = 5
TILE_W = 128
TILE_H = 128
ISO_W = 128
ISO_H = 64
CHUNK = 16
CHUNK_DISTANCE = 3
last_chunk_clmn = -999
last_chunk_row = -999

# ? Colors
bg_color = (128, 0, 128)
fps_f_color = (255, 255, 255)
orange = (255, 102, 3)
grey_dark = (80, 80, 80)
grey_light = (198, 198, 198)
grey = (85, 85, 85)
grey_highlight = (237, 237, 237)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (114, 0, 194)

# ? FPS
f_size = 30
f_type = "Arial"
fps_pos = (10, 10)
fps_cap = 60

# ? Player
x_player = 400
y_player = 300
width_player = 55
height_player = 85
speed_player = 3

# ? Principal loop
run = True

# ? Fonts
font = pygame.font.SysFont(f_type, f_size)
inventory_font = pygame.font.SysFont(f_type, 13, bold=True)

# ? Shoot
shot_radius = 50
shot_width = 55
shot_height = 60
shot_cooldown = 500

# ? Inventory
inventory_x = 130
inventory_y = 10
inventory_width = 70
inventory_height = 70
inventory_squares = 10
squares_size = 50
squares_padding = 4

# ? Items
width_item = 50
height_item = 50
lifetime = 60000

# ? Animals
stag_width = 85
stag_height = 95

# ? Sounds
soundtrack = pygame.mixer.music.load("src\data\music\Minecraft 2015 soundtrack.mp3")

# ? Health
# ! Animals
width_health = 50
height_health = 5
