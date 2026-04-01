from pygame_gui import UIManager
from clutch_draw.game_state import GameState
from clutch_draw.ui.mouse import mouse_inside
from clutch_draw.ui.buttons import create_button

from pygame.font import Font
from pygame import MOUSEBUTTONUP, Surface, Color
from pygame.event import Event

import pygame


class MainMenuScreen:

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

    def render(self, events: list[Event]) -> GameState:

        play_button = create_button(self.button_font, "Play")
        options_button = create_button(self.button_font, "Options")
        exit_button = create_button(self.button_font, "Exit")

        self.screen.fill("grey")

        title_text = self.title_font.render("Main Menu", True, Color(255, 255, 255))
        border_text = self.title_font.render("Main Menu", True, Color(0, 0, 0))

        title_x = self.screen_width // 2 - title_text.get_width() // 2
        title_y = self.screen_height // 2 - title_text.get_height() // 2 - 65

        border = 5

        self.screen.blit(border_text, (title_x - border, title_y))  # left
        self.screen.blit(border_text, (title_x + border, title_y))  # right
        self.screen.blit(border_text, (title_x, title_y - border))  # top
        self.screen.blit(border_text, (title_x, title_y + border))  # bottom

        self.screen.blit(title_text, (title_x, title_y))

        play_button_x = self.screen_width // 2 - play_button.get_width() // 2
        play_button_y = self.screen_height - play_button.get_height() - 280
        options_button_x = self.screen_width // 2 - options_button.get_width() // 2
        options_button_y = self.screen_height - options_button.get_height() - 180
        exit_button_x = self.screen_width // 2 - exit_button.get_width() // 2
        exit_button_y = self.screen_height - exit_button.get_height() - 80

        self.screen.blit(play_button, (play_button_x, play_button_y))
        self.screen.blit(options_button, (options_button_x, options_button_y))
        self.screen.blit(exit_button, (exit_button_x, exit_button_y))

        next_state = GameState.MAIN_MENU_SCREEN

        for event in events:

            if event.type == MOUSEBUTTONUP:
                if mouse_inside(event, play_button, play_button_x, play_button_y):
                    next_state = GameState.GAME_SETUP_SCREEN
                if mouse_inside(
                    event, options_button, options_button_x, options_button_y
                ):
                    next_state = GameState.OPTIONS_SCREEN
                if mouse_inside(event, exit_button, exit_button_x, exit_button_y):
                    print("Exit clicked")
                    pygame.quit()
                    raise SystemExit

        return next_state
