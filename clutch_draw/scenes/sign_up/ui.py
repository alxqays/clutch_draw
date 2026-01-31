from pygame_gui import UIManager
from clutch_draw.db.utils import Database
from clutch_draw.game_state import GameState
from pygame_gui.elements import UITextEntryLine, UILabel

from pygame import MOUSEBUTTONUP, Rect, Surface, Color
from pygame.font import Font
from pygame.event import Event

from clutch_draw.ui.buttons import create_button
from clutch_draw.ui.mouse import mouse_inside

import pygame


class SignUpScreen:

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        screen: Surface,
        font_apocalypse_50: Font,
        font_apocalypse_100: Font,
        manager: UIManager,
        database: Database,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.button_font = font_apocalypse_50
        self.title_font = font_apocalypse_100
        self.manager = manager
        self.database = database

        sign_up_box_width = 350
        sign_up_box_height = 50

        username_input_x = screen_width // 2 - sign_up_box_width // 2
        username_input_y = screen_height // 2 - sign_up_box_height // 2
        self.username_input_label = UILabel(
            relative_rect=Rect(
                (username_input_x - 175 // 2, username_input_y),
                (-1, sign_up_box_height),
            ),
            text="Username:",
            manager=manager,
        )

        self.username_input = UITextEntryLine(
            relative_rect=Rect(
                (username_input_x, username_input_y),
                (sign_up_box_width, sign_up_box_height),
            ),
            manager=manager,
        )

        password_input_x = screen_width // 2 - sign_up_box_width // 2
        password_input_y = screen_height // 2 - sign_up_box_height // 2 + 50
        self.password_input_label = UILabel(
            relative_rect=Rect(
                (password_input_x - 165 // 2, password_input_y),
                (-1, sign_up_box_height),
            ),
            text="Password:",
            manager=manager,
        )
        self.password_input = UITextEntryLine(
            relative_rect=Rect(
                (password_input_x, password_input_y),
                (sign_up_box_width, sign_up_box_height),
            ),
            manager=manager,
        )
        verify_password_input_x = screen_width // 2 - sign_up_box_width // 2
        verify_password_input_y = screen_height // 2 - sign_up_box_height // 2 + 100
        self.verify_password_input_label = UILabel(
            relative_rect=Rect(
                (
                    verify_password_input_x - 250 // 2,
                    verify_password_input_y,
                ),
                (-1, sign_up_box_height),
            ),
            text="Verify Password:",
            manager=manager,
        )
        self.verify_password_input = UITextEntryLine(
            relative_rect=Rect(
                (verify_password_input_x, verify_password_input_y),
                (sign_up_box_width, sign_up_box_height),
            ),
            manager=manager,
        )

        self.error = None

    def render(self, events: list[Event]) -> GameState:

        self.screen.fill("grey")

        main_text = self.title_font.render("Sign Up", True, Color(255, 255, 255))
        border_text = self.title_font.render("Sign Up", True, Color(0, 0, 0))

        text_x = self.screen_width // 2 - main_text.get_width() // 2
        text_y = self.screen_height // 2 - main_text.get_height() // 2 - 65

        border = 5

        self.screen.blit(border_text, (text_x - border, text_y))  # left
        self.screen.blit(border_text, (text_x + border, text_y))  # right
        self.screen.blit(border_text, (text_x, text_y - border))  # top
        self.screen.blit(border_text, (text_x, text_y + border))  # bottom

        self.screen.blit(main_text, (text_x, text_y))

        sign_up_button = create_button(self.button_font, "Sign Up")
        sign_up_button_x = self.screen_width // 2 - sign_up_button.get_width() // 2
        sign_up_button_y = self.screen_height - sign_up_button.get_height() - 110
        self.screen.blit(sign_up_button, (sign_up_button_x, sign_up_button_y))

        if self.error is not None:
            error_font = Font(None, 36)
            error_text = error_font.render(self.error, True, Color(255, 255, 255))
            error_x = self.screen_width // 2 - error_text.get_width() // 2
            error_y = sign_up_button_y - 35
            self.screen.blit(error_text, (error_x, error_y))

        next_state = GameState.SIGN_UP_SCREEN

        for event in events:
            if event.type == MOUSEBUTTONUP:
                if mouse_inside(
                    event, sign_up_button, sign_up_button_x, sign_up_button_y
                ):
                    username = self.username_input.get_text()
                    password = self.password_input.get_text()
                    verify_password = self.verify_password_input.get_text()

                    if verify_password != password:
                        self.error = "Error: Passwords do not match"
                        continue

                    if self.database.account_exists(username):
                        self.error = "Error: Username already taken"
                        continue

                    self.database.insert_account(username, password)
                    next_state = GameState.MAIN_MENU_SCREEN

        return next_state
