from enum import Enum
import pygame
from pathlib import Path

from clutch_draw.ui.buttons import create_button

RESOURCES_PATH = Path(__file__).parent.parent / "resources"
FONTS_PATH = RESOURCES_PATH / "fonts"


class GameState(Enum):
    MAIN_MENU_SCREEN = "MAIN_MENU_SCREEN"
    OPTIONS_SCREEN = "OPTIONS_SCREEN"
    GAME_SETUP_SCREEN = "GAME_SETUP_SCREEN"
    GAME_SCREEN = "GAME_SCREEN"


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
            play_button = create_button(font_apocalypse, "Play")
            options_button = create_button(font_apocalypse, "Options")
            exit_button = create_button(font_apocalypse, "Exit")
            screen.fill("purple")  # Fill the display with a solid color
            title_x = screen_width // 2 - title_text.get_width() // 2
            title_y = screen_height // 2 - title_text.get_height() // 2
            play_button_x = title_x
            play_button_y = title_y + 100
            screen.blit(title_text, (title_x, title_y))
            screen.blit(play_button, (play_button_x, play_button_y))
            screen.blit(options_button, (title_x, title_y + 200))
            screen.blit(exit_button, (title_x, title_y + 300))
            # Process player inputs.
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    _, _, button_width, button_height = play_button.get_rect()
                    if (
                        play_button_x <= mouse_x <= play_button_x + button_width
                        and play_button_y <= mouse_y <= play_button_y + button_height
                    ):
                        current_state = GameState.GAME_SETUP_SCREEN

            # Do logical updates here.
            # ...

            # Render the graphics here.
            # ...
        if current_state == GameState.GAME_SETUP_SCREEN:
            screen.fill("blue")
            back_button = create_button(font_apocalypse, "Back")
            back_button_x = screen_width // 2 - back_button.get_width() // 2
            back_button_y = screen_height // 2 - back_button.get_height() // 2
            screen.blit(back_button, (back_button_x, back_button_y))
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    _, _, button_width, button_height = back_button.get_rect()
                    if (
                        back_button_x <= mouse_x <= back_button_x + button_width
                        and back_button_y <= mouse_y <= back_button_y + button_height
                    ):
                        current_state = GameState.MAIN_MENU_SCREEN

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)


if __name__ == "__main__":
    main()
