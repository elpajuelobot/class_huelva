import pygame
from src.core.system.buttons.buttons import RectButton

class Initial_Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background = pygame.transform.scale(
            pygame.image.load("src\\data\\img\\background\\states\\initial\\initial.webp"),
            (self.width, self.height)
        ).convert_alpha()
        self.play_button = RectButton(self.width / 2, self.height / 2, self.width / 5, self.height / 7)
