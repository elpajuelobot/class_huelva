import pygame
import random
from src.core.system.buttons.buttons import RectButton
from src.core.system.game_states.fatherClass import GameState
from src.core.system.game_states.worlds import WorldsMenu


class InitialMenu(GameState):
    def __init__(self, motor):
        super().__init__(motor)
        self.background = pygame.transform.scale(
            pygame.image.load("src/data/img/background/states/initial/initial.webp"),
            (self.motor.width, self.motor.height)
        ).convert_alpha()
        self.text_background = pygame.transform.scale(
            pygame.image.load("src/data/img/background/states/initial/Maincraft.png"),
            (self.motor.width, self.motor.height // 2)
        ).convert_alpha()

        self.img_n = pygame.image.load("src/data/img/background/states/initial/play_void.png")
        self.img_h = pygame.image.load("src/data/img/background/states/initial/play_hover_void.png")
        self.img_p = pygame.image.load("src/data/img/background/states/initial/play_pressed_void.png")

        self.playButton = RectButton(
            (self.motor.width // 2 - 100), self.motor.height // 2,
            200, 50, self.img_n, self.img_h, self.img_p
        )

    def events_(self, events):
        for event in events:
            if self.playButton.click(event):
                self.motor.change_state(WorldsMenu(self.motor, self))

    def update_(self):
        pass

    def draw_(self, wn):
        wn.blit(self.background, (0, 0))
        wn.blit(self.text_background, (0, 0))
        self.playButton.draw_button(wn, text="Worlds")
