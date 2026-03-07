import pygame
import sys

# Configuración
WIDTH, HEIGHT = 800, 600
TILE_WIDTH = 64
TILE_HEIGHT = 32

def cartesian_to_iso(x, y):
    iso_x = (x - y) * (TILE_WIDTH // 2)
    iso_y = (x + y) * (TILE_HEIGHT // 2)
    # Centramos el mapa en la pantalla
    return iso_x + WIDTH // 2, iso_y + HEIGHT // 4

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # --- CARGA DE ASSETS ---
    # Usamos .convert_alpha() para que la transparencia funcione bien
    try:
        grass_img = pygame.image.load("cesped_2.jpg").convert_alpha()
        player_img = pygame.image.load("_IdleL_4.png").convert_alpha()
    except:
        # Failsafe: Si no tienes las fotos, creamos superficies de colores
        grass_img = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.polygon(grass_img, (34, 139, 34), [(32,0), (64,16), (32,32), (0,16)])
        player_img = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.rect(player_img, (200, 50, 50), (16, 0, 32, 48))

    player_pos = [0, 0]
    map_size = 8

    while True:
        screen.fill((50, 50, 80)) # Color de fondo (Cielo/Oscuro)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:    player_pos[1] -= 1
                if event.key == pygame.K_DOWN:  player_pos[1] += 1
                if event.key == pygame.K_LEFT:  player_pos[0] -= 1
                if event.key == pygame.K_RIGHT: player_pos[0] += 1

        # DIBUJAR EL MAPA (Suelo)
        for x in range(map_size):
            for y in range(map_size):
                iso_x, iso_y = cartesian_to_iso(x, y)
                # Ajuste: Pygame dibuja desde la esquina superior izquierda.
                # Restamos la mitad del ancho del sprite para centrarlo.
                screen.blit(grass_img, (iso_x - grass_img.get_width()//2, iso_y))

        # DIBUJAR AL JUGADOR
        p_iso_x, p_iso_y = cartesian_to_iso(player_pos[0], player_pos[1])
        # Ajuste: El personaje suele ser más alto, lo subimos un poco para que "pise" el tile
        screen.blit(player_img, (p_iso_x - player_img.get_width()//2, p_iso_y - player_img.get_height() + TILE_HEIGHT))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
