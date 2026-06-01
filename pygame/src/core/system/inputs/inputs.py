import pygame
from src.core.settings.config import COLOR_ACTIVE, COLOR_INACTIVE, font

class InputBox:
    def __init__(self, x, y, w, h, text='', letters=True, numbers=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False
        self.letters = letters
        self.numbers = numbers

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el usuario hace clic en el rectángulo
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Cambiar el color según si está activa o no
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            # Re-renderizar por si cambia el color de la fuente
            self.txt_surface = font.render(self.text, True, self.color)

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # En lugar de borrar el texto, simplemente quitamos el foco de la caja
                    self.active = False
                    self.color = COLOR_INACTIVE
                elif event.key == pygame.K_BACKSPACE:
                    # Borrar el último carácter
                    self.text = self.text[:-1]
                else:
                    # VALIDACIÓN DE ENTRADA: 
                    # Comprobamos el carácter ANTES de añadirlo al texto
                    char = event.unicode
                    is_valid = True

                    # Ignorar teclas de control ocultas (como Tab, Escape, etc.)
                    if not char.isprintable():
                        is_valid = False
                    # Bloquear letras si la caja no las admite
                    elif not self.letters and char.isalpha():
                        is_valid = False
                    # Bloquear números si la caja no los admite
                    elif not self.numbers and char.isnumeric():
                        is_valid = False

                    # Si ha pasado todos los filtros, lo añadimos
                    if is_valid:
                        self.text += char

                # Re-renderizar el texto cada vez que se pulsa una tecla
                self.txt_surface = font.render(self.text, True, self.color)

    def update(self):
        # El método update ahora es súper ligero.
        # Ya no hay bucles pesados, solo redimensiona la caja si el texto crece.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, wn):
        # Dibujar el texto
        wn.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + (self.rect.h // 3)))
        # Dibujar el rectángulo
        pygame.draw.rect(wn, self.color, self.rect, 2)
