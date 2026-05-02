# Imports
from pygame import image, transform, Rect, time
from core.settings.config import player_core_w, player_core_h


# * Load and slice the player sprite sheet into directional move/idle animations
def sprites_func_player(width_player, height_player):
    imagen_completa = image.load("src\\data\\img\\player\\player_Completo.png").convert_alpha()
    player_core   = image.load("src\\data\\img\\player\\health\\core.png").convert_alpha()
    player_bubble = image.load("src\\data\\img\\player\\health\\bubble.png").convert_alpha()
    hoja_ancho, hoja_alto = imagen_completa.get_size()

    # * Each cell size in the original sheet (8 columns × 3 rows)
    f_ancho_orig = hoja_ancho / 8
    f_alto_orig  = hoja_alto  / 3

    # * Column order in the sprite sheet matches this direction list
    directions = ["up", "up_right", "right", "down_right", "down", "down_left", "left", "up_left"]
    sprites = {
        "player": {
            "move":     {},
            "not_move": {},
            "health": {
                "core":   {},
                "bubble": {}
            }
        }
    }

    for c, dir_name in enumerate(directions):
        move_frames = []
        # * Row indices 0→1→2→1 give a 4-frame walk cycle using only 3 rows
        for f in [0, 1, 2, 1]:
            rect_bruto   = Rect(int(c * f_ancho_orig), int(f * f_alto_orig), int(f_ancho_orig), int(f_alto_orig))
            sprite_sucio = imagen_completa.subsurface(rect_bruto)

            # * Trim transparent padding so the sprite fills its bounding box
            area_dibujo  = sprite_sucio.get_bounding_rect()
            sprite_limpio = sprite_sucio.subsurface(area_dibujo)

            move_frames.append(transform.scale(sprite_limpio, (width_player, height_player)))

        sprites["player"]["move"][dir_name] = move_frames

        # * Idle frame: row 1 (middle row) is the neutral pose for each direction
        rect_quieto    = Rect(int(c * f_ancho_orig), int(1 * f_alto_orig), int(f_ancho_orig), int(f_alto_orig))
        sprite_q_sucio = imagen_completa.subsurface(rect_quieto)
        area_q         = sprite_q_sucio.get_bounding_rect()
        sprite_q_limpio = sprite_q_sucio.subsurface(area_q)

        sprites["player"]["not_move"][dir_name] = transform.scale(sprite_q_limpio, (width_player, height_player))

    # * Scale health UI icons to match the configured HUD size
    sprites["player"]["health"]["core"]   = transform.scale(player_core,   (player_core_w, player_core_h))
    sprites["player"]["health"]["bubble"] = transform.scale(player_bubble, (player_core_w, player_core_h))

    return sprites


# * Load the projectile sprite and scale it to the configured shot dimensions
def sprites_func_shot(shot_witdh, shot_height):
    sprites = {
        "shot_sprite": {
            "shot": transform.scale(
                image.load("src\\data\\img\\shot_player\\shot_image.png"),
                (shot_witdh, shot_height)
            )
        }
    }

    return sprites


# * Search a free (invisible) slot in the projectile pool and activate it at (x, y)
def projectils_pool(pool, x, y):
    for shoot in pool:
        if not shoot.visible:
            shoot.world_x = x
            shoot.world_y = y
            shoot.visible = True
            return shoot
    return None  # * Pool full — no shot created


# * Load and scale all item sprites into a shared dict keyed by item name
def sprites_func_items(item_width, item_height):
    sprites = {
        "item_sprites": {
            "coin": transform.scale(
                image.load("src\\data\\img\\objects\\coin.png"),
                (item_width, item_height)
            ),

            "banana": transform.scale(
                image.load("src\\data\\img\\objects\\banana.png"),
                (item_width, item_height)
            ),

            "cookie": transform.scale(
                image.load("src\\data\\img\\objects\\cookie.png"),
                (item_width, item_height)
            ),

            "crystal": transform.scale(
                image.load("src\\data\\img\\objects\\crystal.png"),
                (item_width, item_height)
            ),

            "sword": transform.scale(
                image.load("src\\data\\img\\objects\\sword.png"),
                (item_width, item_height)
            )
        }
    }

    return sprites


# * Search a free (invisible) slot in the item pool, configure it and make it visible
def items_pool(pool, name, x, y, health, durability, power=None):
    for item in pool:
        if not item.visible and health > 0:
            item.name = name
            item.item = item.sprites["item_sprites"][name]  # * Swap to the correct sprite
            item.world_x = x
            item.world_y = y
            item.visible = True
            item.spawn_time = time.get_ticks()  # * Start the lifetime countdown
            item.pickup_delay = time.get_ticks() + 500  # * 500ms grace period before the player can pick it up
            item.power = power
            item.health = health
            item.durability = durability
            return item
    return None  # * Pool full — item not spawned


# * Slice a horizontal sprite sheet into individual animation frames and store them in sprites dict
def sprites_func_animals(path, num_sprites, direction, width, height, animal, status, sprites):
    img = image.load(path).convert_alpha()
    sheet_width, sheet_height = img.get_size()

    # * Each cell occupies an equal horizontal slice of the sheet
    cell_width  = sheet_width / num_sprites
    cell_height = sheet_height

    valid_directions = ["right", "up", "down", "left"]
    if direction not in valid_directions:
        raise ValueError(f"Dirección '{direction}' no válida. Usa: {valid_directions}")

    move_frames = []
    for f in range(num_sprites):
        first_rect   = Rect(int(f * cell_width), 0, int(cell_width), cell_height)
        first_sprite = img.subsurface(first_rect)

        # * Trim transparent padding before scaling
        draw_area    = first_sprite.get_bounding_rect()
        final_sprite = first_sprite.subsurface(draw_area)

        move_frames.append(transform.scale(final_sprite, (width, height)))

    # * Nested dict structure: sprites["animal_sprites"][animal][status][direction]
    sprites["animal_sprites"].setdefault(animal, {}).setdefault(status, {})[direction] = move_frames


# * Search a free slot in the animal pool, load its sprites and place it in the world
def animals_pool(pool, name, x, y, width, height, speed, frames):
    for animal in pool:
        if not animal.visible:
            animal.animal = name
            animal.world_x = x
            animal.world_y = y
            animal.width = width
            animal.height = height
            animal.hitbox.width = width
            animal.hitbox.height = height
            animal.speed = speed
            animal.frames = frames
            animal.sprites_dic = {"animal_sprites": {}}  # * Reset before loading new sprites
            animal.load_sprites()
            animal.visible = True
            return animal
    return None  # * Pool full — animal not spawned
