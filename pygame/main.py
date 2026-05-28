# imports
import pygame
import random
from src.core.settings.config import (
                        height, width, f_size, f_type, fps_pos, MAX_ITEMS_IN_WINDOWS,
                        fps_cap, white, x_player, y_player, width_player,
                        height_player, run, width_item, height_item, speed_player,
                        TILE_W, TILE_H, last_chunk_clmn, last_chunk_row, CHUNK,
                        MAX_ANIMALS_IN_WINDOWS, stag_width, stag_height, show_data,
                        player_health_x, player_health_y, soundtrack_path, minimum_sed,
                        maximum_sed, sed_pos)
from src.core.entities.players import Player
from src.core.entities.items import Items
from src.core.entities.animals import Animals
from src.core.entities.proyectiles import Fire
from src.core.system.animations.animations import items_pool, animals_pool
from src.core.system.world.world_generator import World_generator
from src.core.system.inventory.inventory import Inventory
from src.core.entities.spawn_manager import SpawnManager

# * Initialize Pygame
pygame.init()
pygame.mixer.init()


# * Window — main display surface
wn = pygame.display.set_mode((width, height))

# * Background grid overlay — decorative tile grid scaled to fill the window
gride = pygame.transform.scale(
    pygame.image.load("src\\data\\img\\background\\gradillas\\gradilla.png"),
    (width, height)
).convert_alpha()

# * World generator — seed determines the procedural map (alternative seed: 65723874625)821365812
world = World_generator(sed=random.randint(minimum_sed, maximum_sed), tile_w=TILE_W, tile_h=TILE_H)
world.update_chunks(0, 0)  # * Queue the chunks around the spawn tile before the first frame

# * Inventory
inventory = Inventory()

# * Player
hero = Player(
    width=width_player, height=height_player, x=x_player, y=y_player,
    speed_player=speed_player, sprites_player="player", wn_width=width,
    wn_height=height, inventory=inventory, health=20, bubbles=6
)


# * Item pool — pre-allocate MAX_ITEMS_IN_WINDOWS slots; all start invisible and get reused as needed
pool_items = [
    Items(x=0, y=0, width=width_item, height=height_item, name_item="banana", durability=0)
    for _ in range(MAX_ITEMS_IN_WINDOWS)
]

# ! Todos los items como invisibles
for item in pool_items:
    item.visible = False

# * Place initial world items by activating free pool slots
items_pool(pool=pool_items, name="coin",    x=100, y=103, health=1, durability=1)
items_pool(pool=pool_items, name="cookie",  x=200, y=143, health=1, durability=1)
items_pool(pool=pool_items, name="sword",   x=300, y=345, health=5, durability=5)
items_pool(pool=pool_items, name="crystal", x=500, y=123, health=1, durability=1)

# * Animal pool — same pattern as items: fixed-size pool, slots activated on demand
pool_animals = [
    Animals(width=0, height=0, x=0, y=0, frames=0, animal="stag", world=world, visible=False)
    for _ in range(MAX_ANIMALS_IN_WINDOWS)
]

# * Spawner
spawner = SpawnManager(animals_pool, world)

# TODO: IMPORTANTE. METER EN ESTA LISTA TODAS LAS ENTIDADES CREADAS
# * Snapshot of active entities/items at startup — these lists are static after init,
# * so newly spawned entities won't be added automatically; that's the TODO above
entities_list = pool_animals
items_list = [e for e in pool_items if e.visible]
players_list = [hero]

# * Master draw list — sorted by depth each frame for correct isometric layering
sprites_list = entities_list + players_list + items_list

# * Clock
clock = pygame.time.Clock()

# * Font
font = pygame.font.SysFont(f_type, f_size)

# * Save world sed
sed_text = font.render(f"SED: {world.sed}", True, white)

# * Load and play music
pygame.mixer.music.load(soundtrack_path)
#pygame.mixer.music.play(-1)

while run:
    # * Keys Control — sampled once per frame and passed to whoever needs them
    keys_pressed = pygame.key.get_pressed()

    # * Events control — one-shot actions (quit, keydown, inventory, attack)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                # * F3 toggles FPS counter and hitbox debug overlay for all sprites
                show_data = not show_data
                for entity in sprites_list:
                    entity.show_hitbox = not entity.show_hitbox

        hero.update_inventory(event, pool_items)
        hero.attack(event)

    # * Camera — offset so the player is always centred on screen
    cam_x = hero.world_x - width  // 2
    cam_y = hero.world_y - height // 2

    wn.blit(gride, (0, 0))  # * Draw the grid overlay first (bottommost layer)
    result = world.process_queue()  # * Generate one pending chunk per frame
    if result:
        chunk_clmn, chunk_row = result
        spawner.create_animals(pool_animals, chunk_clmn, chunk_row, "stag", stag_width, stag_height, 24, 4)

    # * Check if the player has crossed into a new chunk and trigger a chunk update if so
    current_chunk_clmn = round(hero.tile_clmn) // CHUNK
    current_chunk_row  = round(hero.tile_row)  // CHUNK

    if current_chunk_clmn != last_chunk_clmn or current_chunk_row != last_chunk_row:
        world.update_chunks(round(hero.tile_clmn), round(hero.tile_row), pool_animals)
        last_chunk_clmn = current_chunk_clmn
        last_chunk_row  = current_chunk_row

    world.draw(wn, cam_x, cam_y)

    # * Pre-render FPS text (blit happens later, only if show_data is True)
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, white)
    active_animals = sum(1 for a in pool_animals if a.visible)
    animals_text = font.render(f"Animals: {active_animals}", True, white)

    # * Update the animals
    for entity in entities_list:
        if entity.visible:
            entity.update(cam_x, cam_y, hero.world_x, hero.world_y)
            entity.barra_healt(wn, entity.world_x, entity.world_y)  # * Health bar drawn in world space above the entity

    hero.update(keys_pressed, pool_items, cam_x, cam_y, entities_list, world, Fire)

    # * Sort sprites back-to-front by isometric depth before drawing
    sprites_list.sort(key=lambda x: x.depth)
    for entity in sprites_list:
        entity.draw(wn)

    for item in pool_items:
        item.update(cam_x, cam_y)  # * Recalculate screen position; draw() is handled via sprites_list

    hero.barra_healt(wn, player_health_x, player_health_y)  # * Fixed-position health bar (top-left)
    hero.bubbles_bar(wn, 5, 50)  # * Oxygen bubbles (only visible in water)

    # * Expire items that have exceeded their lifetime
    current_time = pygame.time.get_ticks()
    for item in pool_items:
        if item.visible and current_time - item.spawn_time > item.lifetime:
            item.visible = False

    inventory.draw(wn)  # * Hotbar drawn on top of everything else

    # * Write the FPS in the window
    if show_data:
        wn.blit(fps_text, fps_pos)
        wn.blit(sed_text, sed_pos)
        wn.blit(animals_text, (fps_pos[0] - 50, fps_pos[1] + 30))

    pygame.display.flip()  # * Push the completed frame to the screen
    clock.tick(fps_cap)  # * Cap framerate and yield CPU time

pygame.quit()
