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


class MainMenuScreen:

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        screen: Surface,
        button_font: Font,
        title_font: Font,
        manager: UIManager,
        user_data: dict,
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

        # Extracting user data passed from the login system
        self.username = user_data["username"]
        self.xp = user_data["xp"]
        self.level = user_data["level"]
        self.xp_to_next = (
            100 + (self.level - 1) * 50
        )  # Calculating the XP required for the next level
        self.wins = user_data["wins"]
        self.losses = user_data["losses"]

        # Small player profile box in the top right corner of the screen
        self.profile_rect = pygame.Rect(self.screen_width - 260, 30, 210, 55)
        # Expanded player profile box that appears when the user's mouse is hovered over it
        self.profile_expanded_rect = pygame.Rect(self.screen_width - 320, 30, 300, 230)

    def render(self, events: list[Event]) -> GameState:

        # Loading fonts with specific sizes for profile UI elements
        title_font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 32)
        text_font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 20)
        small_font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 16)

        # Creating the buttons for this screen using the same reusable button function as in other screens
        play_button = create_button(self.button_font, "Play")
        options_button = create_button(self.button_font, "Options")
        exit_button = create_button(self.button_font, "Exit")

        # Drawing the background image onto the screen
        self.screen.blit(
            self.background, (0, 0)
        )  # (0, 0) refers to the top-left position of the screen

        # Drawing the same semi-transparent overlay that is in other screens, used to darken the background image
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(
            60
        )  # However, lighter for this screen as it is more of an actual game screen, so the background can remain more visible
        overlay.fill((0, 0, 0))
        self.screen.blit(
            overlay, (0, 0)
        )  # (0, 0) refers to the top-left position of the screen

        # Rendering the screen's title text and an outline effect for it
        # "True" refers to the enabling of anti-aliasing
        title_text = self.title_font.render("Main Menu", True, Color(255, 255, 255))
        border_text = self.title_font.render("Main Menu", True, Color(0, 0, 0))

        # Calculating the position of the title text, centring it on the screen
        title_x = self.screen_width // 2 - title_text.get_width() // 2
        title_y = (
            self.screen_height // 2 - title_text.get_height() // 2 - 65
        )  # Height adjustment from the centre to allow space for UI elements underneath

        border = 5  # Thickness of the outline

        # Drawing the outline by rendering it multiple times, each time with a slight offset
        self.screen.blit(border_text, (title_x - border, title_y))  # left
        self.screen.blit(border_text, (title_x + border, title_y))  # right
        self.screen.blit(border_text, (title_x, title_y - border))  # top
        self.screen.blit(border_text, (title_x, title_y + border))  # bottom

        self.screen.blit(
            title_text, (title_x, title_y)
        )  # The actual text is drawn on top of the outline

        # Positioning of all the buttons underneath the title text, centring them with the screen but spacing them out between each other
        play_button_x = self.screen_width // 2 - play_button.get_width() // 2
        play_button_y = self.screen_height - play_button.get_height() - 280
        options_button_x = self.screen_width // 2 - options_button.get_width() // 2
        options_button_y = self.screen_height - options_button.get_height() - 180
        exit_button_x = self.screen_width // 2 - exit_button.get_width() // 2
        exit_button_y = self.screen_height - exit_button.get_height() - 80

        # Drawing them onto the screen
        self.screen.blit(play_button, (play_button_x, play_button_y))
        self.screen.blit(options_button, (options_button_x, options_button_y))
        self.screen.blit(exit_button, (exit_button_x, exit_button_y))

        # Default state remains the same unless a button is clicked
        next_state = GameState.MAIN_MENU_SCREEN

        # Processing all input events made by the user
        for event in events:
            if event.type == MOUSEBUTTONUP:

                # Checking if the user's mouse is inside the button's surface/rectangle and if it has been clicked on
                if mouse_inside(event, play_button, play_button_x, play_button_y):
                    next_state = GameState.GAME_SETUP_SCREEN
                    # If clicked, redirect the user to the appropriate screen, "Play" = "Game Setup" screen

                # Checking if the user's mouse is inside the button's surface/rectangle and if it has been clicked on
                if mouse_inside(
                    event, options_button, options_button_x, options_button_y
                ):
                    next_state = GameState.OPTIONS_SCREEN
                    # If clicked, redirect the user to the appropriate screen, "Options" = "Options" screen

                # Checking if the user's mouse is inside the button's surface/rectangle and if it has been clicked on
                if mouse_inside(event, exit_button, exit_button_x, exit_button_y):
                    print("Exit clicked")
                    pygame.quit()
                    raise SystemExit  # If clicked, the program closes

        # Getting the position of the user's mouse to detect hovering over the player profile box
        mouse_pos = pygame.mouse.get_pos()
        hovering_profile = self.profile_rect.collidepoint(mouse_pos)

        # Drawing the player profile box area
        pygame.draw.rect(self.screen, (0, 0, 0), self.profile_rect)

        # Drawing the level circle
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            (self.profile_rect.x + 30, self.profile_rect.y + 30),
            18,
        )

        # Fonts with specific sizes for the player profile box
        name_font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 26)
        level_font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 24)

        # Rendering the level number inside of the circle
        level_text = level_font.render(str(self.level), True, (0, 0, 0))
        self.screen.blit(
            level_text,
            (
                self.profile_rect.x + 30 - level_text.get_width() // 2,
                self.profile_rect.y + 30 - level_text.get_height() // 2,
            ),
        )

        # Rendering the player's username next to the level
        username_text = name_font.render(self.username, True, (255, 255, 255))
        self.screen.blit(
            username_text,
            (self.profile_rect.x + 65, self.profile_rect.y + 15),
        )

        # Expanding the player profile box when the user's mouse is hovered over it
        if hovering_profile:

            pygame.draw.rect(self.screen, (0, 0, 0), self.profile_expanded_rect)
            pygame.draw.rect(
                self.screen, (255, 255, 255), self.profile_expanded_rect, 2
            )

            # Layout spacing
            padding = 12
            line_gap = 38

            # Calculating the starting position so that all of the profile text is algined with consistent padding used for spacing
            start_x = self.profile_expanded_rect.x + padding
            start_y = self.profile_expanded_rect.y + padding

            # Rendering the username and level displays
            title_surface = title_font.render(
                f"(Lvl {self.level}) {self.username} ", True, (255, 255, 255)
            )

            # Rendering the XP display
            xp_surface = text_font.render(
                f"XP: {self.xp}/{self.xp_to_next}", True, (255, 255, 255)
            )

            # Rendering the wins and losses displays
            wins_surface = text_font.render(f"Wins: {self.wins}", True, (255, 255, 255))

            losses_surface = text_font.render(
                f"Losses: {self.losses}", True, (255, 255, 255)
            )

            # Calculating and rendering the total number of games played by the user
            total_games = self.wins + self.losses
            total_surface = text_font.render(
                f"Games: {total_games}", True, (255, 255, 255)
            )

            # Competitive unlock condition with text rendered for it onto the player profile
            unlock_colour = (0, 255, 0) if self.level >= 5 else (255, 80, 80)
            unlock_surface = small_font.render(
                (
                    "Competitive Unlocked"
                    if self.level >= 5
                    else "Competitive unlocks at Level 5"
                ),
                True,
                unlock_colour,
            )

            # Drawing all of the profile information
            self.screen.blit(title_surface, (start_x, start_y))
            self.screen.blit(xp_surface, (start_x, start_y + line_gap))
            self.screen.blit(wins_surface, (start_x, start_y + line_gap * 2))
            self.screen.blit(losses_surface, (start_x, start_y + line_gap * 3))
            self.screen.blit(total_surface, (start_x, start_y + line_gap * 4))
            self.screen.blit(unlock_surface, (start_x, start_y + line_gap * 5))

        # Returning the next game state so that the main game loop can handle the screen transitions and update the display
        return next_state
