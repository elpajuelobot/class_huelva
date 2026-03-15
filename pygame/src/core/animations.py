# Imports
from pygame import image, transform


# * Player's Sprites
def sprites_func_player(widht_player, height_player):
    sprites = {
        "player": {
            "move": {
                "left": [
                    transform.scale(
                        image.load(
                            f'src\\data\\img\\player\\left_{i}.png'
                        ),
                        (widht_player, height_player)) for i in range(0, 2)
                        ],

                "right":  [
                    transform.scale(
                        image.load(
                            f'src\\data\\img\\player\\right_{i}.png'
                        ),
                        (widht_player, height_player)) for i in range(0, 2)
                        ],

                "up":  [
                    transform.scale(
                        image.load(
                            f'src\\data\\img\\player\\up_{i}.png'
                        ),
                        (widht_player, height_player)) for i in range(0, 2)
                        ],

                "down":  [
                    transform.scale(
                        image.load(
                            f'src\\data\\img\\player\\down_{i}.png'
                        ),
                        (widht_player, height_player)) for i in range(0, 2)
                        ],

                "up_left":  [
                    transform.scale(
                        image.load(
                            f'src\\data\\img\\player\\up_left_{i}.png'
                        ),
                        (widht_player, height_player)) for i in range(0, 2)
                        ],

                "up_right":  [
                    transform.scale(
                        image.load(
                            f'src\\data\\img\\player\\up_right_{i}.png'
                        ),
                        (widht_player, height_player)) for i in range(0, 2)
                        ],

                "down_left":  [
                    transform.scale(
                        image.load(
                            f'src\\data\\img\\player\\down_left_{i}.png'
                        ),
                        (widht_player, height_player)) for i in range(0, 2)
                        ],

                "down_right":  [
                    transform.scale(
                        image.load(
                            f'src\\data\\img\\player\\down_right_{i}.png'
                        ),
                        (widht_player, height_player)) for i in range(0, 2)
                        ]
            },

            "not_move": {
                "left": transform.scale(
                    image.load('src\\data\\img\\player\\left_not.png'),
                    (widht_player, height_player)
                ),

                "right": transform.scale(
                    image.load('src\\data\\img\\player\\right_not.png'),
                    (widht_player, height_player)
                ),

                "up": transform.scale(
                    image.load('src\\data\\img\\player\\up_not.png'),
                    (widht_player, height_player)
                ),

                "down": transform.scale(
                    image.load('src\\data\\img\\player\\down_not.png'),
                    (widht_player, height_player)
                ),

                "up_left": transform.scale(
                    image.load('src\\data\\img\\player\\up_left_not.png'),
                    (widht_player, height_player)
                ),

                "up_right": transform.scale(
                    image.load('src\\data\\img\\player\\up_right_not.png'),
                    (widht_player, height_player)
                ),

                "down_left": transform.scale(
                    image.load('src\\data\\img\\player\\down_left_not.png'),
                    (widht_player, height_player)
                ),

                "down_right": transform.scale(
                    image.load('src\\data\\img\\player\\down_right_not.png'),
                    (widht_player, height_player)
                )
            }
        }
    }

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
