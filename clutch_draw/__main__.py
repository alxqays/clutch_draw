import pygame
from pathlib import Path

from clutch_draw.game_state import GameState
from clutch_draw.scenes.credits.ui import screen_credits
from clutch_draw.scenes.game_setup.ui import screen_game_setup
from clutch_draw.scenes.main_menu.ui import screen_main_menu
from clutch_draw.scenes.options.ui import screen_options

RESOURCES_PATH = Path(__file__).parent.parent / "resources"
FONTS_PATH = RESOURCES_PATH / "fonts"


def main():
    print("Launching Clutch Draw...")

    pygame.init()
    current_state = GameState.MAIN_MENU_SCREEN
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    font_apocalypse = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 50)
    title_text = font_apocalypse.render("Clutch Draw", True, pygame.Color(0, 0, 0))

    # Everything inside the while loop happpens on every frame

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                print("Got the quit event")
                pygame.quit()
                raise SystemExit
        if current_state == GameState.MAIN_MENU_SCREEN:
            current_state = screen_main_menu(
                current_state,
                screen_width,
                screen_height,
                screen,
                font_apocalypse,
                title_text,
                events,
            )

        elif current_state == GameState.GAME_SETUP_SCREEN:
            current_state = screen_game_setup(
                current_state,
                screen_width,
                screen_height,
                screen,
                font_apocalypse,
                events,
            )

        elif current_state == GameState.CREDITS_SCREEN:
            current_state = screen_credits(
                current_state,
                screen_width,
                screen_height,
                screen,
                font_apocalypse,
                events,
            )

        elif current_state == GameState.OPTIONS_SCREEN:
            current_state = screen_options(
                current_state,
                screen_width,
                screen_height,
                screen,
                font_apocalypse,
                events,
            )

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)


if __name__ == "__main__":
    main()
