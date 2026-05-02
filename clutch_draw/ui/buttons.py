import pygame


# Creates a button surface with centred text
def create_button(
    font: pygame.font.Font, text: str, width=200, height=75
) -> pygame.Surface:

    # Button surface dimensions and colour
    surface = pygame.Surface((width, height))
    surface.fill(pygame.Color(0, 0, 0))

    # Button text with a font and colour, centred on the button surface
    text_surface = font.render(text, True, pygame.Color(255, 255, 255))
    surface.blit(
        text_surface,
        (
            width // 2 - text_surface.get_width() // 2,
            height // 2 - text_surface.get_height() // 2,
        ),
    )
    return surface
