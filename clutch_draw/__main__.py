import pygame

from pathlib import Path

from pygame_gui import UIManager

from clutch_draw.db.utils import Database
from clutch_draw.game_state import GameState
from clutch_draw.scenes.game.ui import GameScreen
from clutch_draw.scenes.game_setup.ui import GameSetupScreen
from clutch_draw.scenes.main_menu.ui import MainMenuScreen
from clutch_draw.scenes.options.ui import OptionsScreen
from clutch_draw.scenes.audio.ui import AudioScreen
from clutch_draw.scenes.controls.ui import ControlsScreen
from clutch_draw.scenes.sign_in.ui import SignInScreen
from clutch_draw.scenes.sign_up.ui import SignUpScreen
from clutch_draw.scenes.welcome.ui import WelcomeScreen

# Defining file paths for resources
RESOURCES_PATH = Path(__file__).parent.parent / "resources"
FONTS_PATH = RESOURCES_PATH / "fonts"
IMAGES_PATH = RESOURCES_PATH / "images"
SOUNDS_PATH = RESOURCES_PATH / "sounds"


def main():

    # Debugging output
    print("Launching Clutch Draw...")

    # Initialising pygame modules for audio
    pygame.init()
    pygame.mixer.init()

    # Loading and playing background music
    pygame.mixer.music.load(SOUNDS_PATH / "background.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Loops the music

    # State system controls which screen is currently active
    current_state: GameState = GameState.WELCOME_SCREEN
    next_state: GameState = GameState.WELCOME_SCREEN

    # Setting up display window dimensions
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))

    # The clock is used to control the frame rate of the game
    clock = pygame.time.Clock()

    # Loading the font and font sizes to be used across all UI
    font_apocalypse_size100 = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 100)
    font_apocalypse_size50 = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 50)
    font_apocalypse_size15 = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 15)

    # The UI manager handles UI elements (e.g. buttons) and processing events (actions preformed by the user, such as button clicks), updating and rendering them
    manager = UIManager(
        (screen_width, screen_height), theme_path="clutch_draw/ui/theme.json"
    )

    # Initialising the first screen the user will see when running the program
    welcome_screen = WelcomeScreen(
        screen_width,
        screen_height,
        screen,
        font_apocalypse_size50,
        font_apocalypse_size100,
        manager,
    )

    # Other screens are initialised as None and created only when needed
    sign_in_screen = None
    sign_up_screen = None
    main_menu_screen = None
    game_setup_screen = None
    options_screen = None
    audio_screen = None
    controls_screen = None
    game_screen = None

    # The database is used to store and retrieve user data such as XP, Level and Wins/Losses
    database = Database()
    user_data = None

    # MAIN GAME LOOP
    # Everything inside of the while loop runs continuously, once per frame / game loop

    while True:

        # Delta time is used as it ensures movement and animations remain consistent regardless of frame rate
        time_delta = clock.tick(60) / 1000

        # Retrieving all user input events
        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:
                print("Got the quit event")
                pygame.quit()
                raise SystemExit

            # Passing input events to UIManager so that UI elements can respond (e.g. button clicks)
            manager.process_events(event)

        # GAME-STATE-BASED SCREEN RENDERING
        # Depending on the game-state that the user has triggered, the appropriate screen for it will render
        # Each screen handles its own logic and returns the next state of the game

        if current_state == GameState.WELCOME_SCREEN:
            next_state = welcome_screen.render(events)

        elif current_state == GameState.SIGN_IN_SCREEN:
            next_state = sign_in_screen.render(events)

            # Storing logged-in user data once authentication is successful
            if hasattr(sign_in_screen, "logged_in_user"):
                user_data = sign_in_screen.logged_in_user

        elif current_state == GameState.SIGN_UP_SCREEN:
            next_state = sign_up_screen.render(events)

            # Checking if a new account has been successfully created and retrieving the user data to initialise account
            if hasattr(sign_up_screen, "created_user"):
                user_data = sign_up_screen.created_user

        elif current_state == GameState.MAIN_MENU_SCREEN:
            next_state = main_menu_screen.render(events)

        elif current_state == GameState.GAME_SETUP_SCREEN:
            next_state = game_setup_screen.render(events)

        elif current_state == GameState.OPTIONS_SCREEN:
            next_state = options_screen.render(events)

        elif current_state == GameState.AUDIO_SCREEN:
            next_state = audio_screen.render(events)

        elif current_state == GameState.CONTROLS_SCREEN:
            next_state = controls_screen.render(events)

        elif current_state == GameState.GAME_SCREEN:
            next_state = game_screen.render(events)

        else:
            # Safety check to ensure all states are handled
            raise Exception(f"You forgot to handle a game state of {current_state}!")

        # GAME-STATE TRANSITION HANDLING
        # Creates new screen objects when changing the state of the game

        if current_state != next_state:
            # Resetting UI elements when switching screens
            manager.clear_and_reset()

            if next_state == GameState.SIGN_IN_SCREEN:
                sign_in_screen = SignInScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    font_apocalypse_size100,
                    manager,
                    database,
                )

            if next_state == GameState.SIGN_UP_SCREEN:
                sign_up_screen = SignUpScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    font_apocalypse_size100,
                    manager,
                    database,
                )

            if next_state == GameState.WELCOME_SCREEN:
                welcome_screen = WelcomeScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    font_apocalypse_size100,
                    manager,
                )

            if next_state == GameState.MAIN_MENU_SCREEN:

                # Retrieving user data from the database
                account = database.get_account(user_data["username"])

                username, _, xp, level, wins, losses = (
                    account  # "_" is used to ignore the password value returned by the database as it is not needed here.
                )

                # Storing user data in a structured dictionary
                user_data = {
                    "username": username,
                    "xp": xp,
                    "level": level,
                    "wins": wins,
                    "losses": losses,
                }

                main_menu_screen = MainMenuScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    font_apocalypse_size100,
                    manager,
                    user_data,
                )

            if next_state == GameState.GAME_SETUP_SCREEN:
                game_setup_screen = GameSetupScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    manager,
                    user_data,
                )  # User data is required in the game-setup screen in order to restrict play in competitive ranks based on player level.

            if next_state == GameState.OPTIONS_SCREEN:
                options_screen = OptionsScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    font_apocalypse_size100,
                    manager,
                )

            if next_state == GameState.AUDIO_SCREEN:
                audio_screen = AudioScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    font_apocalypse_size100,
                    manager,
                )

            if next_state == GameState.CONTROLS_SCREEN:
                controls_screen = ControlsScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    font_apocalypse_size100,
                    manager,
                )

            if next_state == GameState.GAME_SCREEN:

                # Default game settings
                mode = "casual"
                rank = None

                # Retrieving selected settings from the "Game Setup Screen" if they are available
                if game_setup_screen is not None:
                    mode = getattr(game_setup_screen, "final_mode", "casual")
                    rank = getattr(game_setup_screen, "final_rank", None)

                # Initialising main gameplay screen
                game_screen = GameScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    font_apocalypse_size15,
                    manager,
                    user_data,
                    mode=mode,
                    rank=rank,
                )

        # Updating the current game-state for the next frame
        current_state = next_state

        # Updating the UI elements and animations
        manager.update(time_delta)
        manager.draw_ui(screen)

        # Updating the display to show the user all the rendered changes
        pygame.display.flip()


# Entry point of the program
if __name__ == "__main__":
    main()
