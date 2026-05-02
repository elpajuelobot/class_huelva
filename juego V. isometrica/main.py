from math import dist
import json
import pygame
from random import randint

with open('zones.json') as data:
    zonas = json.load(data)
    zonas = zonas.get("zonas", [])

def encuentros(zone, player_pos, mob_list, zonas_list, radio_detect=100):
    if zone not in zonas_list:
        print("Zona no encontrada")
        zone = "zona desconocida"

    mobs_nearby = []

    for mobs in mob_list:
        if dist(player_pos, mobs) <= radio_detect:
            mobs_nearby.append(mobs)

    count_mobs = len(mobs_nearby)

    if count_mobs == 0:
        dificultad = "Nula"
        message = "Todo está tranquilo"
    elif count_mobs <= 3:
        dificultad = "Baja"
        message = "Estate atento..."
    elif count_mobs <= 5:
        dificultad = "Media"
        message = "¡CUIDADO!"
    else:
        dificultad = "Alta"
        message = "¡HUYE!"

    return {
        "zona": zone,
        "mobs_detected": count_mobs,
        "dificultad": dificultad,
        "alerta": message
    }



# Inicializar Pygame
pygame.init()

# Variables para player
x = 500
y = 500
width = 20
height = 20
area_detection_radius = 100
see_area = False

# Variables
FPS = 60
clock = pygame.time.Clock()
run = True
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
font = pygame.font.Font(None, 30)

# Configuración de la ventana
wn = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Detección de mobs")
background = pygame.transform.scale(pygame.image.load("fondo.png").convert(), (1024, 768))

sprites = {
    "left": pygame.image.load("_IdleL_4.png").convert_alpha(),
    "right": pygame.image.load("_Idle_4.png").convert_alpha()
}

# Player y enemigos
player_actual_sprite = "right"
player_hitbox = sprites["right"].get_rect(topleft=(500, 500))

enemy = [
    # Zona peligrosa
    (200, 200), (150, 230), (275, 242),
    (223, 342), (185, 234), (235, 194),
    # Zona baja
    (900, 600), (776, 673), (800, 700),
    # Zona media
    (200, 600), (150, 630), (275, 642),
    (223, 742), (185, 634)
    ]

# Separadores de mapa
separadorH = pygame.Rect(0, 384, 1024, 10)
separadorV = pygame.Rect(500, 0, 10, 768)

while run:
    clock.tick(FPS)
    keys_pressed = pygame.key.get_pressed()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    # Rellenar fondo
    wn.blit(background, (0, 0))

    # Dibujar Player y área de detección
    if see_area:
        area_detection = pygame.draw.circle(wn, RED, (player_hitbox.centerx, player_hitbox.centery), area_detection_radius)

    # Separadores de mapa
    pygame.draw.rect(wn, BLACK, separadorH)
    pygame.draw.rect(wn, BLACK, separadorV)

    # Dibujar enemigos
    for mob in enemy:
        pygame.draw.circle(wn, GREEN, mob, 10)

    if keys_pressed[pygame.K_s] and player_hitbox.y < 744:
        player_hitbox.y += 5
    if keys_pressed[pygame.K_a] and player_hitbox.x > 0:
        player_hitbox.x -= 5
        player_actual_sprite = "left"
    if keys_pressed[pygame.K_w] and player_hitbox.y > 0:
        player_hitbox.y -= 5
    if keys_pressed[pygame.K_d] and player_hitbox.x < 1000:
        player_hitbox.x += 5
        player_actual_sprite = "right"

    wn.blit(sprites[player_actual_sprite], player_hitbox)

    if keys_pressed[pygame.K_PLUS] and area_detection_radius < 200:
        area_detection_radius += 5
    elif keys_pressed[pygame.K_MINUS] and area_detection_radius > 35:
        area_detection_radius -= 5
    elif keys_pressed[pygame.K_0]:
        area_detection_radius = 100
    elif keys_pressed[pygame.K_e]:
        see_area = False
    elif keys_pressed[pygame.K_r]:
        see_area = True

    if player_hitbox.colliderect(separadorH) and player_hitbox.y > 384:
        player_hitbox.y -= 45
    elif player_hitbox.colliderect(separadorH) and player_hitbox.y < 404:
        player_hitbox.y += 45
    elif player_hitbox.colliderect(separadorV) and player_hitbox.x > 500:
        player_hitbox.x -= 45
    elif player_hitbox.colliderect(separadorV) and player_hitbox.x < 520:
        player_hitbox.x += 45

    # Obtener información de la zona
    if player_hitbox.x < 512 and player_hitbox.y < 384:
        zona_actual = "pradera"
    elif player_hitbox.x >= 512 and player_hitbox.y < 384:
        zona_actual = "ciudad"
    elif player_hitbox.x >= 512 and player_hitbox.y >= 384:
        zona_actual = "castillo"
    else:
        zona_actual = "campo"

    info = encuentros(zona_actual, (player_hitbox.centerx, player_hitbox.centery), enemy, zonas, area_detection_radius)

    # Mostrar información en pantalla
    zona_text = font.render(f"Zona: {info['zona']}", True, BLACK)
    mobs_text = font.render(f"Mobs detectados: {info['mobs_detected']}", True, BLACK)
    dificultad_text = font.render(f"Dificultad: {info['dificultad']}", True, BLACK)
    alerta_text = font.render(f"Alerta: {info['alerta']}", True, BLACK)
    wn.blit(zona_text, (10, 10))
    wn.blit(mobs_text, (10, 40))
    wn.blit(dificultad_text, (10, 70))
    wn.blit(alerta_text, (10, 100))

    pygame.display.update()
