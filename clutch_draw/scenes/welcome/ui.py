from clutch_draw.game_state import GameState

from pygame import MOUSEBUTTONUP, Surface, Color
from pygame.font import Font
from pygame.event import Event

from clutch_draw.ui.buttons import create_button
from clutch_draw.ui.mouse import mouse_inside


class WelcomeScreen:

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
        text = font.render("Welcome to Clutch Draw!", True, Color(0, 0, 0))
        text_x = self.screen_width // 2 - text.get_width() // 2
        text_y = self.screen_height // 2 - text.get_height() // 2
        self.screen.blit(text, (text_x, text_y))

        sign_in_button = create_button(self.font_apocalypse, "Sign In")
        sign_in_button_x = (
            self.screen_width // 2
            - sign_in_button.get_width() // 2
            - sign_in_button.get_width() // 2
            - 10
        )
        sign_in_button_y = self.screen_height - sign_in_button.get_height() - 50
        self.screen.blit(sign_in_button, (sign_in_button_x, sign_in_button_y))

        sign_up_button = create_button(self.font_apocalypse, "Sign Up")
        sign_up_button_x = (
            self.screen_width // 2
            - sign_up_button.get_width() // 2
            + sign_up_button.get_width() // 2
            + 10
        )
        sign_up_button_y = self.screen_height - sign_up_button.get_height() - 50
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
