from pygame_gui import UIManager
from pygame_gui.elements import UITextEntryLine
from clutch_draw.game_state import GameState

from pygame import MOUSEBUTTONUP, Rect, Surface, Color
from pygame.font import Font
from pygame.event import Event

from clutch_draw.ui.buttons import create_button
from clutch_draw.ui.mouse import mouse_inside


text_input = None


def screen_sign_in(
    current_state: GameState,
    screen_width: int,
    screen_height: int,
    screen: Surface,
    font_apocalypse: Font,
    events: list[Event],
    manager: UIManager,
) -> GameState:
    screen.fill("gray")
    font = Font(None, 74)
    text = font.render("Sign In", True, Color(0, 0, 0))
    text_x = screen_width // 2 - text.get_width() // 2
    text_y = screen_height // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))

    global text_input
    if text_input is None:
        text_input = UITextEntryLine(
            relative_rect=Rect((100, 100), (200, 50)), manager=manager
        )

    sign_in_button = create_button(font_apocalypse, "Sign In")
    sign_in_button_x = screen_width // 2 - sign_in_button.get_width() // 2
    sign_in_button_y = screen_height - sign_in_button.get_height() - 50
    screen.blit(sign_in_button, (sign_in_button_x, sign_in_button_y))

    for event in events:
        if event.type == MOUSEBUTTONUP:
            if mouse_inside(event, sign_in_button, sign_in_button_x, sign_in_button_y):
                current_state = GameState.MAIN_MENU_SCREEN

    return current_state
