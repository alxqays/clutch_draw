from clutch_draw.game_state import GameState
from clutch_draw.ui.mouse import mouse_inside
from clutch_draw.ui.buttons import create_button


from pygame import MOUSEMOTION, MOUSEBUTTONUP, Surface, Color
from pygame.event import Event
from pygame.font import Font


def screen_credits(
    current_state: GameState,
    screen_width: int,
    screen_height: int,
    screen: Surface,
    font_apocalypse: Font,
    events: list[Event],
) -> GameState:
    screen.fill("darkgreen")
    credits_lines = [
        "Credits",
        "",
        "Developed by: (Your Name)",
        "Libraries: pygame",
    ]

    start_y = screen_height // 4
    for i, line in enumerate(credits_lines):
        line_surf = font_apocalypse.render(line, True, Color(0, 0, 0))
        line_x = screen_width // 2 - line_surf.get_width() // 2
        line_y = start_y + i * (line_surf.get_height() + 10)
        screen.blit(line_surf, (line_x, line_y))

    back_button = create_button(font_apocalypse, "Back")
    back_button_x = screen_width // 2 - back_button.get_width() // 2
    back_button_y = screen_height - back_button.get_height() - 50
    screen.blit(back_button, (back_button_x, back_button_y))

    for event in events:
        if event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
        if event.type == MOUSEBUTTONUP:
            if mouse_inside(event, back_button, back_button_x, back_button_y):
                current_state = GameState.MAIN_MENU_SCREEN

    return current_state
