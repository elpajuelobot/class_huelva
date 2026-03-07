from pygame import Rect, key, K_s, K_d, K_a, K_w, K_e, K_SPACE, time, draw
from variables import config
from animaciones import *
import math
from enum import Enum
from cinematicas.cinematicas import reproducir_cinematica

#todo: Clase player
class PlayerState(Enum):
    IDLE = "idle"
    WALKING = "walking"
    JUMPING = "jumping"
    ATTACKING = "attacking"
    HURT = "hurt"
    DEAD = "dead"
    CROUCH = "crouch"


class Player:
    def __init__(self, x_ply, y_ply, health, max_health):
        #TODO: Posición y movimiento
        self.x = x_ply
        self.y = y_ply
        self.base_y = y_ply
        self.facing_right = True
        self.crouch = False
        self.crouch_walk = False
        self.walk_count = 0
        self.crouch_count = 0
        self.dx = 0

        #TODO: Salto
        self.jump_anim_count = 0
        self.dy = 0
        self.gravity = 1.0
        self.jump_strength = -12
        self.on_ground = False

        #TODO: Ataque
        self.attack_anim_count = 0
        self.attack_damage_applied = False
        self.current_attack_frames = []

        #TODO: Estado y salud
        self.health = health
        self.max_health = max_health
        self.state = PlayerState.IDLE
        self.death_count = 0
        self.death_timer = 0

        #TODO: Dimensiones
        self.widht_player = 35
        self.height_player = 65
        self.hitbox_player = Rect(self.x, self.y, self.widht_player, self.height_player)

    def update(self, keys_pressed, moused_pressed, can_move, last_key, collision_rects, enemy=None):
        last_key = key.name(last_key)
        if not can_move:
            return

        if self.health <= 0 and self.state != PlayerState.DEAD:
            self.state = PlayerState.DEAD
            self.death_count = 0

        if self.state == PlayerState.DEAD:
            return

        #TODO: Movimiento horizontal
        self.dx = 0
        is_moving = False

        if keys_pressed[K_s] and keys_pressed[K_d] and self.hitbox_player.x < 995:
            self.dx = config.speed_player
            self.crouch = True
            self.crouch_walk = True
            self.facing_right = True
            is_moving = True

        elif keys_pressed[K_s] and keys_pressed[K_a] and self.hitbox_player.x > 3:
            self.dx = -config.speed_player
            self.crouch = True
            self.crouch_walk = True
            self.facing_right = False
            is_moving = True

        elif keys_pressed[K_s]:
            self.crouch = True
            self.crouch_walk = False
            is_moving = False

        elif keys_pressed[K_w]:
            self.crouch = False
            self.crouch_walk = False
            is_moving = False

        elif keys_pressed[K_d] and self.hitbox_player.x < 995:
            self.dx = config.speed_player
            self.crouch = False
            self.crouch_walk = False
            self.facing_right = True
            is_moving = True

        elif keys_pressed[K_a] and self.hitbox_player.x > 3:
            self.dx = -config.speed_player
            self.crouch = False
            self.crouch_walk = False
            self.facing_right = False
            is_moving = True

        #TODO: Hitbox del jugador
        old_bottom = self.hitbox_player.bottom

        if self.crouch:
            current_height = int(self.height_player * 0.5)
            self.hitbox_player.height = current_height
        else:
            self.hitbox_player.height = self.height_player

        self.hitbox_player.bottom = old_bottom

        #TODO: Lógica de salto y gravedad
        self.dy += self.gravity

        if keys_pressed[K_SPACE] and self.on_ground:
            self.dy = self.jump_strength
            self.on_ground = False
            self.state = PlayerState.JUMPING

        #TODO: Detección de colisiones verticales y horizontales
        #! Horizontales
        self.hitbox_player.x += self.dx
        for rect in collision_rects:
            if self.hitbox_player.colliderect(rect):
                if self.dx > 0:
                    self.hitbox_player.right = rect.left
                if self.dx < 0:
                    self.hitbox_player.left = rect.right

                if self.on_ground:
                    self.hitbox_player.y -= 10
                    self.dy = 0

        #! Verticales
        self.hitbox_player.y += self.dy
        self.on_ground = False
        for rect in collision_rects:
            if self.hitbox_player.colliderect(rect):
                if self.dy > 0:
                    self.hitbox_player.bottom = rect.top
                    self.dy = 0
                    self.on_ground = True

                    if self.state == PlayerState.JUMPING:
                        self.state = PlayerState.IDLE

                if self.dy < 0:
                    self.hitbox_player.top = rect.bottom
                    self.dy = 0

        #! Transiciones de estado
        #TODO: Transición a atacar
        if self.state in [PlayerState.IDLE, PlayerState.WALKING] and moused_pressed:
            self.state = PlayerState.ATTACKING
            self.attack_anim_count = 0
            self.attack_damage_applied = False

            #! Elegir tipo de ataque
            if self.facing_right:
                self.current_attack_frames = attack_right_combo_path
            else:
                self.current_attack_frames = attack_left_combo_path

        #TODO: Si está atacando
        elif self.state == PlayerState.ATTACKING:
            self.attack_anim_count += 1

            #! Aplicar daño
            if self.attack_anim_count // 5 >= len(self.current_attack_frames) // 2 and not self.attack_damage_applied:
                if enemy:
                    self.check_collision_enemy(enemy)
                self.attack_damage_applied = True

            #! Una vez acabada
            if self.attack_anim_count >= len(self.current_attack_frames) * 5:
                self.state = PlayerState.IDLE

        #TODO: Si está en el suelo
        elif self.state in [PlayerState.IDLE, PlayerState.WALKING, PlayerState.CROUCH]:
            if is_moving:
                self.state = PlayerState.WALKING
            elif self.crouch:
                self.state = PlayerState.CROUCH
            else:
                self.state = PlayerState.IDLE
            self.walk_count += 1

        self.x = self.hitbox_player.x
        self.y = self.hitbox_player.y

    def draw(self, wn):
        #draw.rect(wn, (255, 0, 0), self.hitbox_player, 2)

        #TODO: Animación de salto
        if self.state == PlayerState.JUMPING:
            self.jump_anim_count += 1
            if self.facing_right:
                anim_list = jump_right_path
            else:
                anim_list = jump_left_path

            #! Dibujar animación de salto
            #?wn.blit(anim_list[self.jump_anim_count // 3 % len(anim_list)], (self.x, self.y))
            current_frame = transform.scale(anim_list[self.jump_anim_count // 3 % len(anim_list)], (self.widht_player, self.height_player))
            wn.blit(current_frame, self.hitbox_player.topleft)

        #TODO: Animación de ataque
        elif self.state == PlayerState.ATTACKING:
            anim_list = self.current_attack_frames
            #! Dibujar animación de ataque
            #?wn.blit(anim_list[self.attack_anim_count // 5 % len(anim_list)], (self.x, self.y))
            current_frame = transform.scale(anim_list[self.attack_anim_count // 5 % len(anim_list)], (self.widht_player, self.height_player))
            wn.blit(current_frame, self.hitbox_player.topleft)

        #TODO: Animación de momiviento
        elif self.state == PlayerState.WALKING and not self.crouch:

            if self.facing_right and not self.crouch:
                anim_list = walk_right_path
            elif not self.facing_right and not self.crouch:
                anim_list = walk_left_path

            #! Dibujar animación de movimiento
            #?wn.blit(anim_list[self.walk_count // 2 % len(anim_list)], (self.x, self.y))
            current_frame = transform.scale(anim_list[self.walk_count // 2 % len(anim_list)], (self.widht_player, self.height_player))
            wn.blit(current_frame, self.hitbox_player.topleft)

        #TODO: Animación cuando está parado
        elif self.state == PlayerState.IDLE:
            if self.facing_right:
                anim_list = stand_right
            else:
                anim_list = stand_left

            #! Dibujar animación de cuando está parado
            #?wn.blit(anim_list[self.walk_count // 5 % len(anim_list)], (self.x, self.y))
            current_frame = transform.scale(anim_list[self.walk_count // 5 % len(anim_list)], (self.widht_player, self.height_player))
            wn.blit(current_frame, self.hitbox_player.topleft)

        #TODO: Animación de muerte
        elif self.state == PlayerState.DEAD:
            self.widht_player = 65
            self.height_player = 35
            self.y = 676

            if self.death_count < len(dead_path) * 5:
                if config.delta_x == 1:
                    #?wn.blit(dead_path[self.death_count // 5 % len(dead_path)], (self.x, self.y))
                    current_frame = transform.scale(dead_path[self.death_count // 5 % len(dead_path)], (self.widht_player, self.height_player))
                else:
                    #?wn.blit(dead_left_path[self.death_count // 5 % len(dead_left_path)], (self.x, self.y))
                    current_frame = transform.scale(dead_left_path[self.death_count // 5 % len(dead_left_path)], (self.widht_player, self.height_player))

                wn.blit(current_frame, self.hitbox_player.topleft)
                self.death_count += 1

            else:
                if self.death_timer == 0:
                    self.death_timer = time.get_ticks()
                if config.delta_x == 1:
                    wn.blit(dead_path[-1], (self.x, self.y))
                else:
                    wn.blit(dead_left_path[-1], (self.x, self.y))

                if time.get_ticks() - self.death_timer > 3000:
                    pass

        #TODO: Animación de agachado moviéndose
        elif self.state == PlayerState.WALKING and self.crouch and self.crouch_walk:
            if self.facing_right:
                anim_list = crouchWalk_right
            else:
                anim_list = crouchWalk_left

            current_width = self.widht_player
            current_height = int(self.height_player * 0.5)

            #! Dibujar animación de movimiento agachado
            #?wn.blit(anim_list[self.walk_count // 2 % len(anim_list)], (self.x, self.y))
            current_frame = transform.scale(anim_list[self.walk_count // 2 % len(anim_list)], (current_width, current_height))
            wn.blit(current_frame, self.hitbox_player.topleft)

        #TODO: Animación de agachado
        elif self.state == PlayerState.CROUCH:
            if self.facing_right:
                anim_list = crouch_right
            else:
                anim_list = crouch_left

            current_width = self.widht_player
            current_height = int(self.height_player * 0.5)

            #?wn.blit(anim_list, (self.x, self.y))
            current_frame = transform.scale(anim_list, (current_width, current_height))
            wn.blit(current_frame, self.hitbox_player.topleft)

    def barra_healt(self, wn, x, y):
        calculo_barra = int((self.health / self.max_health) * config.widht_healt)
        borde = Rect(x, y, config.widht_healt, config.height_healt)
        rectangulo = Rect(x, y, calculo_barra, config.height_healt)
        draw.rect(wn, (255, 0, 255), rectangulo)
        draw.rect(wn, (0, 0, 255), borde, 3)
        text_healt = config.fuente.render(f"Vida: {self.health}", True, config.text_color)
        wn.blit(text_healt, (6, 7))
        if self.health <= 0:
            self.health = 0

    def check_collision_enemy(self, enemy):
        if self.hitbox_player.colliderect(enemy.hitbox_enemy):
            enemy.health -= 4
            enemy.health = max(enemy.health, 0)

    def set_size(self, widht, height):
        print(f"\nwidht_player: {self.widht_player} | height_player: {self.height_player}")
        self.widht_player = widht
        self.height_player = height
        print(f"\nx: {self.x} | y: {self.y}")
        self.hitbox_player = Rect(self.x, self.y, self.widht_player, self.height_player)
        print(f"\nwidht_player: {self.widht_player} | height_player: {self.height_player}")

#todo: Clase enemy
class Villain:

    MOVE_GROUND = 0
    MODE_LEVITATE = 1
    MODE_FLY = 2

    def __init__(self, health, max_health, speed, animation_paths, can_shoot=False, movement_mode=MOVE_GROUND, levitate_height=50, fly_speed_y=2):
        # Configuración principal
        self.x = config.x_enemy
        self.y = config.y_enemy
        self.hitbox_enemy = Rect(self.x, self.y, config.width_enemy, config.height_enemy)
        self.animations = animation_paths
        self.standing = self.animations['idle_right']  # Imagen de pie por defecto
        self.walk_count = 0
        self.moving_right = False
        self.moving_left = False
        self.is_attack = False
        self.attack_count = 0
        self.health = health
        self.max_health = max_health
        self.dead_count = 0
        self.is_dead = False
        self.visible = True
        self.is_stand = False
        self.num_hurt = 4
        self.speed = speed
        self.direction = 1
        self.can_create_prj = False

        # Disparo
        self.can_shoot = can_shoot
        self.is_shooting = False
        self.shoot_cooldown = config.shoot_cooldown
        self.last_shoot_time = 0
        self.projectiles = []
        self.prj_speed = config.prj_speed
        self.prj_damage = config.prj_damage

        # Modo de movimiento {Levitación//vuelo//correr}
        self.mv_mode = movement_mode
        self.lvt_height = levitate_height
        self.fly_speed_y = fly_speed_y
        self.target_y = self.y
        self.ground_y = config.y_enemy

        if self.mv_mode == self.MODE_LEVITATE:
            self.y = self.ground_y - self.lvt_height

    def move_towards_player(self, player):
        if player.health > 0 and self.health > 0 and config.show_inventory == False:
            distance_player_x = abs(player.x - self.x)
            distance_player_y = abs(player.y - self.y)
            distance_player_total = math.hypot(player.x - self.x, player.y -self.y)

            if self.mv_mode == self.MOVE_GROUND:
                self.y = self.ground_y
            elif self.mv_mode == self.MODE_LEVITATE:
                target_y_levitate = self.ground_y - self.lvt_height
                if self.y < target_y_levitate:
                    self.y += min(self.fly_speed_y, target_y_levitate - self.y)
                elif self.y > target_y_levitate:
                    self.y -= min(self.fly_speed_y, self.y - target_y_levitate)
            elif self.mv_mode == self.MODE_FLY:
                if player.y > self.y:
                    self.y += min(self.fly_speed_y, player.y - self.y)
                elif player.y < self.y:
                    self.y -= min(self.fly_speed_y, self.y - player.y)

            if self.can_shoot and distance_player_total <= config.shooting_range:
                self.is_attack = False
                self.moving_left = False
                self.moving_right = False
                self.direction = 1 if player.x > self.x else -1

                current_time = time.get_ticks()
                if current_time - self.last_shoot_time > self.shoot_cooldown and not self.is_shooting:
                    self.is_shooting = True
                    self.last_shoot_time = current_time
                    self.attack_count = 0
                    self.can_create_prj = True

            elif not self.is_shooting:
                if player.x > self.x:
                    self.moving_right = True
                    self.moving_left = False
                    self.is_attack = False
                    self.direction = 1
                    self.x += min(self.speed, player.x - self.x)
                elif player.x < self.x:
                    self.moving_right = False
                    self.moving_left = True
                    self.is_attack = False
                    self.direction = -1
                    self.x -= min(self.speed, self.x - player.x)
                else:
                    self.moving_left = False
                    self.moving_right = False
                    if not self.can_shoot:
                        self.is_attack = True
                    else:
                        self.is_stand = True
                        self.direction = 1 if player.x > self.x else -1
                        self.standing = self.animations['idle_right'] if self.direction == 1 else self.animations['idle_left']

        else:
            self.moving_left = False
            self.moving_right = False
            self.is_attack = False
            self.is_shooting = False
            self.is_stand = True
            if self.mv_mode != self.MOVE_GROUND:
                self.fly_speed_y = 0

    def draw(self, wn, player, enemy):
        if not self.visible:
            return

        self.hitbox_enemy = Rect(self.x, self.y, config.width_enemy, config.height_enemy)
        #draw.rect(wn, (255, 0, 0), self.hitbox_enemy, 2)

        if self.is_dead:
            current_animation = self.animations.get('dead') if self.direction == 1 else self.animations.get('dead_left')
            wn.blit(current_animation[self.dead_count // config.ANIMATION_SPEED % len(current_animation)], (self.x, self.y))
            self.dead_count += 1
            if self.dead_count >= len(current_animation) * config.ANIMATION_SPEED:
                self.visible = False
            return

        elif self.is_shooting:
            current_animation = self.animations.get('shoot_right') if self.direction == 1 else self.animations.get('shoot_left')
            if current_animation:
                wn.blit(current_animation[self.attack_count // config.ANIMATION_SPEED % len(current_animation)], (self.x, self.y))
                self.attack_count += 1

                if self.attack_count // config.ANIMATION_SPEED ==  (len(current_animation) - 1) and self.can_create_prj:
                    self.projectiles.append(Projectile(
                        self.x + config.width_enemy // 2,
                        self.y + config.height_enemy // 2,
                        player.x + config.widht_player // 2,
                        player.y + config.height_player // 2,
                        self.prj_speed,
                        self.prj_damage,
                        self.animations.get('prj_right') if self.direction == 1 else self.animations.get('prj_left')
                    ))
                    self.can_create_prj = False

                if self.attack_count >= len(current_animation) * config.ANIMATION_SPEED:
                    self.is_shooting = False
                    self.attack_count = 0
            else:
                self.is_shooting = False
                self.attack_count = 0

        elif self.is_attack:
            current_animation = self.animations['attack_right'] if self.moving_right or not self.moving_left else self.animations['attack_left']
            wn.blit(current_animation[self.attack_count // config.ANIMATION_SPEED % len(current_animation)], (self.x, self.y))
            self.attack_count += 1

            if self.attack_count >= len(current_animation) * 6:
                self.attack_count = 0
                self.check_collision_hero(player)

        elif self.moving_right or self.moving_left:
            if self.mv_mode == self.MOVE_GROUND:
                current_animation = self.animations['run_right'] if self.direction == 1 else self.animations['run_left']
            elif self.mv_mode != self.MOVE_GROUND:
                current_animation = self.animations.get('fly_right', self.animations['idle_right']) if self.direction == 1 else self.animations.get('fly_left', self.animations['idle_left'])
            wn.blit(current_animation[self.walk_count // config.ANIMATION_SPEED % len(current_animation)], (self.x, self.y))
        else:
            if self.mv_mode == self.MOVE_GROUND:
                current_animation = self.standing
            elif self.mv_mode != self.MOVE_GROUND:
                current_animation = self.animations.get('idle_right', self.standing) if self.direction == 1 else self.animations.get('idle_left', self.standing)
            wn.blit(current_animation[self.walk_count // config.ANIMATION_SPEED % len(current_animation)], (self.x, self.y))

        self.walk_count += 1

        for projectile in list(self.projectiles):
            projectile.update(player, enemy)
            projectile.draw(wn)
            projectile.can_damage_player(player)

            if not projectile.visible:
                self.projectiles.remove(projectile)

    def draw_health_bar(self, wn):
        if self.visible:
            health_x = self.x + (config.width_enemy - config.width_health_enemy) // 2
            health_y = self.y - 15
            health_ratio = max(self.health / self.max_health, 0)
            health_width = int(health_ratio * config.width_health_enemy)
            health_bar = Rect(self.x + 15, self.y - 5, health_width, config.height_health_enemy)
            draw.rect(wn, (255, 0, 255), health_bar)
            health_text = config.fuente.render(f"Vida: {self.health}", True, config.text_color)
            text_x = self.x + (config.width_enemy - health_text.get_width()) / 2
            text_y = self.y - 35
            wn.blit(health_text, (text_x, text_y))
            if self.health <= 0:
                self.health = 0
                self.is_dead = True

    def check_collision_hero(self, player):
        if self.hitbox_enemy.colliderect(player.hitbox_player):
            player.health -= self.num_hurt

#Todo: Clase proyectil
class Projectile:
    def __init__(self, x, y, target_X, target_y, speed, damage, animation_frames):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.animation_frames = animation_frames
        self.current_frame = 0
        self.visible = True
        self.reflected = False
        delta_x = target_X - self.x
        delta_y = target_y - self.y
        distance = math.hypot(delta_x, delta_y)

        if distance == 0:
            self.dx = 0
            self.dy = 0
            self.visible = False
        else:
            self.dx = (delta_x / distance) * self.speed
            self.dy = (delta_y / distance) * self.speed

        self.rect = self.animation_frames[0].get_rect(center=(self.x, self.y))

    def update(self, hero, enemy):
        self.x += self.dx
        self.y += self.dy

        self.rect.center = (self.x, self.y)
        self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

        if self.x < -50 or self.x > config.WIDHT + 50 or self.y < -50 or self.y > config.HEIGHT + 50:
            self.visible = False
            return

        if not self.reflected and hero.state == PlayerState.ATTACKING and self.rect.colliderect(hero.hitbox_player):
            self.dx *= -1
            self.dy *= -1
            self.reflected = True

        if self.reflected and self.rect.colliderect(enemy.hitbox_enemy):
            enemy.health -= self.damage
            self.visible = False

    def can_damage_player(self, player):
        if player.state != PlayerState.ATTACKING and self.visible and self.rect.colliderect(player.hitbox_player):
            player.health -= self.damage
            self.visible = False

    def draw(self, wn):
        if self.visible:
            wn.blit(self.animation_frames[self.current_frame], self.rect.topleft)

class Npc:
    def __init__(self, x, y, width, height, name, to_x, to_y, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animations = npc(name, self.width, self.height)
        self.hitbox_npc = Rect(self.x, self.y, self.width, self.height)
        self.state = self.animations["idle_right"]
        self.range = 20
        self.start_moving = False
        self.move_to_x = to_x
        self.move_to_y = to_y
        self.in_coor = False #! RECORDATORIO: Esta variable sirve para saber si el npc ha llegado a la coordenada establecida
        self.walk_count = 0
        self.second_anim_count = 0
        self.speed = speed
        self.cinematic = False
        self.second_anim = False
        self.second_anim_timer = 0
        self.repeat = True
        self.last_animantion_frame = True
        self.finish_npc_work = False

    def update(self, player):
        self.hitbox_npc.x = self.x
        self.hitbox_npc.y = self.y

        if self.repeat:
            distance = math.hypot(player.hitbox_player.centerx - self.hitbox_npc.centerx,
                                player.hitbox_player.centery - self.hitbox_npc.centery)

            if distance <= self.range:
                self.start_moving = True
                self.repeat = False
            else:
                self.start_moving = False

        if self.start_moving and not self.in_coor:
            # Mover horizontalmente
            if abs(self.x - self.move_to_x) > self.speed:
                if self.x > self.move_to_x:
                    self.x -= self.speed
                    self.state = self.animations.get("walk_left", self.state)
                else:
                    self.x += self.speed
                    self.state = self.animations.get("walk_right", self.state)
            else:
                self.x = self.move_to_x

            # Mover verticalmente
            if abs(self.y - self.move_to_y) > self.speed:
                if self.y > self.move_to_y:
                    self.y -= self.speed
                else:
                    self.y += self.speed
            else:
                self.y = self.move_to_y

            if abs(self.x - self.move_to_x) < 2 and abs(self.y - self.move_to_y) < 2:
                self.in_coor = True
                self.cinematic = True
                self.start_moving = False

    def draw(self, wn, level, tipo):
        if self.start_moving:
            wn.blit(self.state[self.walk_count // config.ANIMATION_SPEED % len(self.state)], (self.x, self.y))
            self.walk_count += 1
        elif self.in_coor:
            if self.cinematic:
                reproducir_cinematica(wn, level, tipo)
                self.cinematic = False
            elif self.second_anim_count < len(self.animations["sword_left"]) * config.ANIMATION_SPEED:
                wn.blit(self.animations["sword_left"][self.second_anim_count // config.ANIMATION_SPEED % len(self.state)], (self.x, self.y))
                self.second_anim_count += 1
            else:
                if self.last_animantion_frame:
                    wn.blit(self.animations["sword_left"][-1], (self.x, self.y))
                if self.second_anim_timer == 0:
                    self.second_anim_timer = time.get_ticks()

                if time.get_ticks() - self.second_anim_timer > 5000:
                    self.last_animantion_frame = False
                    wn.blit(self.animations["idle_left"], (self.x, self.y))
                    self.finish_npc_work = True

        else:
            wn.blit(self.animations["idle_left"], (self.x, self.y))