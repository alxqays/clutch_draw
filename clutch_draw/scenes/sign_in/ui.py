import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UITextEntryLine, UILabel
from clutch_draw.db.utils import Database
from clutch_draw.game_state import GameState
from pygame import MOUSEBUTTONUP, Rect, Surface, Color
from pygame.font import Font
from pygame.event import Event
from clutch_draw.ui.buttons import create_button
from clutch_draw.ui.mouse import mouse_inside

from pathlib import Path

# Defining file paths for resources
RESOURCES_PATH = Path(__file__).parent.parent.parent.parent / "resources"
IMAGES_PATH = RESOURCES_PATH / "images"


class SignInScreen:

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
        # Storing screen dimensions so that they can be used when rendering UI elements
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        # Storing fonts (in different sizes) for reuse when rendering text
        self.button_font = font_apocalypse_50
        self.title_font = font_apocalypse_100
        # Storing UIManager for handling UI updates and event processing
        self.manager = manager
        # Storing the database to retrieve account information from it
        self.database = database

        # Loading the background image using the path and scaling it to the screen's dimensions
        self.background = pygame.image.load(IMAGES_PATH / "orig_big.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.screen_width, self.screen_height)
        )

        # Dimensions for the input boxes
        sign_in_box_width = 350
        sign_in_box_height = 50

        # Positioning for the username input box
        username_input_x = screen_width // 2 - sign_in_box_width // 2
        username_input_y = screen_height // 2 - sign_in_box_height // 2

        # Label and label positioning for the username input box
        self.username_input_label = UILabel(
            relative_rect=Rect(
                (username_input_x - 175 // 2, username_input_y),
                (-1, sign_in_box_height),
            ),
            text="Username:",
            manager=manager,
        )

        # Username input box creation
        self.username_input = UITextEntryLine(
            relative_rect=Rect(
                (username_input_x, username_input_y),
                (sign_in_box_width, sign_in_box_height),
            ),
            manager=manager,
        )

        # Positioning for the password input box
        password_input_x = screen_width // 2 - sign_in_box_width // 2
        password_input_y = screen_height // 2 - sign_in_box_height // 2 + 50

        # Label and label positioning for the password input box
        self.password_input_label = UILabel(
            relative_rect=Rect(
                (password_input_x - 165 // 2, password_input_y),
                (-1, sign_in_box_height),
            ),
            text="Password:",
            manager=manager,
        )

        # Password input box creation
        self.password_input = UITextEntryLine(
            relative_rect=Rect(
                (password_input_x, password_input_y),
                (sign_in_box_width, sign_in_box_height),
            ),
            manager=manager,
        )

        # Storing error messages so that they can be displayed to the user if need be
        self.error = None

    def render(self, events: list[Event]) -> GameState:

        # Drawing the background image onto the screen
        self.screen.blit(
            self.background, (0, 0)
        )  # (0, 0) refers to the top-left position of the screen

        # Drawing the same semi-transparent overlay that is in the "Welcome Screen", used to darken the background image
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(
            120
        )  # However, slightly darker/stronger in the "Sign In" screen as it is more of a functional screen
        overlay.fill((0, 0, 0))
        self.screen.blit(
            overlay, (0, 0)
        )  # (0, 0) refers to the top-left position of the screen

        # Rendering the screen's title text and an outline effect for it
        # "True" refers to the enabling of anti-aliasing
        main_text = self.title_font.render("Sign In", True, Color(255, 255, 255))
        border_text = self.title_font.render("Sign In", True, Color(0, 0, 0))

        # Calculating the position of the title text, centring it on the screen
        text_x = self.screen_width // 2 - main_text.get_width() // 2
        text_y = (
            self.screen_height // 2 - main_text.get_height() // 2 - 65
        )  # Height adjustment from the centre to allow space for UI elements underneath

        border = 5  # Thickness of the outline

        # Drawing the outline by rendering it multiple times, each time with a slight offset
        self.screen.blit(border_text, (text_x - border, text_y))  # left
        self.screen.blit(border_text, (text_x + border, text_y))  # right
        self.screen.blit(border_text, (text_x, text_y - border))  # top
        self.screen.blit(border_text, (text_x, text_y + border))  # bottom

        # The actual text is drawn on top of the outline
        self.screen.blit(main_text, (text_x, text_y))

        # Creating the "Sign In" button using the same reusable button function as in other screens
        sign_in_button = create_button(self.button_font, "Sign In")
        # Positioning it on top of the "Back" button
        sign_in_button_x = self.screen_width // 2 - sign_in_button.get_width() // 2
        sign_in_button_y = self.screen_height - sign_in_button.get_height() - 165

        # Creating the "Back" button using the same reusable button function as in other screens
        back_button = create_button(self.button_font, "Back")
        # Positioning it underneath the "Sign In" button
        back_button_x = self.screen_width // 2 - back_button.get_width() // 2
        back_button_y = sign_in_button_y + 80

        # Drawing the buttons onto the screen
        self.screen.blit(sign_in_button, (sign_in_button_x, sign_in_button_y))
        self.screen.blit(back_button, (back_button_x, back_button_y))

        # Displaying error messages if they exist
        if self.error is not None:
            error_font = Font(
                None, 36
            )  # No custom font assigned, "None" refers to Pygame's default font, "36" refers to its size
            error_text = error_font.render(
                self.error, True, Color(255, 255, 255)
            )  # "True" refers to the enabling of anti-aliasing
            # Positioning of the error message
            error_x = self.screen_width // 2 - error_text.get_width() // 2
            error_y = sign_in_button_y - 35
            # Drawing it onto the screen
            self.screen.blit(error_text, (error_x, error_y))

        # Default state remains the same unless login is successful
        next_state = GameState.SIGN_IN_SCREEN

        # Processing all input events made by the user
        for event in events:
            if event.type == MOUSEBUTTONUP:

                # Checking if the user's mouse is inside the button's surface/rectangle and if it has been clicked on
                if mouse_inside(
                    event, sign_in_button, sign_in_button_x, sign_in_button_y
                ):

                    # If clicked, retrieve the user's inputs and perform the validation checks below
                    # "strip()" removes whitespaces to prevent empty inputs such as " " from being treated as valid
                    username = self.username_input.get_text().strip()
                    password = self.password_input.get_text().strip()

                    if username == "" or password == "":
                        self.error = "Error: Fields cannot be left empty"
                        continue

                    # Retrieving the account from the database
                    account = self.database.get_account(username)

                    if account is None:
                        self.error = "Error: Username does not exist"
                        continue

                    # Unpacking stored user data
                    username, stored_password, xp, level, wins, losses = account

                    if password != stored_password:
                        self.error = "Error: Invalid password"
                        continue

                    # Storing logged in user data for use in other screens
                    self.logged_in_user = {
                        "username": username,
                        "xp": xp,
                        "level": level,
                        "wins": wins,
                        "losses": losses,
                    }

                    # Redirect the user to the next appropriate screen if login is successful, in this case "Main Menu"
                    next_state = GameState.MAIN_MENU_SCREEN

                # Redirecting the user back to the appropriate screen, "Welcome Screen", if the back button has been clicked
                if mouse_inside(event, back_button, back_button_x, back_button_y):
                    next_state = GameState.WELCOME_SCREEN

        # Returning the next game state so that the main game loop can handle the screen transitions and update the display
        return next_state
