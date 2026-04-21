# Imports
from pygame import image, transform, Rect, time



def sprites_func_player(width_player, height_player):
    imagen_completa = image.load("src\\data\\img\\player\\player_Completo.png").convert_alpha()
    hoja_ancho, hoja_alto = imagen_completa.get_size()

    f_ancho_orig = hoja_ancho / 8
    f_alto_orig = hoja_alto / 3

    directions = ["up", "up_right", "right", "down_right", "down", "down_left", "left", "up_left"]
    sprites = {"player": {"move": {}, "not_move": {}}}

    for c, dir_name in enumerate(directions):
        move_frames = []
        for f in [0, 1, 2, 1]: 
            rect_bruto = Rect(int(c * f_ancho_orig), int(f * f_alto_orig), int(f_ancho_orig), int(f_alto_orig))
            sprite_sucio = imagen_completa.subsurface(rect_bruto)

            area_dibujo = sprite_sucio.get_bounding_rect()
            sprite_limpio = sprite_sucio.subsurface(area_dibujo)

            move_frames.append(transform.scale(sprite_limpio, (width_player, height_player)))

        sprites["player"]["move"][dir_name] = move_frames

        rect_quieto = Rect(int(c * f_ancho_orig), int(1 * f_alto_orig), int(f_ancho_orig), int(f_alto_orig))
        sprite_q_sucio = imagen_completa.subsurface(rect_quieto)
        area_q = sprite_q_sucio.get_bounding_rect()
        sprite_q_limpio = sprite_q_sucio.subsurface(area_q)

        sprites["player"]["not_move"][dir_name] = transform.scale(sprite_q_limpio, (width_player, height_player))

    return sprites


# * Shots' Sprites
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


# * Items' Sprites
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


# * Search a free space in the pool to draw the item in the window
def items_pool(pool, name, x, y, durability, power=None):
    for item in pool:
        if not item.visible and durability > 0:
            item.name = name
            item.item = item.sprites["item_sprites"][name]
            item.world_x = x
            item.world_y = y
            item.visible = True
            item.spawn_time = time.get_ticks()
            item.pickup_delay = time.get_ticks() + 500
            item.power = power
            item.durability = durability
            return item
    return None


# * Animals' sprites
def sprites_func_animals(path, num_sprites, direction, width, height, animal, status, sprites):
    img = image.load(path).convert_alpha()
    sheet_width, sheet_height = img.get_size()

    cell_width = sheet_width / num_sprites
    cell_height = sheet_height

    valid_directions = ["right", "up", "down", "left"]
    if direction not in valid_directions:
        raise ValueError(f"Dirección '{direction}' no válida. Usa: {valid_directions}")

    move_frames = []
    for f in range(num_sprites):
        first_rect = Rect(int(f * cell_width), 0, int(cell_width), cell_height)
        first_sprite = img.subsurface(first_rect)

        draw_area = first_sprite.get_bounding_rect()
        final_sprite = first_sprite.subsurface(draw_area)

        move_frames.append(transform.scale(final_sprite, (width, height)))

    sprites["animal_sprites"].setdefault(animal, {}).setdefault(status, {})[direction] = move_frames


# * Search a free space in the pool to draw the animal in the window
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
            animal.sprites_dic = {"animal_sprites": {}}
            animal.load_sprites()
            animal.visible = True
            return animal
    return None
