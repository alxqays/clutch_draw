from typing import Optional
from pygame_gui import UIManager
from pygame_gui.core import ObjectID
from pygame_gui.elements import UITextEntryLine, UILabel
from clutch_draw.db.utils import Database
from clutch_draw.game_state import GameState

from pygame import MOUSEBUTTONUP, Rect, Surface, Color
from pygame.font import Font
from pygame.event import Event

from clutch_draw.ui.buttons import create_button
from clutch_draw.ui.mouse import mouse_inside


class SignInScreen:

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        screen: Surface,
        font_apocalypse: Font,
        manager: UIManager,
        database: Database,
    ):

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.font_apocalypse = font_apocalypse
        self.manager = manager
        self.database = database

        sign_in_box_width = 350
        sign_in_box_height = 50

        username_input_x = screen_width // 2 - sign_in_box_width // 2
        username_input_y = screen_height // 2 - sign_in_box_height // 2 + 100
        self.username_input_label = UILabel(
            relative_rect=Rect(
                (username_input_x - sign_in_box_width // 2, username_input_y),
                (-1, sign_in_box_height),
            ),
            text="Username:",
            manager=manager,
        )

        self.username_input = UITextEntryLine(
            relative_rect=Rect(
                (username_input_x, username_input_y),
                (sign_in_box_width, sign_in_box_height),
            ),
            manager=manager,
        )

        password_input_x = screen_width // 2 - sign_in_box_width // 2
        password_input_y = screen_height // 2 - sign_in_box_height // 2 + 150
        self.password_input_label = UILabel(
            relative_rect=Rect(
                (password_input_x - sign_in_box_width // 2, password_input_y),
                (-1, sign_in_box_height),
            ),
            text="Password:",
            manager=manager,
        )
        self.password_input = UITextEntryLine(
            relative_rect=Rect(
                (password_input_x, password_input_y),
                (sign_in_box_width, sign_in_box_height),
            ),
            manager=manager,
        )

        self.error = None

    def render(self, events: list[Event]) -> GameState:
        self.screen.fill("gray")
        font = Font(None, 74)
        text = font.render("Sign In", True, Color(0, 0, 0))
        text_x = self.screen_width // 2 - text.get_width() // 2
        text_y = self.screen_height // 2 - text.get_height() // 2
        self.screen.blit(text, (text_x, text_y))

        sign_in_button = create_button(self.font_apocalypse, "Sign In")
        sign_in_button_x = self.screen_width // 2 - sign_in_button.get_width() // 2
        sign_in_button_y = self.screen_height - sign_in_button.get_height() - 50
        self.screen.blit(sign_in_button, (sign_in_button_x, sign_in_button_y))

        if self.error is not None:
            error_font = Font(None, 36)
            error_text = error_font.render(self.error, True, Color(255, 0, 0))
            error_x = self.screen_width // 2 - error_text.get_width() // 2
            error_y = sign_in_button_y - 50
            self.screen.blit(error_text, (error_x, error_y))

        next_state = GameState.SIGN_IN_SCREEN

        for event in events:
            if event.type == MOUSEBUTTONUP:
                if mouse_inside(
                    event, sign_in_button, sign_in_button_x, sign_in_button_y
                ):
                    account = self.database.get_account(self.username_input.get_text())
                    if account is None:
                        self.error = "Username does not exist."
                        continue

                    _, stored_password = account
                    if self.password_input.get_text() != stored_password:
                        self.error = "Invalid password."
                        continue

                    next_state = GameState.MAIN_MENU_SCREEN

        return next_state
