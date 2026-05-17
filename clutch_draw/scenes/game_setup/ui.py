import pygame
from pygame_gui import UIManager
from pygame import MOUSEBUTTONUP, Surface
from pygame.event import Event
from pygame.font import Font
from clutch_draw.game_state import GameState
from clutch_draw.ui.buttons import create_button
from clutch_draw.ui.mouse import mouse_inside

from pathlib import Path

# Defining file paths for resources
RESOURCES_PATH = Path(__file__).parent.parent.parent.parent / "resources"
FONTS_PATH = RESOURCES_PATH / "fonts"
IMAGES_PATH = RESOURCES_PATH / "images"


class GameSetupScreen:

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        screen: Surface,
        title_font: Font,
        manager: UIManager,
        user_data: dict,
    ):
        # Storing screen dimensions so that they can be used when rendering UI elements
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        # Storing font for reuse when rendering buttons and text
        self.title_font = title_font
        # Storing UIManager for handling UI updates and event processing
        self.manager = manager

        # Loading the background image using the path and scaling it to the screens dimensions
        self.background = pygame.image.load(IMAGES_PATH / "orig_big.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.screen_width, self.screen_height)
        )

        # Retrieving the player's level to determine if the competitive gamemode can be unlocked, and if so, which ranks within it can be unlocked
        self.level = user_data["level"]

        # Initialising default selections
        self.selected_mode = "casual"
        self.selected_rank = None

    def render(self, events: list[Event]) -> GameState:

        # Drawing the background image onto the screen
        self.screen.blit(
            self.background, (0, 0)
        )  # (0, 0) refers to the top-left position of the screen

        # Drawing the same semi-transparent overlay that is used in other screens
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(
            120
        )  # Darker for this screen as it is more of a functional screen
        overlay.fill((0, 0, 0))
        self.screen.blit(
            overlay, (0, 0)
        )  # (0, 0) refers to the top-left position of the screen

        # Creating all of the buttons for this screen using the same reusable button function as in other screens

        # Creates buttons for the gamemode selection
        casual_button = create_button(self.title_font, "Casual")
        comp_button = create_button(self.title_font, "Competitive")
        # Creates buttons for the competitive gamemode rank selection
        bronze_button = create_button(self.title_font, "Bronze")
        silver_button = create_button(self.title_font, "Silver")
        gold_button = create_button(self.title_font, "Gold")
        # Creates the "Play" which confirms these selections and the "Back" button
        play_button = create_button(self.title_font, "Play")
        back_button = create_button(self.title_font, "Back")

        # Positioning all of the buttons on the screen

        # Horizontal centre of the screen defined once to be used for consistent alignment
        centre_x = self.screen_width // 2

        casual_x = centre_x - casual_button.get_width() - 20
        casual_y = 200

        comp_x = centre_x + 20
        comp_y = 200

        bronze_x = centre_x - bronze_button.get_width() - 150
        silver_x = centre_x - silver_button.get_width() // 2
        gold_x = centre_x + 150
        rank_y = 350

        play_x = centre_x - play_button.get_width() // 2
        play_y = 500

        back_x = centre_x - back_button.get_width() // 2
        back_y = 580

        # Drawing the gamemode buttons onto the screen
        self.screen.blit(casual_button, (casual_x, casual_y))
        self.screen.blit(comp_button, (comp_x, comp_y))

        # If the competitive gamemode is locked for the player, draw a grey overlay on top of the button to show it can't be accessed
        if self.level < 5:
            overlay = pygame.Surface(
                (comp_button.get_width(), comp_button.get_height())
            )
            overlay.set_alpha(90)
            overlay.fill((100, 100, 100))
            self.screen.blit(overlay, (comp_x, comp_y))

        # Drawing/showing the rank buttons if the competitive mode is selected
        if self.selected_mode == "competitive":
            self.screen.blit(bronze_button, (bronze_x, rank_y))
            self.screen.blit(silver_button, (silver_x, rank_y))
            self.screen.blit(gold_button, (gold_x, rank_y))

        # Highlighting the selected mode with a green border around the button
        if self.selected_mode == "casual":

            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                (
                    casual_x,
                    casual_y,
                    casual_button.get_width(),
                    casual_button.get_height(),
                ),
                5,
            )

        elif self.selected_mode == "competitive":

            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                (comp_x, comp_y, comp_button.get_width(), comp_button.get_height()),
                5,
            )

        # Highlighting the selected rank with a green border around the button
        if self.selected_mode == "competitive":

            if self.selected_rank == "bronze":
                pygame.draw.rect(
                    self.screen,
                    (0, 255, 0),
                    (
                        bronze_x,
                        rank_y,
                        bronze_button.get_width(),
                        bronze_button.get_height(),
                    ),
                    5,
                )

            elif self.selected_rank == "silver":
                pygame.draw.rect(
                    self.screen,
                    (0, 255, 0),
                    (
                        silver_x,
                        rank_y,
                        silver_button.get_width(),
                        silver_button.get_height(),
                    ),
                    5,
                )

            elif self.selected_rank == "gold":
                pygame.draw.rect(
                    self.screen,
                    (0, 255, 0),
                    (gold_x, rank_y, gold_button.get_width(), gold_button.get_height()),
                    5,
                )

        # Drawing the "Play" and "Back" buttons onto the screen
        self.screen.blit(play_button, (play_x, play_y))
        self.screen.blit(back_button, (back_x, back_y))

        # Defining a font with a specific size for the gamemode unlock message
        font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 20)

        # Displaying the gamemode locked message if the player's level is below 5
        if self.level < 5:
            lock_text = font.render(
                "Competitive unlocks at Level 5", True, (225, 80, 80)
            )
            self.screen.blit(lock_text, (centre_x - lock_text.get_width() // 2, 300))

        # Displaying the rank unlock requirement message
        if self.selected_mode == "competitive":

            if self.level < 10:
                silver_text = font.render(
                    "Silver unlocks at Level 10", True, (255, 80, 80)
                )
                self.screen.blit(silver_text, (silver_x, rank_y + 60))

            if self.level < 15:
                gold_text = font.render("Gold unlocks at Level 15", True, (255, 80, 80))
                self.screen.blit(gold_text, (gold_x, rank_y + 60))

        # Default state remains the same unless a button is clicked
        next_state = GameState.GAME_SETUP_SCREEN

        # Processing all input events made by the user
        for event in events:
            if event.type == MOUSEBUTTONUP:

                # Checking if the user's mouse is inside the button's surface/rectangle and if it has been clicked on
                if mouse_inside(event, back_button, back_x, back_y):
                    next_state = GameState.MAIN_MENU_SCREEN
                    # If clicked, redirect the user to the next appropriate screen, in this case the "Main Menu" screen

                # Setting the gamemode and rank for the game if the "Casual" button has been clicked
                if mouse_inside(event, casual_button, casual_x, casual_y):
                    self.selected_mode = "casual"
                    self.selected_rank = None

                # Setting the gamemode for the game depending on what the user has clicked
                elif mouse_inside(event, comp_button, comp_x, comp_y):
                    # The gamemode will be competitive if the user has clicked the "Competitive" button and their level is at least 5
                    if self.level >= 5:
                        self.selected_mode = "competitive"
                    else:
                        self.selected_mode = "casual"

                # Setting the rank within the competitve gamemode depending on what the user has clicked and if they meet the level requirement
                if self.selected_mode == "competitive":

                    if mouse_inside(event, bronze_button, bronze_x, rank_y):
                        self.selected_rank = "bronze"

                    elif mouse_inside(event, silver_button, silver_x, rank_y):
                        if self.level >= 10:
                            self.selected_rank = "silver"

                    elif mouse_inside(event, gold_button, gold_x, rank_y):
                        if self.level >= 15:
                            self.selected_rank = "gold"

                if mouse_inside(event, play_button, play_x, play_y):

                    # Preventing the game from starting if the "Play" button has been clicked,
                    # but the user does not meet the requirements for the gamemode and rank they are trying to play in
                    if self.selected_mode == "competitive":

                        if self.level < 5:
                            next_state = GameState.GAME_SETUP_SCREEN

                        # Preventing start if competitive has been selected but a rank for it has not been selected
                        if not self.selected_rank:
                            next_state = GameState.GAME_SETUP_SCREEN

                        else:
                            # Storing the final confirmed selections so that the appropriate game can activate
                            self.final_mode = self.selected_mode
                            self.final_rank = self.selected_rank

                            next_state = GameState.GAME_SCREEN

                    else:
                        # Starting casual mode immediately as no rank selection is required
                        self.final_mode = self.selected_mode
                        self.final_rank = None

                        next_state = GameState.GAME_SCREEN

        # Returning the next game state so that the main game loop can handle the screen transitions and update the display
        return next_state
