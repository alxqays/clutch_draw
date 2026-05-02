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
FONTS_PATH = RESOURCES_PATH / "fonts"
IMAGES_PATH = RESOURCES_PATH / "images"


class AudioScreen:

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

        # Loading the background image using the path and scaling it to the screen's dimensions
        self.background = pygame.image.load(IMAGES_PATH / "orig_big.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.screen_width, self.screen_height)
        )

        # Getting the current volume of sound from the mixer and converting it into a percentage
        self.volume = int(pygame.mixer.music.get_volume() * 100)

    def render(self, events: list[Event]) -> GameState:

        # Drawing the background image onto the screen
        self.screen.blit(
            self.background, (0, 0)
        )  # (0, 0) refers to the top-left position of the screen

        # Drawing the same semi-transparent overlay that is in other screens, used to darken the background image
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(
            120
        )  # However, slightly darker/stronger in this screen as it is more of a functional screen
        overlay.fill((0, 0, 0))
        self.screen.blit(
            overlay, (0, 0)
        )  # (0, 0) refers to the top-left position of the screen

        # Rendering the screen's title text and an outline effect for it
        # "True" refers to the enabling of anti-aliasing
        main_text = self.title_font.render("Audio", True, Color(255, 255, 255))
        border_text = self.title_font.render("Audio", True, Color(0, 0, 0))

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

        # No custom font assigned for the volume text, "None" refers to Pygame's default font, "50" refers to its size
        volume_font = Font(None, 50)
        volume_text = volume_font.render(
            f"Volume: {self.volume}%", True, Color(255, 255, 255)
        )

        # Positioning the volume text, centring it with the screen, allowing space for the volume increase/decrease buttons underneath
        volume_x = self.screen_width // 2 - volume_text.get_width() // 2
        volume_y = self.screen_height // 2 + 20

        # Drawing the volume text onto the screen
        self.screen.blit(volume_text, (volume_x, volume_y))

        # Creating a font with a specific size for the "+" and "-" symbols which are used as volume controls
        symbol_font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 40)

        # Creating the "+" and "-" controls and a "Back" button with the same reusable button function
        up_control = symbol_font.render("+", True, (255, 255, 255))
        down_control = symbol_font.render("-", True, (255, 255, 255))
        back_button = create_button(self.button_font, "Back")

        # Positioning the volume controls relative to the centre of the screen, spacing them apart evenly, with the back button underneath the controls
        up_control_x = self.screen_width // 2 - up_control.get_width() - 40
        up_control_y = self.screen_height // 2 + 100
        down_control_x = self.screen_width // 2 + 40
        down_control_y = self.screen_height // 2 + 100
        back_button_x = self.screen_width // 2 - back_button.get_width() // 2
        back_button_y = self.screen_height - back_button.get_height() - 80

        # Drawing the buttons onto the screen
        self.screen.blit(down_control, (down_control_x, down_control_y))
        self.screen.blit(up_control, (up_control_x, up_control_y))
        self.screen.blit(back_button, (back_button_x, back_button_y))

        # Default state remains the same unless a button is clicked
        next_state = GameState.AUDIO_SCREEN

        # Processing all input events made by the user
        for event in events:
            if event.type == MOUSEBUTTONUP:

                # Checking if the user's mouse is inside the button's surface/rectangle and if it has been clicked on
                if mouse_inside(event, down_control, down_control_x, down_control_y):
                    # Decreasing the volume in 10s while ensuring it does not go below 0
                    self.volume = max(0, self.volume - 10)
                    pygame.mixer.music.set_volume(
                        self.volume / 100
                    )  # Converting the percentage into the range used by the mixer

                # Checking if the user's mouse is inside the button's surface/rectangle and if it has been clicked on
                if mouse_inside(event, up_control, up_control_x, up_control_y):
                    # Increasing the volume in 10s while ensuring it does not exceed 100
                    self.volume = min(100, self.volume + 10)
                    pygame.mixer.music.set_volume(
                        self.volume / 100
                    )  # Converting the percentage into the range used by the mixer

                # Checking if the user's mouse is inside the button's surface/rectangle and if it has been clicked on
                if mouse_inside(event, back_button, back_button_x, back_button_y):
                    next_state = GameState.OPTIONS_SCREEN
                    # If clicked, redirect the user to the next appropriate screen ("Options")

        # Returning the next game state so that the main game loop can handle the screen transitions and update the display
        return next_state
