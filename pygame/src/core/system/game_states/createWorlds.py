import pygame
from src.core.system.buttons.buttons import RectButton
from src.core.system.game_states.fatherClass import GameState
from src.core.system.inputs.inputs import InputBox
from src.core.settings.config import white
from src.core.system.game_states.game import GamingState
from src.database.scripts.database import DataBase


class CreateMenu(GameState):
    def __init__(self, motor, worlds_menu):
        super().__init__(motor)
        self.worlds_menu = worlds_menu
        self.db = DataBase()

        self.img_n = pygame.image.load("src/data/img/background/states/initial/play_void.png")
        self.img_h = pygame.image.load("src/data/img/background/states/initial/play_hover_void.png")
        self.img_p = pygame.image.load("src/data/img/background/states/initial/play_pressed_void.png")

        self.CreateButton = RectButton(
            self.motor.width // 2 - 200,
            self.motor.height // 2 + 110,
            400, 50, self.img_n,
            self.img_h,
            self.img_p
        )

        self.BackButton = RectButton(
            self.motor.width // 2 - 200,
            self.motor.height // 2 + 180,
            400, 50, self.img_n,
            self.img_h,
            self.img_p
        )

        self.world_text = self.motor.font.render("CREATE YOUR WORLD", True, white)
        self.world_name_text = self.motor.font.render("World Name:", True, white)
        self.world_sed_text = self.motor.font.render("World Sed:", True, white)

        self.input_world_name = InputBox(
            x=self.motor.width // 2 - 75,
            y=self.motor.height // 2 - 70,
            w=150,
            h=50,
            text="New World"
        )

        self.input_world_sed = InputBox(
            x=self.motor.width // 2 - 75,
            y=self.motor.height // 2,
            w=150,
            h=50,
            letters=False
        )

        self.inputs_boxes = [self.input_world_name, self.input_world_sed]


    def events_(self, events):
        for event in events:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or self.BackButton.click(event):
                self.motor.change_state(self.worlds_menu)

            if self.CreateButton.click(event):
                world_name = self.input_world_name.text.strip()
                if not world_name:
                    world_name = "New World"

                if self.input_world_sed.text.strip():
                    world_sed = int(self.input_world_sed.text)
                    self.motor.change_state(GamingState(self.motor, sed=world_sed))
                else:
                    self.motor.change_state(GamingState(self.motor))

                    print("New world has been created:")
                    print(f"  1. New world name: {self.input_world_name.text}")
                    print(f"  2. New world sed:  {self.input_world_sed.text}")

                self.db.WriteDelete("""
                        INSERT INTO worlds (name, seed)
                        VALUES (?, ?)
                """, (self.input_world_name.text, self.motor.world.sed))

            for input_box in self.inputs_boxes:
                input_box.handle_event(event)

    def update_(self):
        for input_box in self.inputs_boxes:
            input_box.update()

    def draw_(self, wn):
        self.worlds_menu.draw_(wn)

        overlay = pygame.Surface((self.motor.width, self.motor.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        wn.blit(overlay, (0, 0))

        text_rect = self.world_text.get_rect(center=(self.motor.width // 2, self.motor.height // 2 - 200))
        wn.blit(self.world_text, text_rect)

        text_rect_name = self.world_name_text.get_rect(center=(self.motor.width // 2 - 170, self.motor.height // 2 - 45))
        wn.blit(self.world_name_text, text_rect_name)

        text_rect_sed = self.world_sed_text.get_rect(center=(self.motor.width // 2 - 170, self.motor.height // 2 + 20))
        wn.blit(self.world_sed_text, text_rect_sed)

        for input_box in self.inputs_boxes:
            input_box.draw(wn)

        self.CreateButton.draw_button(wn, text="Create World")
        self.BackButton.draw_button(wn, text="Back")
