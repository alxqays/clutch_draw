from clutch_draw.game_state import GameState
from pygame_gui import UIManager

from pygame import MOUSEBUTTONUP, Surface, Color
from pygame.font import Font
from pygame.event import Event

from clutch_draw.ui.buttons import create_button
from clutch_draw.ui.mouse import mouse_inside

import pygame


class OptionsScreen:

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

        self.background = pygame.image.load("resources/images/orig_big.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.screen_width, self.screen_height)
        )

    def render(self, events: list[Event]) -> GameState:

        self.screen.blit(self.background, (0, 0))

        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        main_text = self.title_font.render("Options", True, Color(255, 255, 255))
        border_text = self.title_font.render("Options", True, Color(0, 0, 0))

        text_x = self.screen_width // 2 - main_text.get_width() // 2
        text_y = self.screen_height // 2 - main_text.get_height() // 2 - 65

        border = 5

        self.screen.blit(border_text, (text_x - border, text_y))  # left
        self.screen.blit(border_text, (text_x + border, text_y))  # right
        self.screen.blit(border_text, (text_x, text_y - border))  # top
        self.screen.blit(border_text, (text_x, text_y + border))  # bottom

        self.screen.blit(main_text, (text_x, text_y))

        audio_button = create_button(self.button_font, "Audio")
        controls_button = create_button(self.button_font, "Controls")

        audio_x = self.screen_width // 2 - audio_button.get_width() // 2
        audio_y = self.screen_height - audio_button.get_height() - 280

        controls_x = self.screen_width // 2 - controls_button.get_width() // 2
        controls_y = self.screen_height - controls_button.get_height() - 180

        back_button = create_button(self.button_font, "Back")
        back_button_x = self.screen_width // 2 - back_button.get_width() // 2
        back_button_y = self.screen_height - back_button.get_height() - 80

        self.screen.blit(audio_button, (audio_x, audio_y))
        self.screen.blit(controls_button, (controls_x, controls_y))

        self.screen.blit(back_button, (back_button_x, back_button_y))

        next_state = GameState.OPTIONS_SCREEN

        for event in events:
            if event.type == MOUSEBUTTONUP:

                if mouse_inside(event, back_button, back_button_x, back_button_y):
                    return GameState.MAIN_MENU_SCREEN

                if mouse_inside(event, audio_button, audio_x, audio_y):
                    return GameState.AUDIO_SCREEN

                if mouse_inside(event, controls_button, controls_x, controls_y):
                    return GameState.CONTROLS_SCREEN

        return next_state
