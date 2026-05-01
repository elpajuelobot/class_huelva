# Imports
import pygame
from src.core.animations import (
    sprites_func_player,
    sprites_func_shot,
    sprites_func_items,
    sprites_func_animals
)
from src.core.config import (
    shot_width,
    shot_height,
    shot_cooldown,
    lifetime,
    width_health,
    height_health,
    width_health_player,
    height_health_player,
    grey_red,
    red_dark,
    water_attack_delay,
    regenerate_bubbles,
    ISO_W,
    ISO_H,
    purple
)
import json
import math


# * Base class for all entities in the game (player, animals, items, projectiles)
class Entities(pygame.sprite.Sprite):
    def __init__(self, *groups, width, height, x, y):
        super().__init__(*groups)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        # * Collision rectangle, starts at spawn position
        self.hitbox = pygame.Rect(
            self.x, self.y,
            self.width, self.height
        )
        self.show_hitbox = False  # * Toggle with F3 to debug collisions
        self.visible = True
        self.health_bar = True  # * Whether to draw the health bar above this entity


class Player(Entities):
    def __init__(self, *groups, width, height, x, y, speed_player, sprites_player, wn_width, wn_height, inventory, health, bubbles):
        super().__init__(*groups, width=width, height=height, x=x, y=y)
        # ? Player configuration
        self.name = "Scot"  # * Player's name
        self.speed = speed_player  # * Player's speed (changes when in water)
        self.world_x = x  # * Player's x axis in the isometric world
        self.world_y = y  # * Player's y axis in the isometric world
        # ? Sprites
        self.sprites = sprites_func_player(self.width, self.height)  # * Upload the player's sprites
        self.sprites_dict = self.sprites[sprites_player]  # * Player's sprites dict (move, not_move, health)
        self.anim_count = 0  # * Counter for the animations' frames
        # ? Player's health
        self.health = health  # * Player's actual health
        self.initial_health = health  # * Player's initial health (used to calculate the health bar ratio)
        self.player_core = self.sprites_dict["health"]["core"]  # * Heart icon shown on the health bar
        self.player_bubble = self.sprites_dict["health"]["bubble"]  # * Bubble icon shown when underwater
        self.bubbles = bubbles  # * Current bubble count (oxygen while in water)
        self.initial_bubbles = bubbles  # * Max bubbles (used to cap regeneration)
        self.last_bubble_time = 0  # * Timestamp of last bubble regeneration
        self.oxigen = True  # * Verify if the player have or no oxigen
        # ? States and moving
        self.player_state = "right"  # * Current facing direction, used to pick the right sprite
        self.is_move = False  # * True while the player is pressing a movement key
        self.terrain = None  # * Current terrain type under the player ("water", "sand", "grass", "rock")
        # ? Inventory
        self.inventory = inventory  # * Reference to the Inventory instance
        # ? Projectiles
        self.is_shot = False  # * True while the player is shooting (unused, reserved for future)
        self.projectiles = []  # * Active projectile list (Fire instances)
        self.can_create_shot = False  # * Reserved for future shot unlock logic
        self.last_shot_time = 0  # * Timestamp of last shot fired, used for cooldown
        self.shot_count_down = shot_cooldown  # * Minimum ms between shots
        # ? World Map
        self.tile_clmn = 0  # * Isometric column the player is currently on
        self.tile_row = 0  # * Isometric row the player is currently on
        self.depth = self.tile_clmn + self.tile_row  # * Draw order: higher depth = drawn later (on top)
        self.wn_width = wn_width  # * Window width, used to center the player sprite on screen
        self.wn_height = wn_height  # * Window height, used to center the player sprite on screen
        # ? Entities
        self.entities = None  # * Reference to the active entities list, set each frame in update()
        # ? Water
        self.last_water_damage_time = 0  # * Timestamp of last water damage tick

    # * Update de inventory
    def update_inventory(self, event, items):
        self.inventory.update(
            event,
            items,
            self.world_x,
            self.world_y
        )

    # * Converts a world-space point (px, py) to isometric tile coords and returns its terrain type
    def get_tile_terrain(self, px, py, world):
        clmn = math.floor((px / (ISO_W / 2) + py / (ISO_H / 2)) / 2)
        row = math.floor((py / (ISO_H / 2) - px / (ISO_W / 2)) / 2)
        return world.get_terrain(clmn, row)

    # * Update function for move the player
    def update(self, keys_pressed, items, cam_x, cam_y, entities, world):
        self.entities = entities
        delta_x = 0
        delta_y = 0
        # * Vertical midpoint of the sprite — the visual "foot" contact point in isometric projection
        self.base_y = self.world_y + self.height * 0.5
        # * Horizontal offset for the lateral terrain sample points (~30% of sprite width)
        offset = self.width * 0.3
        center_point = (self.world_x,          self.base_y)
        left_point   = (self.world_x - offset, self.base_y)
        right_point  = (self.world_x + offset, self.base_y)
        self.is_move = False

        # * Sample terrain at three points and vote: 2 out of 3 water → player is in water
        terrains = [
            self.get_tile_terrain(*center_point, world=world),
            self.get_tile_terrain(*left_point,   world=world),
            self.get_tile_terrain(*right_point,  world=world)
        ]

        water_count = terrains.count("water")
        self.terrain = "water" if water_count >= 2 else terrains[0]

        # * Tile position using only the center point (used for depth sorting and chunk loading)
        self.tile_clmn = math.floor((self.world_x / (ISO_W / 2) + self.base_y / (ISO_H / 2)) / 2)
        self.tile_row  = math.floor((self.base_y / (ISO_H / 2) - self.world_x / (ISO_W / 2)) / 2)

        # ? Horizontal axis configuration
        if keys_pressed[pygame.K_w]:
            delta_y -= self.speed
            self.is_move = True
        elif keys_pressed[pygame.K_s]:
            delta_y += self.speed
            self.is_move = True

        # ? Vertical axis configuration
        if keys_pressed[pygame.K_a]:
            delta_x -= self.speed
            self.is_move = True
        elif keys_pressed[pygame.K_d]:
            delta_x += self.speed
            self.is_move = True

        # ? Convert screen-space deltas to isometric world-space movement
        iso_x = delta_x - delta_y
        iso_y = (delta_x + delta_y) / 2

        # * Normalize diagonal movement so it doesn't go faster than cardinal
        length = (iso_x**2 + iso_y**2) ** 0.5
        if length > 0:
            iso_x = (iso_x / length) * self.speed
            iso_y = (iso_y / length) * self.speed

        # * Apply water effects: slow movement and drain bubbles/health on a timer
        current_time_water = pygame.time.get_ticks()
        if self.terrain == "water":
            self.speed = 1.5
            if current_time_water - self.last_water_damage_time > water_attack_delay:
                if self.bubbles > 0:
                    self.oxigen = True
                    self.bubbles -= 1
                elif self.bubbles <= 0:
                    self.oxigen = False
                    self.health -= 1
                self.last_water_damage_time = current_time_water
        else:
            self.oxigen = True
            self.speed = 3

        self.world_x += iso_x
        self.world_y += iso_y

        # * Subtract 0.5 so the player renders just in front of the tile it stands on
        self.depth = (self.tile_clmn + self.tile_row) - 0.5

        # ? Update player_state
        if delta_y < 0:
            self.player_state = "up_right"
        elif delta_y > 0:
            self.player_state = "down_left"
        elif delta_x < 0:
            self.player_state = "up_left"
        elif delta_x > 0:
            self.player_state = "down_right"

        # ? Shot a fire ball
        if keys_pressed[pygame.K_SPACE]:
            # * Get the time of the shot
            current_time = pygame.time.get_ticks()

            # * Compare the time of the shot with the delay
            if current_time - self.last_shot_time > self.shot_count_down:
                self.last_shot_time = current_time

                # * Create the projectile
                if len(self.projectiles) < 10:
                    self.projectiles.append(Fire(
                        width=shot_width,
                        height=shot_height,
                        x=self.world_x,
                        y=self.world_y,
                        speed=8,
                        shot_sprite="shot_sprite",
                        player_state=self.player_state
                    ))

        # ? Update all the projectiles
        for shot in list(self.projectiles):
            shot.update(cam_x, cam_y)
            remove = False
            # * If the projectile is out of the window bounds, mark it for removal
            if (shot.hitbox.x > 800 or shot.hitbox.x < -80
                    or
                    shot.hitbox.y > 600 or shot.hitbox.y < -80):
                remove = True

            # * Check collision with each entity; on hit, deal damage and remove the shot
            if not remove:
                for entity in self.entities:
                    if entity.life and shot.hitbox.colliderect(entity.hitbox):
                        entity.take_damage(damage=3)
                        remove = True
                        break

            if remove and shot in self.projectiles:
                self.projectiles.remove(shot)

        # ? Add item in the inventory
        current_time = pygame.time.get_ticks()
        for item in items:
            if (
                    item.visible
                    and
                    current_time > item.pickup_delay  # * Prevents picking up items immediately after dropping them
                    and
                    self.hitbox.colliderect(item.hitbox)):
                if self.inventory.put_images(item.name, item.durability, item.health):
                    item.visible = False

    # * Draw function for draw the player in the window
    def draw(self, wn):
        if self.show_hitbox:
            pygame.draw.rect(wn, (255, 0, 0), self.hitbox, 4)

        # * Always draw the player centered on screen (camera follows player)
        wn_x = self.wn_width  // 2 - self.width  // 2
        wn_y = self.wn_height // 2 - self.height // 2

        if self.is_move:
            # * Cycle through 4 animation frames (0→1→2→1) at 8 ticks per frame
            frame_index = (self.anim_count // 8) % 4
            current_frame = self.sprites_dict["move"][self.player_state][frame_index]
            wn.blit(current_frame, (wn_x, wn_y))
            self.anim_count += 1
        elif not self.is_move:
            # * Reset animation counter and show the idle frame for the current direction
            self.anim_count = 0
            current_frame = self.sprites_dict["not_move"][self.player_state]
            wn.blit(current_frame, (wn_x, wn_y))
        else:
            print("\n\n  FUCK YOU!!!!  \n\n")

        # ? Draw all the projectiles
        for shot in list(self.projectiles):
            shot.draw(wn)

        self.hitbox.x = wn_x
        self.hitbox.y = wn_y

    # * Melee attack: deals damage if the player has a sword equipped and clicks on an entity's hitbox
    def attack(self, events):
        if events.type == pygame.MOUSEBUTTONDOWN and events.button == 1:
            for entity in self.entities:
                    if entity.life:
                        if self.hitbox.colliderect(entity.hitbox) and self.inventory.actual_item == "sword":
                            self.inventory.use_item()
                            entity.take_damage()
                            break

    # * Draw the player health bar at the given screen position
    def barra_healt(self, wn, x, y):
        health_x = x
        health_y = y
        if self.oxigen:
            blod_color = red_dark
        else:
            blod_color = purple
        calculo_barra = int((self.health / self.initial_health) * width_health_player)
        borde = pygame.Rect(health_x, health_y, width_health_player, height_health_player)
        rectangulo = pygame.Rect(health_x, health_y, calculo_barra, height_health_player)
        pygame.draw.rect(wn, blod_color, rectangulo)  # * Filled portion (current health)
        pygame.draw.rect(wn, grey_red, borde, 3)  # * Border of the full bar
        wn.blit(self.player_core, (health_x + 15, health_y + 2))  # * Heart icon
        if self.health <= 0:
            self.health = 0  # * Clamp to avoid negative health

    # * Draw the bubble bar (oxygen) — only visible while in water; regenerates one bubble per interval on land
    def bubbles_bar(self, wn, x, y):
        if self.bubbles >= 0:
            if self.terrain == "water":
                for i in range(self.bubbles):
                    wn.blit(self.player_bubble, (x, y))
                    x += self.player_bubble.get_width() + 10  # * Space bubbles horizontally
            else:
                current_time_bubble = pygame.time.get_ticks()
                if (
                        self.bubbles < self.initial_bubbles and
                        current_time_bubble - self.last_bubble_time > regenerate_bubbles
                        ):
                    self.bubbles += 1
                    self.last_bubble_time = current_time_bubble
        else:
            self.bubbles = 0  # * Clamp to avoid negative bubbles


# * Fire balls' class
class Fire(Entities):
    # * __init__
    def __init__(self, *groups, width, height, x, y, speed, shot_sprite, player_state):
        super().__init__(*groups, width=width, height=height, x=x, y=y)
        self.sprites = sprites_func_shot(self.width, self.height)
        self.speed = speed
        self.shot = self.sprites[shot_sprite]["shot"]  # * Projectile sprite image
        self.player_state = player_state  # * Direction inherited from the player at the moment of firing
        self.world_x = x
        self.world_y = y
        self.cam_x = 0
        self.cam_y = 0

    # * Move the projectile each frame and update its screen-space hitbox
    def update(self, cam_x, cam_y):
        # * Map player state to a screen-space delta, then convert to isometric movement
        directions = {
            "up_right":   (0,          -self.speed),
            "up_left":    (-self.speed, 0),
            "down_right": (self.speed,  0),
            "down_left":  (0,           self.speed)
        }

        delta_x, delta_y = directions.get(self.player_state, (0, 0))
        iso_x = delta_x - delta_y
        iso_y = (delta_x + delta_y) / 2

        self.world_x += iso_x
        self.world_y += iso_y

        # * Convert world position to screen position using the camera offset
        self.hitbox.x = self.world_x - cam_x
        self.hitbox.y = self.world_y - cam_y

    # * Draw the fire ball
    def draw(self, wn):
        if self.visible:
            wn.blit(self.shot, self.hitbox)
            if self.show_hitbox:
                pygame.draw.rect(wn, (255, 0, 0), self.hitbox, 4)


# * Items' class
class Items(Entities):
    # * __init__
    def __init__(self, *groups, width, height, x, y, name_item, durability, item_power=None):
        super().__init__(*groups, width=width, height=height, x=x, y=y)
        self.sprites = sprites_func_items(self.width, self.height)
        self.name = name_item
        self.item = self.sprites["item_sprites"][self.name]  # * Item sprite image
        self.world_x = x
        self.world_y = y
        self.spawn_time = 0  # * Tick when this item became visible (used for lifetime expiry)
        self.lifetime = lifetime # * 60*10^4ms (1 min) — item disappears after this
        self.pickup_delay = 0  # * Tick before which the player cannot pick up this item
        self.power = item_power  # * Optional stat bonus (reserved for future use)
        self.durability = durability  # * Max uses before the item breaks
        self.health = durability  # * Current uses remaining
        self.tile_clmn = 0
        self.tile_row = 0
        self.depth = self.tile_clmn + self.tile_row  # * Draw order
        self.health_bar = False  # * Items don't show a health bar in the world
        self.cam_x = 0
        self.cam_y = 0

    # * Recalculate tile position and depth each frame (items can be dropped anywhere)
    def update(self, cam_x, cam_y):
        if self.visible:
            self.base_y = self.world_y + self.height * 0.5
            self.tile_clmn = math.floor((self.world_x / (ISO_W / 2) + self.base_y / (ISO_H / 2)) / 2)
            self.tile_row  = math.floor((self.base_y / (ISO_H / 2) - self.world_x / (ISO_W / 2)) / 2)

            self.depth = self.tile_clmn + self.tile_row

            self.cam_x = cam_x
            self.cam_y = cam_y

    # * Draw the Items
    def draw(self, wn):
        if self.visible:
            if self.show_hitbox:
                pygame.draw.rect(wn, (255, 0, 0), self.hitbox, 4)
            wn_x = self.world_x - self.cam_x
            wn_y = self.world_y - self.cam_y
            wn.blit(self.item, (wn_x, wn_y))
            # * Keep hitbox in sync with screen position for pickup collision detection
            self.hitbox.x = wn_x
            self.hitbox.y = wn_y


# * Animals' class
class Animals(Entities):
    def __init__(self, width, height, x, y, speed, frames, animal, visible=True, health=3):
        super().__init__(width=width, height=height, x=x, y=y)
        self.speed = speed
        self.frames = frames  # * Total number of animation frames in the sprite sheet
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

    # * Load the animal's sprite sheet from the JSON path registry
    def load_sprites(self):
        with open("src\\data\\json\\animals_path.json", "r", encoding="utf-8") as data:
            self.animals_paths = json.load(data)
        sprites_func_animals(
            self.animals_paths[self.animal]["idle"]["down"],
            self.frames, "down", self.width, self.height,
            self.animal, "idle", self.sprites_dic
        )

    # * Reduce health; mark as dead when it hits zero
    def take_damage(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            self.life = False

    # * Update tile position, depth and camera each frame
    def update(self, cam_x, cam_y):
        if not self.life:
            self.visible = False  # * Hide the animal one frame after death
        if self.visible:
            self.base_y = self.world_y + self.height * 0.5
            self.tile_clmn = math.floor((self.world_x / (ISO_W / 2) + self.base_y / (ISO_H / 2)) / 2)
            self.tile_row  = math.floor((self.base_y / (ISO_H / 2) - self.world_x / (ISO_W / 2)) / 2)

            self.depth = self.tile_clmn + self.tile_row

            self.cam_x = cam_x
            self.cam_y = cam_y

    def draw(self, wn):
        if self.visible:
            if self.show_hitbox:
                pygame.draw.rect(wn, (255, 0, 0), self.hitbox, 4)
            wn_x = self.world_x - self.cam_x
            wn_y = self.world_y - self.cam_y
            frames = self.sprites_dic["animal_sprites"][self.animal]["idle"]["down"]
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
