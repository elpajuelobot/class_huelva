import pygame
from src.core.system.buttons.buttons import RectButton
from src.core.system.game_states.fatherClass import GameState
from src.core.settings.config import white


class PauseMenu(GameState):
    def __init__(self, motor, gaming_state):
        super().__init__(motor)
        self.gaming_state = gaming_state

        self.img_n = pygame.image.load("src\\data\\img\\background\\states\\initial\\play_void.png")
        self.img_h = pygame.image.load("src\\data\\img\\background\\states\\initial\\play_hover_void.png")
        self.img_p = pygame.image.load("src\\data\\img\\background\\states\\initial\\play_pressed_void.png")

        self.resume_button = RectButton(
            self.motor.width // 2 - 200,
            self.motor.height // 2 - 40,
            400, 50, self.img_n, 
            self.img_h, 
            self.img_p
        )

        self.initial_button = RectButton(
            self.motor.width // 2 - 200,
            self.motor.height // 2 + 40,
            400, 50, self.img_n, 
            self.img_h, 
            self.img_p
        )

        self.pause_text = self.motor.font.render("GAME PAUSED", True, white)


    def events_(self, events):
        for event in events:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or self.resume_button.click(event):
                self.motor.change_state(self.gaming_state)

            if self.initial_button.click(event):
                from src.core.system.game_states.initial import InitialMenu
                self.motor.change_state(InitialMenu(self.motor))

    def update_(self):
        pass

    def draw_(self, wn):
        self.gaming_state.draw_(wn)

        overlay = pygame.Surface((self.motor.width, self.motor.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        wn.blit(overlay, (0, 0))

        text_rect = self.pause_text.get_rect(center=(self.motor.width // 2, self.motor.height // 2 - 120))
        wn.blit(self.pause_text, text_rect)

        self.resume_button.draw_button(wn, text="Back to Game")
        self.initial_button.draw_button(wn, text="Save and Quit to Title")
