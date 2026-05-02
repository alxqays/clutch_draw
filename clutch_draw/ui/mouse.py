from clutch_draw.ui.rect import inside_rect
import pygame


# Checks if a mouse event has occurred within the bounds of a surface
def mouse_inside(
    event: pygame.event.Event,
    surface: pygame.Surface,
    surface_x: int,
    surface_y: int,
) -> bool:

    # Gets the position of the mouse click
    mouse_x, mouse_y = event.pos
    # Gets the size of the surface
    _, _, width, height = (
        surface.get_rect()
    )  # "_" is used to ignore the position of the surface and only store the dimensions of it

    return inside_rect(
        mouse_x,
        mouse_y,
        surface_x,
        surface_y,
        width,
        height,
    )  # Calls the function and returns True if the mouse is inside the rectangle and False if it is not
