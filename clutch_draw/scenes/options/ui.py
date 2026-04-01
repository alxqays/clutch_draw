from clutch_draw.game_state import GameState
from pygame_gui import UIManager

from pygame import MOUSEBUTTONUP, Surface, Color
from pygame.font import Font
from pygame.event import Event

from clutch_draw.ui.buttons import create_button
from clutch_draw.ui.mouse import mouse_inside


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

    def render(self, events: list[Event]) -> GameState:

        self.screen.fill("grey")

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

        back_button = create_button(self.button_font, "Back")
        back_button_x = self.screen_width // 2 - back_button.get_width() // 2
        back_button_y = self.screen_height - back_button.get_height() - 50
        self.screen.blit(back_button, (back_button_x, back_button_y))

        next_state = GameState.OPTIONS_SCREEN

        for event in events:
            if event.type == MOUSEBUTTONUP:
                if mouse_inside(event, back_button, back_button_x, back_button_y):
                    next_state = GameState.MAIN_MENU_SCREEN

        return next_state
