from clutch_draw.game_state import GameState

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
        font_apocalypse: Font,
        manager,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.font_apocalypse = font_apocalypse
        self.manager = manager

    def render(self, events: list[Event]) -> GameState:
        self.screen.fill("gray")
        font = Font(None, 74)
        text = font.render("Options Screen - Coming Soon!", True, Color(0, 0, 0))
        text_x = self.screen_width // 2 - text.get_width() // 2
        text_y = self.screen_height // 2 - text.get_height() // 2
        self.screen.blit(text, (text_x, text_y))

        back_button = create_button(self.font_apocalypse, "Back")
        back_button_x = self.screen_width // 2 - back_button.get_width() // 2
        back_button_y = self.screen_height - back_button.get_height() - 50
        self.screen.blit(back_button, (back_button_x, back_button_y))

        next_state = GameState.OPTIONS_SCREEN

        for event in events:
            if event.type == MOUSEBUTTONUP:
                if mouse_inside(event, back_button, back_button_x, back_button_y):
                    next_state = GameState.MAIN_MENU_SCREEN

        return next_state
