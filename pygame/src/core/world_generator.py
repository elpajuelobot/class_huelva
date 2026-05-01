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
        self.gen = OpenSimplex(seed=self.sed)  # * Noise generator — same seed always produces the same world
        self.tile_w = tile_w
        self.tile_h = tile_h
        self.scale = scale  # * Noise sampling frequency: lower = smoother/larger terrain features
        self.chunks = {}  # * Dict of loaded chunks: {(col, row): {"data": [...], "surface": Surface}}
        self.chunk_queue = []  # * FIFO queue of chunk coords pending generation (processed one per frame)

        # * Load a tile image by index, scale it to match the configured tile size
        def load_tile(index):
            path = f"src\\data\\img\\background\\tiles\\separados\\tile_{index:03d}.png"
            img = pygame.image.load(path).convert_alpha()
            scale_factor = tile_w / 32  # * Source tiles are 32×32px
            new_w = int(32 * scale_factor)
            new_h = int(32 * scale_factor)
            return pygame.transform.scale(img, (new_w, new_h))

        # * Terrain tile sets — indices correspond to the tile atlas layout
        self.tiles_grass = [load_tile(22), load_tile(23), load_tile(24)]  # * Three grass variants for visual variety
        self.tiles_rock  = [load_tile(61)]
        self.tiles_water = [load_tile(i) for i in range(104, 120)]  # * 16 water tiles for shoreline transitions

        # * Lookup table: bitmask string of neighbouring non-water tiles → water tile index
        # * Key format: "NESW" where 1 = neighbour is land, 0 = neighbour is water
        self.water_map = {
            "0000": 0,  # * All neighbours are water (open water)
            "1000": 1,  # * Only North is land
            "0001": 2,  # * Only East is land
            "0100": 3,  # * Only South is land
            "0010": 4,  # * Only West is land
            "1001": 5,  # * North and East are land
            "0110": 6,  # * South and West are land
            "0011": 7,  # * East and West are land
            "1100": 8,  # * North and South are land
            "1111": 9,  # * All neighbours are land (isolated water cell)
            "1101": 10, # * Only West is water
            "0101": 11, # * North and South are land (horizontal strip)
            "1010": 12, # * East and West are land (vertical strip)
            "1110": 13, # * Only East is water
            "1011": 14, # * Only South is water
            "0111": 15, # * Only North is water
        }
        self.tiles_sand = load_tile(0)

        # * Debug / legacy colour palette (kept in case needed for fallback drawing)
        self.blue = (30, 100, 200)
        self.yellow = (194, 178, 128)
        self.green = (100, 180, 80)
        self.grey = (150, 150, 150)
        self.black = (0, 0, 0)

    # * Pre-render an entire chunk into a single Surface — called from process_queue(), not the main loop
    def generate_chunk(self, chunk_clmn, chunk_row):
        chunk_data = []

        # * Surface large enough to hold all tiles in the chunk with isometric overlap
        surface_w = (CHUNK * 2) * (ISO_W // 2)
        surface_h = (CHUNK * 2) * (ISO_H // 2) + self.tile_h * 2
        chunk_surface = pygame.Surface((surface_w, surface_h), pygame.SRCALPHA)

        # * Local origin offsets so tiles are centred inside the surface
        offset_x = surface_w // 2
        offset_y = self.tile_h

        for row in range(CHUNK):
            actual_rw = []
            for clmn in range(CHUNK):
                # * Convert local chunk coords to absolute world tile coords
                global_clmn = chunk_clmn * CHUNK + clmn
                global_row  = chunk_row  * CHUNK + row
                value = self.gen.noise2(global_clmn * self.scale, global_row * self.scale)

                terrain = self.get_terrain(global_clmn, global_row)
                if terrain == "water":
                    # * Build the NESW bitmask by checking each cardinal neighbour
                    north = 1 if self.get_terrain(global_clmn, global_row - 1) != "water" else 0
                    east  = 1 if self.get_terrain(global_clmn + 1, global_row) != "water" else 0
                    south = 1 if self.get_terrain(global_clmn, global_row + 1) != "water" else 0
                    west  = 1 if self.get_terrain(global_clmn - 1, global_row) != "water" else 0

                    neight_key = f"{north}{east}{south}{west}".strip()
                    tile_content = self.tiles_water[self.water_map.get(neight_key, 0)]
                else:
                    tile_content = self.get_tiles(value, global_clmn, global_row)

                actual_rw.append(value)

                # * Isometric screen position relative to the chunk surface origin
                local_x = (clmn - row) * (ISO_W // 2) + offset_x
                local_y = (clmn + row) * (ISO_H // 2)

                chunk_surface.blit(tile_content, (local_x - ISO_W // 2, local_y - ISO_H // 2 + offset_y))

            chunk_data.append(actual_rw)

        return {"data": chunk_data, "surface": chunk_surface}

    # * Add newly visible chunks to the queue and unload chunks that are too far away
    def update_chunks(self, player_tile_clmn, player_tile_row):
        player_chunk_clmn = player_tile_clmn // CHUNK
        player_chunk_row  = player_tile_row  // CHUNK

        # * Enqueue all chunks within CHUNK_DISTANCE that are not already loaded or queued
        for row in range(
                    player_chunk_row - CHUNK_DISTANCE,
                    player_chunk_row + CHUNK_DISTANCE + 1):
            for clmn in range(
                    player_chunk_clmn - CHUNK_DISTANCE,
                    player_chunk_clmn + CHUNK_DISTANCE + 1):
                if (clmn, row) not in self.chunks and (clmn, row) not in self.chunk_queue:
                    self.chunk_queue.append((clmn, row))

        # * Mark chunks beyond CHUNK_DISTANCE + 2 for unloading (the extra 2 gives a hysteresis buffer)
        to_unload = []
        for (clmn, row) in self.chunks:
            if (abs(clmn - player_chunk_clmn) > CHUNK_DISTANCE + 2
                    or abs(row - player_chunk_row) > CHUNK_DISTANCE + 2):
                to_unload.append((clmn, row))
        for key in to_unload:
            del self.chunks[key]

    # * Generate one chunk per frame from the queue to avoid frame spikes
    def process_queue(self):
        if len(self.chunk_queue) > 0:
            clmn, row = self.chunk_queue.pop(0)
            self.chunks[(clmn, row)] = self.generate_chunk(clmn, row)

    # * Return the correct tile image for a non-water cell based on its noise value
    def get_tiles(self, value, global_clmn, global_row):
        if value < -0.1:
            return self.tiles_water[0]
        elif value < 0.1:
            return self.tiles_sand
        elif value < 0.4:
            # * Use a seeded RNG per tile so grass variants are consistent across frames
            rng = random.Random(global_clmn * 1000 + global_row)
            return rng.choice(self.tiles_grass)
        else:
            return self.tiles_rock[0]

    # * Return the terrain type string for any world tile — used for collision and shoreline detection
    # * This recalculates the noise value on the fly so it works even for unloaded chunks
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

    # * Return the four corners of an isometric diamond centred at (cx, cy)
    # * (kept for potential future use with diamond-based hit detection)
    def get_diamond(self, cx, cy):
        return [
            (cx, cy),
            (cx + self.tile_w // 2, cy + self.tile_h // 2),
            (cx, cy + self.tile_h),
            (cx - self.tile_w // 2, cy + self.tile_h // 2),
        ]

    # * Blit all loaded chunk surfaces each frame, sorted back-to-front for correct isometric layering
    def draw(self, wn, cam_x, cam_y):
        # * Sort by col + row so chunks further "into" the screen are drawn first
        chunks_correct_order = sorted(self.chunks.items(), key=lambda item: item[0][0] + item[0][1])

        for (chunk_clmn, chunk_row), chunk in chunks_correct_order:
            # * World-space position of this chunk's top-left tile
            original_clmn = chunk_clmn * CHUNK
            original_row  = chunk_row  * CHUNK

            world_x = (original_clmn - original_row) * (ISO_W // 2)
            world_y = (original_clmn + original_row) * (ISO_H // 2)

            surface_w = chunk["surface"].get_width()
            # * Convert world position to screen position, centering the surface on its origin tile
            sx = world_x - cam_x - surface_w // 2
            sy = world_y - cam_y - self.tile_h

            wn.blit(chunk["surface"], (sx, sy))
