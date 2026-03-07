from pygame import image, transform


def sprites_func(widht_player, height_player):
    sprites = {
        "player": {
            "move": {
                "left": [
                    transform.scale(image.load(f'data\\img\\player\\left_{i}.png'),
                                    (widht_player, height_player)) for i in range(0, 2)
                        ],
                "right":  [
                    transform.scale(image.load(f'data\\img\\player\\right_{i}.png'),
                                    (widht_player, height_player)) for i in range(0, 2)
                        ],
                "up":  [
                    transform.scale(image.load(f'data\\img\\player\\up_{i}.png'),
                                    (widht_player, height_player)) for i in range(0, 2)
                        ],
                "down":  [
                    transform.scale(image.load(f'data\\img\\player\\down_{i}.png'),
                                    (widht_player, height_player)) for i in range(0, 2)
                        ],
                "up_left":  [
                    transform.scale(image.load(f'data\\img\\player\\up_left_{i}.png'),
                                    (widht_player, height_player)) for i in range(0, 2)
                        ],
                "up_right":  [
                    transform.scale(image.load(f'data\\img\\player\\up_right_{i}.png'),
                                    (widht_player, height_player)) for i in range(0, 2)
                        ],
                "down_left":  [
                    transform.scale(image.load(f'data\\img\\player\\down_left_{i}.png'),
                                    (widht_player, height_player)) for i in range(0, 2)
                        ],
                "down_right":  [
                    transform.scale(image.load(f'data\\img\\player\\down_right_{i}.png'),
                                    (widht_player, height_player)) for i in range(0, 2)
                        ]
            },
            "not_move": {
                "left": transform.scale(image.load(f'data\\img\\player\\left_not.png'), (widht_player, height_player)),

                "right": transform.scale(image.load(f'data\\img\\player\\right_not.png'), (widht_player, height_player)),

                "up": transform.scale(image.load(f'data\\img\\player\\up_not.png'), (widht_player, height_player)),

                "down": transform.scale(image.load(f'data\\img\\player\\down_not.png'), (widht_player, height_player)),

                "up_left": transform.scale(image.load(f'data\\img\\player\\up_left_not.png'), (widht_player, height_player)),

                "up_right": transform.scale(image.load(f'data\\img\\player\\up_right_not.png'), (widht_player, height_player)),

                "down_left": transform.scale(image.load(f'data\\img\\player\\down_left_not.png'), (widht_player, height_player)),

                "down_right": transform.scale(image.load(f'data\\img\\player\\down_right_not.png'), (widht_player, height_player))
            }
        }
    }

    return sprites
