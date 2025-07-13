import pygame
from pathlib import Path

RESOURCES_PATH = Path(__file__).parent.parent / "resources"
FONTS_PATH = RESOURCES_PATH / "fonts"


def main():
    print("Launching Clutch Draw...")

    pygame.init()

    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    font_apocalypse = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 50)
    title_text = font_apocalypse.render("Clutch Draw", True, pygame.Color(0, 0, 0))
    play_button = create_button(font_apocalypse, "Play")
    options_button = create_button(font_apocalypse, "Options")
    exit_button = create_button(font_apocalypse, "Exit")
    clock = pygame.time.Clock()

    # This happens once at the start not once per frame
    screen.fill("purple")  # Fill the display with a solid color
    title_x = screen_width // 2 - title_text.get_width() // 2
    title_y = screen_height // 2 - title_text.get_height() // 2
    screen.blit(title_text, (title_x, title_y))
    screen.blit(play_button, (title_x, title_y + 100))
    screen.blit(options_button, (title_x, title_y + 200))
    screen.blit(exit_button, (title_x, title_y + 300))

    # Everything inside the while loop happpens on every frame

    while True:

        # Process player inputs.
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                print("Got the quit event")
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                print(x, y)

        # Do logical updates here.
        # ...

        # Render the graphics here.
        # ...

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)


def create_button(font: pygame.font.Font, text: str) -> pygame.Surface:
    width = 200
    height = 75
    surface = pygame.Surface((width, height))
    surface.fill(pygame.Color(255, 0, 0))
    text_surface = font.render(text, True, pygame.Color(0, 0, 0))
    surface.blit(
        text_surface,
        (
            width // 2 - text_surface.get_width() // 2,
            height // 2 - text_surface.get_height() // 2,
        ),
    )
    return surface


if __name__ == "__main__":
    main()
