import pygame
from opensimplex import OpenSimplex
from src.core.config import (
    CHUNK, CHUNK_DISTANCE,
    ISO_W, ISO_H
)
import random

class World_generator:
    def __init__(self, sed, tile_w, tile_h, scale=0.1):
        self.sed = sed
        self.gen = OpenSimplex(seed=self.sed)
        self.tile_w = tile_w
        self.tile_h = tile_h
        self.scale = scale
        self.chunks = {}
        self.chunk_queue = []
        def load_tile(index):
            path = f"src\\data\\img\\background\\tiles\\separados\\tile_{index:03d}.png"
            img = pygame.image.load(path).convert_alpha()
            scale_factor = tile_w / 32
            new_w = int(32 * scale_factor)
            new_h = int(32 * scale_factor)
            return pygame.transform.scale(img, (new_w, new_h))

        self.tiles_grass = [load_tile(22), load_tile(23), load_tile(24)]
        self.tiles_rock = [load_tile(61)]
        self.tiles_water = [load_tile(i) for i in range(104, 120)]
        self.water_map = {
            # Derecha, Abajo, Izquierda, Arriba -> 0: Agua // 1: Tierra/Arena/Roca
            "0000": 0,  ## ? Todos son agua
            "1000": 1,  ## ? Derecha no es agua
            "0001": 2,  ## ? Arriba no es agua
            "0100": 3,  ## ? Abajo no es agua
            "0010": 4,  ## ? Izquierda no es agua
            "1001": 5,  ## ? Derecha y arriba
            "0110": 6,  ## ? Abajo y izquierda
            "0011": 7,  ## ? Arriba e izquierda
            "1100": 8,  ## ? Abajo y derecha
            "1111": 9,  ## ? Ninguno es agua
            "1101": 10, ## ? Izquierda solo es agua
            "0101": 11, ## ? Paralelo horizontal no es agua
            "1010": 12, ## ? Paralelo vertical no es agua
            "1110": 13, ## ? Arriba solo es agua. Está mal
            "1011": 14, ## ? Abajo solo es agua REAL
            "0111": 15, ## ? Derecha solo es agua
        }
        self.tiles_sand = load_tile(0)

        # * Colours
        self.blue = (30, 100, 200)
        self.yellow = (194, 178, 128)
        self.green = (100, 180, 80)
        self.grey = (150, 150, 150)
        self.black = (0, 0, 0)

    # * out of the loop
    def generate_chunk(self, chunk_clmn, chunk_row):
        chunk_data = []

        surface_w = (CHUNK * 2) * (ISO_W // 2)
        surface_h = (CHUNK * 2) * (ISO_H // 2) + self.tile_h * 2
        chunk_surface = pygame.Surface((surface_w, surface_h), pygame.SRCALPHA)

        offset_x = surface_w // 2
        offset_y = self.tile_h

        for row in range(CHUNK):
            actual_rw = []
            for clmn in range(CHUNK):
                global_clmn = chunk_clmn * CHUNK + clmn
                global_row = chunk_row * CHUNK + row
                value = self.gen.noise2(global_clmn * self.scale, global_row * self.scale)

                terrain = self.get_terrain(global_clmn, global_row)
                if terrain == "water":
                    north = 1 if self.get_terrain(global_clmn, global_row-1) != "water" else 0
                    east = 1 if self.get_terrain(global_clmn+1, global_row) != "water" else 0
                    south = 1 if self.get_terrain(global_clmn, global_row+1) != "water" else 0
                    west = 1 if self.get_terrain(global_clmn-1, global_row) != "water" else 0

                    neight_key = f"{north}{east}{south}{west}".strip()

                    tile_content = self.tiles_water[self.water_map.get(neight_key, 0)]
                else:
                    tile_content = self.get_tiles(value, global_clmn, global_row)

                actual_rw.append(value)

                local_x = (clmn - row) * (ISO_W // 2) + offset_x
                local_y = (clmn + row) * (ISO_H // 2)

                chunk_surface.blit(tile_content, (local_x - ISO_W // 2, local_y - ISO_H // 2 + offset_y))

            chunk_data.append(actual_rw)

        return {"data": chunk_data, "surface": chunk_surface}

    # * Update the chunks
    def update_chunks(self, player_tile_clmn, player_tile_row):
        player_chunk_clmn = player_tile_clmn // CHUNK
        player_chunk_row = player_tile_row // CHUNK

        for row in range(
                    player_chunk_row - CHUNK_DISTANCE,
                    player_chunk_row + CHUNK_DISTANCE + 1):
            for clmn in range(
                    player_chunk_clmn - CHUNK_DISTANCE,
                    player_chunk_clmn + CHUNK_DISTANCE + 1):
                if (clmn, row) not in self.chunks and (clmn, row) not in self.chunk_queue:
                    self.chunk_queue.append((clmn, row))

        to_unload = []
        for (clmn, row) in self.chunks:
            if (abs(clmn - player_chunk_clmn) > CHUNK_DISTANCE + 2
                    or abs(row - player_chunk_row) > CHUNK_DISTANCE + 2):
                to_unload.append((clmn, row))
        for key in to_unload:
            del self.chunks[key]

    def process_queue(self):
        if len(self.chunk_queue) > 0:
            clmn, row = self.chunk_queue.pop(0)
            self.chunks[(clmn, row)] = self.generate_chunk(clmn, row)

    # * Chunk generator called
    def get_tiles(self, value, global_clmn, global_row):
        if value < -0.1:
            return self.tiles_water[0]
        elif value < 0.1:
            return self.tiles_sand
        elif value < 0.4:
            rng = random.Random(global_clmn * 1000 + global_row)
            return rng.choice(self.tiles_grass)
        else:
            return self.tiles_rock[0]

    # * Chunk generator called
    def get_terrain(self, global_clmn, global_row):
        value = self.gen.noise2(global_clmn * self.scale, global_row * self.scale)
        if value < -0.1:
            return "water"
        elif value < 0.1:
            return "sand"
        elif value < 0.4:
            return "grass"
        else:
            return "rock"

    # * Chunk generator called
    def get_diamond(self, cx, cy):
        return [
            (cx,              cy),
            (cx + self.tile_w // 2, cy + self.tile_h // 2),
            (cx,              cy + self.tile_h),
            (cx - self.tile_w // 2, cy + self.tile_h // 2),
        ]

    # * Inside the loop
    def draw(self, wn, cam_x, cam_y):
        chunks_correct_order = sorted(self.chunks.items(), key=lambda item: item[0][0] + item[0][1])

        for (chunk_clmn, chunk_row), chunk in chunks_correct_order:
            original_clmn = chunk_clmn * CHUNK
            original_row = chunk_row * CHUNK

            world_x = (original_clmn - original_row) * (ISO_W // 2)
            world_y = (original_clmn + original_row) * (ISO_H // 2)

            surface_w = chunk["surface"].get_width()
            sx = world_x - cam_x - surface_w // 2
            sy = world_y - cam_y - self.tile_h

            wn.blit(chunk["surface"], (sx, sy))
