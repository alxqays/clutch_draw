from clutch_draw.game_state import GameState

from pygame import MOUSEBUTTONUP, Surface, Color
from pygame.font import Font
from pygame.event import Event

from clutch_draw.ui.buttons import create_button
from clutch_draw.ui.mouse import mouse_inside

import pygame


class ControlsScreen:

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        screen: Surface,
        button_font: Font,
        title_font: Font,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.button_font = button_font
        self.title_font = title_font

    def render(self, events: list[Event]) -> GameState:

        self.screen.fill("grey")

        main_text = self.title_font.render("Controls", True, Color(255, 255, 255))
        border_text = self.title_font.render("Controls", True, Color(0, 0, 0))

        text_x = self.screen_width // 2 - main_text.get_width() // 2
        text_y = self.screen_height // 2 - main_text.get_height() // 2 - 140

        border = 5

        self.screen.blit(border_text, (text_x - border, text_y))
        self.screen.blit(border_text, (text_x + border, text_y))
        self.screen.blit(border_text, (text_x, text_y - border))
        self.screen.blit(border_text, (text_x, text_y + border))

        self.screen.blit(main_text, (text_x, text_y))

        font = pygame.font.Font("resources/fonts/Apocalypse.ttf", 28)
        header_font = pygame.font.Font("resources/fonts/Apocalypse.ttf", 32)

        controls = [
            ("1-5", "Play cards"),
            ("D", "Draw card"),
            ("P / ESC", "Pause"),
            ("Q", "Quit game"),
            ("Mouse", "Select cards"),
        ]

        start_y = self.screen_height // 2 - 30

        key_x = self.screen_width // 2 - 120
        action_x = self.screen_width // 2 + 40

        key_header = header_font.render("KEY", True, (255, 255, 255))
        action_header = header_font.render("ACTION", True, (255, 255, 255))

        self.screen.blit(key_header, (key_x, start_y - 60))
        self.screen.blit(action_header, (action_x, start_y - 60))

        pygame.draw.line(
            self.screen,
            (255, 255, 255),
            (key_x, start_y - 15),
            (action_x + 180, start_y - 15),
            2,
        )

        for i, (key, action) in enumerate(controls):
            key_text = font.render(key, True, (255, 255, 255))
            action_text = font.render(action, True, (255, 255, 255))

            y = start_y + i * 50

            self.screen.blit(key_text, (key_x, y))
            self.screen.blit(action_text, (action_x, y))

        back_button = create_button(self.button_font, "Back")

        back_x = self.screen_width // 2 - back_button.get_width() // 2
        back_y = self.screen_height - back_button.get_height() - 80

        self.screen.blit(back_button, (back_x, back_y))

        next_state = GameState.CONTROLS_SCREEN

        for event in events:
            if event.type == MOUSEBUTTONUP:
                if mouse_inside(event, back_button, back_x, back_y):
                    return GameState.OPTIONS_SCREEN

        return next_state
