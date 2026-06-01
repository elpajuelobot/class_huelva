import pygame
from src.core.system.buttons.buttons import RectButton
from src.core.system.game_states.fatherClass import GameState


class Defeat(GameState):
    def __init__(self, motor, gaming_state):
        super().__init__(motor)
        self.gaming_state = gaming_state

        self.img_n = pygame.image.load("src/data/img/background/states/initial/play_void.png")
        self.img_h = pygame.image.load("src/data/img/background/states/initial/play_hover_void.png")
        self.img_p = pygame.image.load("src/data/img/background/states/initial/play_pressed_void.png")
        self.background = pygame.transform.scale(
            pygame.image.load("src/data/img/background/states/initial/defeat.png"),
            (self.motor.width, self.motor.height)
        ).convert_alpha()

        self.respawn_button = RectButton(
            self.motor.width // 2 - 200,
            self.motor.height // 2 + 25,
            400, 60, self.img_n, 
            self.img_h, 
            self.img_p
        )

        self.initial_button = RectButton(
            self.motor.width // 2 - 200,
            self.motor.height // 2 + 90,
            400, 60, self.img_n, 
            self.img_h, 
            self.img_p
        )


    def events_(self, events):
        for event in events:
            if self.initial_button.click(event):
                from src.core.system.game_states.initial import InitialMenu
                self.motor.change_state(InitialMenu(self.motor))
            if self.respawn_button.click(event):
                self.motor.change_state(self.gaming_state)
                self.motor.hero.health = self.motor.hero.initial_health
                self.motor.hero.bubbles = self.motor.hero.initial_bubbles
                self.motor.hero.world_x = 400
                self.motor.hero.world_y = 300

    def update_(self):
        pass

    def draw_(self, wn):
        self.gaming_state.draw_(wn)

        overlay = pygame.Surface((self.motor.width, self.motor.height), pygame.SRCALPHA)
        overlay.fill((210, 0, 0, 150))
        wn.blit(overlay, (0, 0))
        wn.blit(self.background, (0, 0))

        self.initial_button.draw_button(wn, text="Title Screen")
        self.respawn_button.draw_button(wn, text="Respawn")
