# Imports
from pygame import image, transform, Rect



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
            )
        }
    }

    return sprites
