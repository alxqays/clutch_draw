from clutch_draw.ui.rect import inside_rect


import pygame


def mouse_inside(
    event: pygame.event.Event,
    surface: pygame.Surface,
    surface_x: int,
    surface_y: int,
) -> bool:
    mouse_x, mouse_y = event.pos
    _, _, width, height = surface.get_rect()
    return inside_rect(
        mouse_x,
        mouse_y,
        surface_x,
        surface_y,
        width,
        height,
    )