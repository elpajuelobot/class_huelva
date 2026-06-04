import pygame
from src.core.system.buttons.buttons import RectButton
from src.core.system.game_states.fatherClass import GameState
from src.database.scripts.database import DataBase
from src.core.system.game_states.game import GamingState


class WorldsMenu(GameState):
    def __init__(self, motor, initial_menu):
        super().__init__(motor)
        self.initial_menu = initial_menu
        self.db = DataBase()
        self.background = pygame.transform.scale(
            pygame.image.load("src/data/img/background/states/initial/initial.webp"),
            (self.motor.width, self.motor.height)
        ).convert_alpha()

        self.img_n = pygame.image.load("src/data/img/background/states/initial/play_void.png")
        self.img_h = pygame.image.load("src/data/img/background/states/initial/play_hover_void.png")
        self.img_p = pygame.image.load("src/data/img/background/states/initial/play_pressed_void.png")

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

        self.world_block_x = 50
        self.world_block_y = 160
        self.world_block_width = self.motor.width - 100
        self.world_block_height = 80
        self.world_spacing = 15
        self.worlds_buttons = []
        self.load_worlds()


    def load_worlds(self):
        self.worlds = self.db.Select("SELECT * FROM worlds ORDER BY last_played DESC")

        if self.worlds is None:
            self.worlds = []

        self.worlds_buttons = []

        for index, world in enumerate(self.worlds):
            world_id = world["id"]
            world_name = world["name"]
            world_seed = world["seed"]
            player_axis = world["player_axis"]
            list_player_axis = player_axis.split(",")
            x_player = int(list_player_axis[0].replace("X:", ""))
            y_player = int(list_player_axis[1].replace("Y:", ""))
            delta_y = self.world_block_y + index * (self.world_block_height + self.world_spacing)

            world_block = RectButton(
                self.world_block_x,
                delta_y,
                self.world_block_width,
                self.world_block_height,
                self.img_n,
                self.img_h,
                self.img_p
            )

            self.worlds_buttons.append({
                "button": world_block,
                "id": world_id,
                "name": world_name,
                "seed": world_seed
            })

    def events_(self, events):
        for event in events:
            if self.BackButton.click(event):
                self.motor.change_state(self.initial_menu)

            if self.CreateWorld.click(event):
                from src.core.system.game_states.createWorlds import CreateMenu
                self.motor.change_state(CreateMenu(self.motor, self))

            for world_data in self.worlds_buttons:
                if world_data["button"].click(event):
                    query_seed = world_data["seed"]
                    world_seed = query_seed if query_seed else None

                    self.motor.change_state(GamingState(self.motor, sed=world_seed))
                    break


    def update_(self):
        pass

    def draw_(self, wn):
        wn.blit(self.background, (0, 0))
        self.BackButton.draw_button(wn, text="Back")
        self.CreateWorld.draw_button(wn, text="Create new World")
        for world_data in self.worlds_buttons:
            world_data["button"].draw_button(wn, text=world_data["name"])
