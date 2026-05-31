from pygame import *
from src.core.settings.config import inventory_font, white

class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class RectButton(Shape):
    # Reemplazamos 'color' por las tres imágenes correspondientes
    def __init__(self, x_button, y_button, width, height, img_normal, img_hover, img_pressed):
        super().__init__(x_button, y_button)
        self.width_button = width
        self.height_button = height
        self.form_button = Rect(self.x, self.y, self.width_button, self.height_button)

        # Escalamos las imágenes al tamaño del botón por seguridad
        self.img_normal = transform.scale(img_normal, (width, height))
        self.img_hover = transform.scale(img_hover, (width, height))
        self.img_pressed = transform.scale(img_pressed, (width, height))

        # Estado inicial
        self.is_pressed = False

    def draw_button(self, wn, text=None):
        # 1. Obtener la posición del ratón y el estado de los clics
        mouse_pos = mouse.get_pos()
        mouse_click = mouse.get_pressed()

        # 2. Determinar qué imagen usar
        current_img = self.img_normal

        if self.form_button.collidepoint(mouse_pos):
            if mouse_click[0]: # Si el clic izquierdo está presionado
                current_img = self.img_pressed
                self.is_pressed = True
            else:
                current_img = self.img_hover
                self.is_pressed = False
        else:
            self.is_pressed = False

        # 3. Dibujar la imagen de fondo
        wn.blit(current_img, (self.x, self.y))

        if text:
            # 4. Dibujar el texto centrado
            text_surface = inventory_font.render(text, True, white)
            text_rect = text_surface.get_rect(center=self.form_button.center)
            wn.blit(text_surface, text_rect)

    def click(self, event):
        # Simplificado: si hubo un evento de levantar el clic y estábamos presionando el botón
        if event.type == MOUSEBUTTONUP and event.button == 1:
            if self.form_button.collidepoint(event.pos) and self.is_pressed:
                self.is_pressed = False
                return True
        return False


class CircleButton(Shape):
    def __init__(self, x, y, radius, img_normal, img_hover, img_pressed):
        super().__init__(x, y)
        self.radio = radius
        # En los círculos, el centro suele ser x, y. Si tus imágenes nacen desde la esquina:
        self.center_button = (self.x + self.radio, self.y + self.radio)

        # Escalamos las imágenes al diámetro del círculo
        diameter = radius * 2
        self.img_normal = transform.scale(img_normal, (diameter, diameter))
        self.img_hover = transform.scale(img_hover, (diameter, diameter))
        self.img_pressed = transform.scale(img_pressed, (diameter, diameter))

        self.is_pressed = False

    def draw(self, wn, text):
        mouse_pos = mouse.get_pos()
        mouse_click = mouse.get_pressed()

        # Calcular distancia matemática para colisión circular
        distance = ((mouse_pos[0] - self.center_button[0])**2 + (mouse_pos[1] - self.center_button[1])**2)**0.5

        current_img = self.img_normal

        if distance <= self.radio:
            if mouse_click[0]:
                current_img = self.img_pressed
                self.is_pressed = True
            else:
                current_img = self.img_hover
                self.is_pressed = False
        else:
            self.is_pressed = False

        # Dibujar la imagen (ajustando la esquina superior izquierda para el blit)
        top_left_x = self.center_button[0] - self.radio
        top_left_y = self.center_button[1] - self.radio
        wn.blit(current_img, (top_left_x, top_left_y))

        # Dibujar texto
        text_surface = inventory_font.render(text, True, white)
        text_rect = text_surface.get_rect(center=self.center_button)
        wn.blit(text_surface, text_rect)

    def click(self, event):
        if event.type == MOUSEBUTTONUP and event.button == 1:
            mouse_x, mouse_y = event.pos
            distance = ((mouse_x - self.center_button[0])**2 + (mouse_y - self.center_button[1])**2)**0.5
            if distance <= self.radio and self.is_pressed:
                self.is_pressed = False
                return True
        return False
