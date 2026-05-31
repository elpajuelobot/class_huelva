from src.core.entities.sprites_class import Entities
from src.core.settings.config import ISO_H, ISO_W, width_health, height_health
from src.core.system.animations.animations import sprites_func_animals
import pygame
import json
import math
from enum import Enum
import random


# * Animals' states
class AnimalState(Enum):
    IDLE="idle"
    WANDERING="wandering"
    ALERT="alert"
    FLEEING="fleeing"

# * Animals' class
class Animals(Entities):
    # * Information
    BEHAVIOR = {
        "stag":  {"speed": 1, "flee_speed": 3.5, "detect_radius": 200, "flee_radius": 120},
        "wolf":   {"speed": 3.0, "flee_speed": 6.0, "detect_radius": 210, "flee_radius": 130},
    }

    def __init__(self, width, height, x, y, frames, animal, world, visible=True, health=3):
        super().__init__(width=width, height=height, x=x, y=y)
        self.behavior = self.BEHAVIOR.get(
            animal, {"speed": 2.0, "flee_speed": 4.0, "detect_radius": 180, "flee_radius:": 100}
        )
        self.speed = self.behavior["speed"]
        self.flee_speed = self.behavior["flee_speed"]
        self.detect_radius = self.behavior["detect_radius"]
        self.flee_radius = self.behavior["flee_radius"]
        self.pickup_hitbox = pygame.Rect(0, 0, 0, 0)
        self.chunk = None

        self.animal = animal  # * Animal type key, used to look up sprites and JSON paths
        self.sprites_dic = {"animal_sprites": {}}  # * Populated by load_sprites()
        self.anim_count = 0
        self.health = health
        self.initial_health = health
        self.life = True  # * False when health reaches 0; triggers hide on next update
        self.tile_clmn = 0
        self.tile_row = 0
        self.depth = self.tile_clmn + self.tile_row
        self.cam_x = 0
        self.cam_y = 0
        self.world_x = self.x
        self.world_y = self.y
        self.visible = visible
        self.world = world
        self.direction = "SE"

        # * FMS
        self.state = AnimalState.IDLE
        self.state_timer = self._random_idle_time()
        self.target_x = self.world_x
        self.target_y = self.world_y
        self.wander_radius = 300

    # * How many frames the animal is idle
    def _random_idle_time(self):
        return random.randint(60, 240)

    # * Move to a random position
    def _pick_wander_target(self):
        iso_vectors = [
            (1, 0.5),  # ? SE
            (-1, 0.5),  # ? SW
            (-1, -0.5),  # ? NW
            (1, -0.5)  # ? NE
        ]
        for _ in range(10):
            dir_x, dir_y = random.choice(iso_vectors)
            dist = random.uniform(50, self.wander_radius)
            tx = self.world_x + (dir_x * dist)
            ty = self.world_y + (dir_y * dist)

            if self._is_walkable(tx, ty):
                return tx, ty
        return self.world_x, self.world_y


    # * Ask if this tile is grass
    def _is_walkable(self, wx, wy):
        base_y = wy + self.height * 0.9
        tile_clmn = math.floor((wx / (ISO_W / 2) + base_y / (ISO_H / 2)) / 2)
        tile_row  = math.floor((base_y / (ISO_H / 2) - wx / (ISO_W / 2)) / 2)
        return self.world.get_terrain(tile_clmn, tile_row) not in ("water", "void")

    def _distance_to(self, other_x, other_y):
        dx = self.world_x - other_x
        dy = self.world_y - other_y
        return math.sqrt(dx * dx + dy * dy)

    def _get_iso_direction(self, dx, dy):
        angle = math.degrees(math.atan2(dy, dx))
        if 0 <= angle < 90:
            return "SE"
        elif 90 <= angle < 180:
            return "SW"
        elif -180 <= angle < -90:
            return "NW"
        else:
            return "NE"

    def _move_towards(self, tx, ty, speed):
        dx = tx - self.world_x
        dy = ty - self.world_y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < speed:
            self.world_x = tx
            self.world_y = ty
            return True
        self.direction = self._get_iso_direction(dx, dy)
        self.world_x += (dx / dist) * speed
        self.world_y += (dy / dist) * speed
        return False

    def _move_away_from(self, fx, fy, speed):
        dx = self.world_x - fx
        dy = self.world_y - fy

        iso_vectors = [
            (1, 0.5),  # ? SE
            (-1, 0.5),  # ? SW
            (-1, -0.5),  # ? NW
            (1, -0.5)  # ? NE
        ]

        dist = math.sqrt(dx * dx + dy * dy) or 1
        nx = dx / dist
        ny = dy / dist
        best_vector = iso_vectors[0]
        max_dot = -float('inf')

        for vx, vy in iso_vectors:
            v_dist = math.sqrt(vx * vx + vy * vy)
            nvx = vx / v_dist
            nvy = vy / v_dist

            dot = (nx * nvx) + (ny * nvy)
            if dot > max_dot:
                max_dot = dot
                best_vector = (nvx, nvy)

        self.direction = self._get_iso_direction(best_vector[0], best_vector[1])
        next_x = self.world_x + best_vector[0] * speed
        next_y = self.world_y + best_vector[1] * speed

        if self._is_walkable(next_x, next_y):
            self.world_x = next_x
            self.world_y = next_y

    def _update_fms(self, player_x, player_y):
        dist_player = self._distance_to(player_x, player_y)

        # ? Idle
        if self.state == AnimalState.IDLE:
            self.state_timer -= 1
            if dist_player < self.detect_radius:
                self.state = AnimalState.ALERT
                self.state_timer = 60
            elif self.state_timer <= 0:
                self.target_x, self.target_y = self._pick_wander_target()
                self.state = AnimalState.WANDERING

        # ? Wandering
        elif self.state == AnimalState.WANDERING:
            if dist_player < self.detect_radius:
                self.state = AnimalState.ALERT
                self.state_timer = 45
                return
            arrived = self._move_towards(self.target_x, self.target_y, self.speed)
            if arrived:
                self.state = AnimalState.IDLE
                self.state_timer = self._random_idle_time()

        # ? Alert
        elif self.state == AnimalState.ALERT:
            self.state_timer -= 1
            if dist_player < self.flee_radius or self.state_timer <= 0:
                self.state = AnimalState.FLEEING
                self.state_timer = random.randint(120, 300)
            elif dist_player > self.detect_radius * 1.3:
                self.state = AnimalState.IDLE
                self.state_timer = self._random_idle_time()

        # ? Fleeing
        elif self.state == AnimalState.FLEEING:
            self._move_away_from(player_x, player_y, self.flee_speed)
            self.state_timer -= 1
            if dist_player > self.detect_radius * 1.5 and self.state_timer <= 0:
                self.state = AnimalState.IDLE
                self.state_timer = self._random_idle_time()

    # * Load the animal's sprite sheet from the JSON path registry
    def load_sprites(self):
        with open("src\\data\\json\\animals_path.json", "r", encoding="utf-8") as data:
            animals_paths = json.load(data)

        for state in animals_paths[self.animal]:
            for direction in animals_paths[self.animal][state]:
                data2 = animals_paths[self.animal][state][direction]

                path = data2[0]
                frames = data2[1]

                sprites_func_animals(
                    path=path,
                    num_sprites=frames,
                    direction=direction,
                    width=self.width,
                    height=self.height,
                    animal=self.animal,
                    status=state,
                    sprites=self.sprites_dic
                )

    # * Reduce health; mark as dead when it hits zero
    def take_damage(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            self.life = False
            self.visible = False

    # * Update tile position, depth and camera each frame
    def update(self, cam_x, cam_y, player_x, player_y):
        if not self.life:
            self.visible = False  # * Hide the animal one frame after death
        if self.visible:
            self._update_fms(player_x, player_y)
            self.base_y = self.world_y + self.height * 0.9
            self.tile_clmn = math.floor((self.world_x / (ISO_W / 2) + self.base_y / (ISO_H / 2)) / 2)
            self.tile_row  = math.floor((self.base_y / (ISO_H / 2) - self.world_x / (ISO_W / 2)) / 2)

            self.depth = self.tile_clmn + self.tile_row

            self.cam_x = cam_x
            self.cam_y = cam_y

            offset = self.width * 0.3
            self.pickup_hitbox = pygame.Rect(
                (self.world_x - cam_x) + self.width // 2 - offset,
                (self.base_y - cam_y) - (ISO_H // 2),
                offset * 2,
                ISO_H // 2
            )

    # * Draw the animals
    def draw(self, wn):
        if self.visible:
            if self.show_hitbox:
                pygame.draw.rect(wn, (255, 0, 0), self.hitbox, 4)
                pygame.draw.rect(wn, (0, 255, 0), self.pickup_hitbox, 4)
            wn_x = self.world_x - self.cam_x
            wn_y = self.world_y - self.cam_y
            if self.state == AnimalState.IDLE:
                frames = self.sprites_dic["animal_sprites"][self.animal]["idle"][self.direction]
                # * Advance one animation frame every 5 game ticks
                current_frame = frames[self.anim_count // 5 % len(frames)]
                wn.blit(current_frame, (wn_x, wn_y))
                self.anim_count += 1
            elif self.state == AnimalState.FLEEING:
                frames = self.sprites_dic["animal_sprites"][self.animal]["run"][self.direction]
                # * Advance one animation frame every 5 game ticks
                current_frame = frames[self.anim_count // 5 % len(frames)]
                wn.blit(current_frame, (wn_x, wn_y))
                self.anim_count += 1
            elif self.state == AnimalState.WANDERING:
                frames = self.sprites_dic["animal_sprites"][self.animal]["walk"][self.direction]
                # * Advance one animation frame every 5 game ticks
                current_frame = frames[self.anim_count // 5 % len(frames)]
                wn.blit(current_frame, (wn_x, wn_y))
                self.anim_count += 1
            elif self.state == AnimalState.ALERT:
                frames = self.sprites_dic["animal_sprites"][self.animal]["idle"][self.direction]
                # * Advance one animation frame every 5 game ticks
                current_frame = frames[self.anim_count // 5 % len(frames)]
                wn.blit(current_frame, (wn_x, wn_y))
                self.anim_count += 1

            # * Reset counter once a full animation cycle completes
            if self.anim_count >= len(frames) * 5:
                self.anim_count = 0

            self.hitbox.x = wn_x
            self.hitbox.y = wn_y

    # * Draw the animal's health bar directly above it in world space
    def barra_healt(self, wn, x, y):
        if self.health > 0:
            health_x = x - self.cam_x
            health_y = y - self.cam_y
            calculo_barra = int((self.health / self.initial_health) * width_health)
            rectangulo = pygame.Rect(health_x, health_y, calculo_barra, height_health)
            pygame.draw.rect(wn, (255, 0, 100), rectangulo)
        else:
            self.health = 0  # * Clamp to avoid negative health
