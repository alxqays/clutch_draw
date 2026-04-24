from pygame_gui import UIManager
from clutch_draw.game_state import GameState

from pygame import MOUSEBUTTONUP, Surface, Color
from pygame.font import Font
from pygame.event import Event

from clutch_draw.ui.buttons import create_button
from clutch_draw.ui.mouse import mouse_inside

import pygame


class WelcomeScreen:

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

        main_text = self.title_font.render("Clutch Draw", True, Color(255, 255, 255))
        border_text = self.title_font.render("Clutch Draw", True, Color(0, 0, 0))

        text_x = self.screen_width // 2 - main_text.get_width() // 2
        text_y = self.screen_height // 2 - main_text.get_height() // 2 - 65

        border = 5

        self.screen.blit(border_text, (text_x - border, text_y))  # left
        self.screen.blit(border_text, (text_x + border, text_y))  # right
        self.screen.blit(border_text, (text_x, text_y - border))  # top
        self.screen.blit(border_text, (text_x, text_y + border))  # bottom

        self.screen.blit(main_text, (text_x, text_y))

        sign_in_button = create_button(self.button_font, "Sign In")
        sign_in_button_x = (
            self.screen_width // 2
            - sign_in_button.get_width() // 2
            - sign_in_button.get_width() // 2
            - 10
        )
        sign_in_button_y = self.screen_height - sign_in_button.get_height() - 275

        self.screen.blit(sign_in_button, (sign_in_button_x, sign_in_button_y))

        sign_up_button = create_button(self.button_font, "Sign Up")
        sign_up_button_x = (
            self.screen_width // 2
            - sign_up_button.get_width() // 2
            + sign_up_button.get_width() // 2
            + 10
        )
        sign_up_button_y = self.screen_height - sign_up_button.get_height() - 275

        self.screen.blit(sign_up_button, (sign_up_button_x, sign_up_button_y))

        next_state = GameState.WELCOME_SCREEN

        for event in events:
            if event.type == MOUSEBUTTONUP:
                if mouse_inside(
                    event, sign_in_button, sign_in_button_x, sign_in_button_y
                ):
                    next_state = GameState.SIGN_IN_SCREEN
                if mouse_inside(
                    event, sign_up_button, sign_up_button_x, sign_up_button_y
                ):
                    next_state = GameState.SIGN_UP_SCREEN

        return next_state
