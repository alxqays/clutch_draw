from clutch_draw.game_state import GameState
from pygame_gui import UIManager

from pygame import MOUSEBUTTONUP, Surface, Color
from pygame.font import Font
from pygame.event import Event

from clutch_draw.ui.buttons import create_button
from clutch_draw.ui.mouse import mouse_inside

import pygame


class AudioScreen:

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        screen: Surface,
        button_font: Font,
        title_font: Font,
        manager: UIManager,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.button_font = button_font
        self.title_font = title_font
        self.manager = manager

        self.volume = 100

    def render(self, events: list[Event]) -> GameState:

        self.screen.fill("grey")

        main_text = self.title_font.render("Audio", True, Color(255, 255, 255))
        border_text = self.title_font.render("Audio", True, Color(0, 0, 0))

        text_x = self.screen_width // 2 - main_text.get_width() // 2
        text_y = self.screen_height // 2 - main_text.get_height() // 2 - 65

        border = 5

        self.screen.blit(border_text, (text_x - border, text_y))
        self.screen.blit(border_text, (text_x + border, text_y))
        self.screen.blit(border_text, (text_x, text_y - border))
        self.screen.blit(border_text, (text_x, text_y + border))

        self.screen.blit(main_text, (text_x, text_y))

        volume_font = Font(None, 50)
        volume_text = volume_font.render(
            f"Volume: {self.volume}%", True, Color(255, 255, 255)
        )

        volume_x = self.screen_width // 2 - volume_text.get_width() // 2
        volume_y = self.screen_height // 2 + 20

        self.screen.blit(volume_text, (volume_x, volume_y))

        symbol_font = pygame.font.Font("resources/fonts/Apocalypse.ttf", 40)

        down_button = symbol_font.render("-", True, (255, 255, 255))
        up_button = symbol_font.render("+", True, (255, 255, 255))
        back_button = create_button(self.button_font, "Back")

        button_y = self.screen_height // 2 + 100

        centre_x = self.screen_width // 2
        spacing = 40

        up_x = centre_x - down_button.get_width() - spacing
        down_x = centre_x + spacing

        back_x = self.screen_width // 2 - back_button.get_width() // 2
        back_y = self.screen_height - back_button.get_height() - 80

        self.screen.blit(down_button, (down_x, button_y))
        self.screen.blit(up_button, (up_x, button_y))
        self.screen.blit(back_button, (back_x, back_y))

        next_state = GameState.AUDIO_SCREEN

        for event in events:
            if event.type == MOUSEBUTTONUP:

                if mouse_inside(event, down_button, down_x, button_y):
                    self.volume = max(0, self.volume - 10)

                if mouse_inside(event, up_button, up_x, button_y):
                    self.volume = min(100, self.volume + 10)

                if mouse_inside(event, back_button, back_x, back_y):
                    next_state = GameState.OPTIONS_SCREEN

        return next_state
