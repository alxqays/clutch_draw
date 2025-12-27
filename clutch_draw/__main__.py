from typing import Optional
import pygame
from pathlib import Path

from pygame_gui import UIManager

from clutch_draw.game_state import GameState
from clutch_draw.scenes.credits.ui import screen_credits
from clutch_draw.scenes.game_setup.ui import screen_game_setup
from clutch_draw.scenes.main_menu.ui import screen_main_menu
from clutch_draw.scenes.options.ui import screen_options
from clutch_draw.scenes.sign_in.ui import SignInScreen
from clutch_draw.scenes.sign_up.ui import screen_sign_up
from clutch_draw.scenes.welcome.ui import screen_welcome

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
    font_apocalypse = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 50)
    title_text = font_apocalypse.render("Clutch Draw", True, pygame.Color(0, 0, 0))
    manager = UIManager((screen_width, screen_height))

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
            next_state = screen_welcome(
                current_state,
                screen_width,
                screen_height,
                screen,
                font_apocalypse,
                events,
            )

        elif current_state == GameState.SIGN_IN_SCREEN:
            next_state = sign_in_screen.render(events)

        elif current_state == GameState.SIGN_UP_SCREEN:
            next_state = screen_sign_up(
                current_state,
                screen_width,
                screen_height,
                screen,
                font_apocalypse,
                events,
            )

        elif current_state == GameState.MAIN_MENU_SCREEN:
            next_state = screen_main_menu(
                current_state,
                screen_width,
                screen_height,
                screen,
                font_apocalypse,
                title_text,
                events,
            )

        elif current_state == GameState.GAME_SETUP_SCREEN:
            next_state = screen_game_setup(
                current_state,
                screen_width,
                screen_height,
                screen,
                font_apocalypse,
                events,
            )

        elif current_state == GameState.CREDITS_SCREEN:
            next_state = screen_credits(
                current_state,
                screen_width,
                screen_height,
                screen,
                font_apocalypse,
                events,
            )

        elif current_state == GameState.OPTIONS_SCREEN:
            next_state = screen_options(
                current_state,
                screen_width,
                screen_height,
                screen,
                font_apocalypse,
                events,
            )
        else:
            raise Exception(f"You forgot to handle a game state of {current_state}!")

        if current_state != next_state:
            manager.clear_and_reset()

            if next_state == GameState.SIGN_IN_SCREEN:
                sign_in_screen = SignInScreen(
                    screen_width,
                    screen_height,
                    screen,
                    font_apocalypse,
                    manager,
                )

        current_state = next_state

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()  # Refresh on-screen display


if __name__ == "__main__":
    main()
