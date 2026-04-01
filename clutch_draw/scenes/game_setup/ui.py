from pygame_gui import UIManager
from clutch_draw.game_state import GameState
from clutch_draw.ui.mouse import mouse_inside
from clutch_draw.ui.buttons import create_button

from pygame import MOUSEMOTION, MOUSEBUTTONUP, Surface
from pygame.event import Event
from pygame.font import Font


class GameSetupScreen:

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        screen: Surface,
        title_font: Font,
        manager: UIManager,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.title_font = title_font
        self.manager = manager

    def render(self, events: list[Event]) -> GameState:

        self.screen.fill("grey")
        back_button = create_button(self.title_font, "Back")
        back_button_x = self.screen_width // 2 - back_button.get_width() // 2
        back_button_y = self.screen_height // 2 - back_button.get_height() // 2 + 265
        self.screen.blit(back_button, (back_button_x, back_button_y))

        play_button = create_button(self.title_font, "Play")
        play_button_x = self.screen_width // 2 - play_button.get_width() // 2
        play_button_y = self.screen_height // 2 - play_button.get_height() // 2
        self.screen.blit(play_button, (play_button_x, play_button_y))

        next_state = GameState.GAME_SETUP_SCREEN

        for event in events:
            if event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            if event.type == MOUSEBUTTONUP:
                if mouse_inside(event, back_button, back_button_x, back_button_y):
                    next_state = GameState.MAIN_MENU_SCREEN
                elif mouse_inside(event, play_button, play_button_x, play_button_y):
                    next_state = GameState.GAME_SCREEN

        return next_state
