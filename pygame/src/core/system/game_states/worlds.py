import pygame
from src.core.system.buttons.buttons import RectButton
from src.core.system.game_states.fatherClass import GameState


class WorldsMenu(GameState):
    def __init__(self, motor, initial_menu):
        super().__init__(motor)
        self.initial_menu = initial_menu
        self.background = pygame.transform.scale(
            pygame.image.load("src\\data\\img\\background\\states\\initial\\initial.webp"),
            (self.motor.width, self.motor.height)
        ).convert_alpha()

        self.img_n = pygame.image.load("src\\data\\img\\background\\states\\initial\\play_void.png")
        self.img_h = pygame.image.load("src\\data\\img\\background\\states\\initial\\play_hover_void.png")
        self.img_p = pygame.image.load("src\\data\\img\\background\\states\\initial\\play_pressed_void.png")

        self.BackButton = RectButton(
            x_button=50,
            y_button=50,
            width=80,
            height=80,
            img_normal=self.img_n,
            img_hover=self.img_h,
            img_pressed=self.img_p
        )

        self.CreateWorld = RectButton(
            x_button=140,
            y_button=50,
            width=self.motor.width - 190,
            height=80,
            img_normal=self.img_n,
            img_hover=self.img_h,
            img_pressed=self.img_p
        )


    def events_(self, events):
        for event in events:
            if self.BackButton.click(event):
                self.motor.change_state(self.initial_menu)

            if self.CreateWorld.click(event):
                from src.core.system.game_states.createWorlds import CreateMenu
                self.motor.change_state(CreateMenu(self.motor, self))

    def update_(self):
        pass

    def draw_(self, wn):
        wn.blit(self.background, (0, 0))
        self.BackButton.draw_button(wn, text="Back")
        self.CreateWorld.draw_button(wn, text="Create new World")
