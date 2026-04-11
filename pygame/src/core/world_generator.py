import pygame
from opensimplex import OpenSimplex

class World_generator:
    def __init__(self, sed, columns, rows, tile_w, tile_h, scale=0.1):
        self.sed = sed
        self.clmns = columns
        self.rws = rows
        self.tile_w = tile_w
        self.tile_h = tile_h
        self.scale = scale
        self.color = None
        self.map = []
        # * Colours
        self.blue = (30, 100, 200)
        self.yellow = (194, 178, 128)
        self.green = (100, 180, 80)
        self.grey = (150, 150, 150)
        self.black = (0, 0, 0)

    # * out of the loop
    def generate_map(self):
        gen = OpenSimplex(seed=self.sed)

        for row in range(self.rws):
            actual_rw = []
            for clmn in range(self.clmns):
                value = gen.noise2(clmn * self.scale, row * self.scale)
                actual_rw.append(value)
            self.map.append(actual_rw)

    # * Draw called
    def selected_colors(self, value):
        if value < -0.1:
            return self.blue
        elif value < 0.1:
            return self.yellow
        elif value < 0.4:
            return self.green
        else:
            return self.grey

    # * Draw called
    def get_diamond(self, cx, cy):
        return [
            (cx,              cy),
            (cx + self.tile_w // 2, cy + self.tile_h // 2),
            (cx,              cy + self.tile_h),
            (cx - self.tile_w // 2, cy + self.tile_h // 2),
        ]

    # * Inside the loop
    def draw(self, wn, cam_x, cam_y):
        for row in range(self.rws):
            for clmn in range(self.clmns):
                tile_x = (clmn - row) * (self.tile_w // 2)
                tile_y = (clmn + row) * (self.tile_h // 2)

                cx = tile_x - cam_x
                cy = tile_y - cam_y

                color = self.selected_colors(self.map[row][clmn])
                pygame.draw.polygon(wn, color, self.get_diamond(cx, cy))
                pygame.draw.polygon(wn, self.black, self.get_diamond(cx, cy), 1)
