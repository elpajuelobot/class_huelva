import pygame
from src.core.settings.config import (
    COLOR_ACTIVE, COLOR_INACTIVE, font,
    abc, nums
)


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
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.text:
                        self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = font.render(self.text, True, self.color)

    def update(self):
        if not self.letters:
            list_text = self.text.strip()
            for character in list_text:
                for letter in abc:
                    if character.lower() == letter:
                        self.active = False

        if not self.numbers:
            list_text = self.text.strip()
            for character in list_text:
                for num in nums:
                    if character.lower() == num:
                        self.active = False

        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, wn):
        # Blit the text.
        wn.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + (self.rect.h // 3)))
        # Blit the rect.
        pygame.draw.rect(wn, self.color, self.rect, 2)
