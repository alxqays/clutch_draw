from clutch_draw.game_state import GameState
from clutch_draw.ui.mouse import mouse_inside
from clutch_draw.ui.buttons import create_button

from pygame.font import Font
from pygame.surface import Surface
from pygame.event import Event

import pygame


class MainMenuScreen:

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        screen: Surface,
        font_apocalypse: Font,
        manager,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.font_apocalypse = font_apocalypse
        self.manager = manager

    def render(self, events: list[Event]) -> GameState:
        play_button = create_button(self.font_apocalypse, "Play")
        options_button = create_button(self.font_apocalypse, "Options")
        credits_button = create_button(self.font_apocalypse, "Credits")
        exit_button = create_button(self.font_apocalypse, "Exit")
        self.screen.fill("purple")  # Fill the display with a solid color
        title_text = self.font_apocalypse.render(
            "Clutch Draw", True, pygame.Color(0, 0, 0)
        )
        title_x = self.screen_width // 2 - title_text.get_width() // 2
        title_y = self.screen_height // 2 - title_text.get_height() // 2
        play_button_x = title_x
        play_button_y = title_y + 100
        options_button_x = title_x
        options_button_y = title_y + 200
        credits_button_x = title_x
        credits_button_y = title_y + 300
        exit_button_x = title_x
        exit_button_y = title_y + 400

        self.screen.blit(title_text, (title_x, title_y))
        self.screen.blit(play_button, (play_button_x, play_button_y))
        self.screen.blit(options_button, (options_button_x, options_button_y))
        self.screen.blit(credits_button, (credits_button_x, credits_button_y))
        self.screen.blit(exit_button, (exit_button_x, exit_button_y))

        next_state = GameState.MAIN_MENU_SCREEN

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if mouse_inside(event, play_button, play_button_x, play_button_y):
                    next_state = GameState.GAME_SETUP_SCREEN
                if mouse_inside(
                    event, options_button, options_button_x, options_button_y
                ):
                    next_state = GameState.OPTIONS_SCREEN
                if mouse_inside(
                    event, credits_button, credits_button_x, credits_button_y
                ):
                    next_state = GameState.CREDITS_SCREEN
                if mouse_inside(event, exit_button, exit_button_x, exit_button_y):
                    print("Exit clicked")
                    pygame.quit()
                    raise SystemExit

        return next_state
