import pygame
from pygame_gui import UIManager
from clutch_draw.game_state import GameState
from pygame import MOUSEBUTTONUP, Surface, Color
from pygame.font import Font
from pygame.event import Event
from clutch_draw.ui.buttons import create_button
from clutch_draw.ui.mouse import mouse_inside

from pathlib import Path

# Defining file paths for resources
RESOURCES_PATH = Path(__file__).parent.parent.parent.parent / "resources"
IMAGES_PATH = RESOURCES_PATH / "images"


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
        # Storing screen dimensions so that they can be used when rendering UI elements
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        # Storing fonts for reuse when rendering text
        self.button_font = button_font
        self.title_font = title_font
        # Storing UIManager for handling UI updates and event processing
        self.manager = manager

        # Loading the background image using the image path and scaling it to the screens dimensions
        self.background = pygame.image.load(IMAGES_PATH / "orig_big.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.screen_width, self.screen_height)
        )

    def render(self, events: list[Event]) -> GameState:

        # Drawing the background image onto the screen
        self.screen.blit(
            self.background, (0, 0)
        )  # (0, 0) refers to the top-left position of the screen

        # Drawing a semi-transparent overlay to darken the background to imporve the contrast and UI element's visibility
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(
            60
        )  # The aplha value sets the opacity of the overlay, it is set at 60 for this screen because it is more of an actual game screen, so the background can remain more visible
        overlay.fill((0, 0, 0))  # The colour of the overlay
        self.screen.blit(
            overlay, (0, 0)
        )  # (0, 0) refers to the top-left position of the screen

        # Rendering the screen's title text and an outline effect for it
        # "True" refers to the enabling of anti-aliasing which ensures the text looks smooth and less pixelated
        main_text = self.title_font.render("Clutch Draw", True, Color(255, 255, 255))
        border_text = self.title_font.render("Clutch Draw", True, Color(0, 0, 0))

        # Calculating the positon of the title text, centring it on the screen
        text_x = self.screen_width // 2 - main_text.get_width() // 2
        text_y = (
            self.screen_height // 2 - main_text.get_height() // 2 - 65
        )  # Height adjustment from the centre to allow space for UI elements underneath

        border = 5  # The thickness of the outline

        # Drawing the outline by rendering it multiple times, each time with a slight offset
        self.screen.blit(border_text, (text_x - border, text_y))  # left
        self.screen.blit(border_text, (text_x + border, text_y))  # right
        self.screen.blit(border_text, (text_x, text_y - border))  # top
        self.screen.blit(border_text, (text_x, text_y + border))  # bottom

        self.screen.blit(
            main_text, (text_x, text_y)
        )  # The actual text is drawn on top of the outline

        # Creating the "Sign In" button using the reusable "create_button" function from the "buttons.py" file under the "ui" folder
        sign_in_button = create_button(self.button_font, "Sign In")
        # Positioning it slightly to the left to make space for the "Sign Up" button later
        sign_in_button_x = (
            self.screen_width // 2
            - sign_in_button.get_width() // 2
            - sign_in_button.get_width() // 2
            - 10
        )
        sign_in_button_y = self.screen_height - sign_in_button.get_height() - 275

        # Drawing it onto the screen
        self.screen.blit(sign_in_button, (sign_in_button_x, sign_in_button_y))

        # Creating the "Sign Up" button using the same function as before
        sign_up_button = create_button(self.button_font, "Sign Up")
        # Positioning it slightly to the right to ensure both buttons can be evenly spaced
        sign_up_button_x = (
            self.screen_width // 2
            - sign_up_button.get_width() // 2
            + sign_up_button.get_width() // 2
            + 10
        )
        sign_up_button_y = self.screen_height - sign_up_button.get_height() - 275

        # Drawing it onto the screen
        self.screen.blit(sign_up_button, (sign_up_button_x, sign_up_button_y))

        # Default state remains the same unless a button is clicked
        next_state = GameState.WELCOME_SCREEN

        # Processing all input events made by the user
        for event in events:
            if event.type == MOUSEBUTTONUP:

                # Checking if the user's mouse is inside the button's surface/rectangle and if it has been clicked on
                if mouse_inside(
                    event, sign_in_button, sign_in_button_x, sign_in_button_y
                ):
                    next_state = (
                        GameState.SIGN_IN_SCREEN
                    )  # Upon clicking, once the mouse is released (MOUSEBUTTONUP), the user gets redirected to the next appropriate screen, in this case that is the "Sign In" screen

                # Checking if the user's mouse is inside the button's surface/rectangle and if it has been clicked on
                if mouse_inside(
                    event, sign_up_button, sign_up_button_x, sign_up_button_y
                ):
                    next_state = (
                        GameState.SIGN_UP_SCREEN
                    )  # Upon clicking, once the mouse is released (MOUSEBUTTONUP), the user gets redirected to the next appropriate screen, in this case that is the "Sign Up" screen

        # Returning the next game state so that the main game loop in the "main" file can handle the screen transition and update which screen is displayed
        return next_state
