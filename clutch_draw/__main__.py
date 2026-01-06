import pygame
from pathlib import Path

from pygame_gui import UIManager

from clutch_draw.db.utils import Database
from clutch_draw.game_state import GameState
from clutch_draw.scenes.credits.ui import CreditsScreen
from clutch_draw.scenes.game.ui import GameScreen
from clutch_draw.scenes.game_setup.ui import GameSetupScreen
from clutch_draw.scenes.main_menu.ui import MainMenuScreen
from clutch_draw.scenes.options.ui import OptionsScreen
from clutch_draw.scenes.sign_in.ui import SignInScreen
from clutch_draw.scenes.sign_up.ui import SignUpScreen
from clutch_draw.scenes.welcome.ui import WelcomeScreen

RESOURCES_PATH = Path(__file__).parent.parent / "resources"
FONTS_PATH = RESOURCES_PATH / "fonts"


def main():
    print("Launching Clutch Draw...")

    pygame.init()
    current_state: GameState = GameState.WELCOME_SCREEN
    next_state: GameState = GameState.WELCOME_SCREEN
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    font_apocalypse_size50 = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 50)
    font_apocalypse_size15 = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 15)
    manager = UIManager(
        (screen_width, screen_height), theme_path="clutch_draw/ui/theme.json"
    )

    welcome_screen = WelcomeScreen(
        screen_width, screen_height, screen, font_apocalypse_size50, manager
    )
    sign_in_screen = None
    sign_up_screen = None
    main_menu_screen = None
    game_setup_screen = None
    options_screen = None
    credits_screen = None
    game_screen = None

    database = Database()
    # Everything inside the while loop happpens on every frame

    while True:
        time_delta = clock.tick(60) / 1000

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                print("Got the quit event")
                pygame.quit()
                raise SystemExit

            manager.process_events(event)

        if current_state == GameState.WELCOME_SCREEN:
            next_state = welcome_screen.render(events)

        elif current_state == GameState.SIGN_IN_SCREEN:
            next_state = sign_in_screen.render(events)

        elif current_state == GameState.SIGN_UP_SCREEN:
            next_state = sign_up_screen.render(events)

        elif current_state == GameState.MAIN_MENU_SCREEN:
            next_state = main_menu_screen.render(events)

        elif current_state == GameState.GAME_SETUP_SCREEN:
            next_state = game_setup_screen.render(events)

        elif current_state == GameState.CREDITS_SCREEN:
            next_state = credits_screen.render(events)

        elif current_state == GameState.OPTIONS_SCREEN:
            next_state = options_screen.render(events)

        elif current_state == GameState.GAME_SCREEN:
            next_state = game_screen.render(events)
        else:
            raise Exception(f"You forgot to handle a game state of {current_state}!")

        if current_state != next_state:
            manager.clear_and_reset()

            if next_state == GameState.SIGN_IN_SCREEN:
                sign_in_screen = SignInScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    manager,
                    database,
                )

            if next_state == GameState.SIGN_UP_SCREEN:
                sign_up_screen = SignUpScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    manager,
                    database,
                )

            if next_state == GameState.WELCOME_SCREEN:
                welcome_screen = WelcomeScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    manager,
                )

            if next_state == GameState.MAIN_MENU_SCREEN:
                main_menu_screen = MainMenuScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    manager,
                )

            if next_state == GameState.GAME_SETUP_SCREEN:
                game_setup_screen = GameSetupScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    manager,
                )

            if next_state == GameState.OPTIONS_SCREEN:
                options_screen = OptionsScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    manager,
                )

            if next_state == GameState.CREDITS_SCREEN:
                credits_screen = CreditsScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    manager,
                )

            if next_state == GameState.GAME_SCREEN:
                game_screen = GameScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse_size50,
                    font_apocalypse_size15,
                    manager,
                )

        current_state = next_state

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()  # Refresh on-screen display


if __name__ == "__main__":
    main()
