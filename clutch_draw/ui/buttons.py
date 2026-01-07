import pygame


def create_button(font: pygame.font.Font, text: str) -> pygame.Surface:
    width = 200
    height = 75
    surface = pygame.Surface((width, height))
    surface.fill(pygame.Color(0, 0, 0))
    text_surface = font.render(text, True, pygame.Color(255, 255, 255))
    surface.blit(
        text_surface,
        (
            width // 2 - text_surface.get_width() // 2,
            height // 2 - text_surface.get_height() // 2,
        ),
    )
    return surface
