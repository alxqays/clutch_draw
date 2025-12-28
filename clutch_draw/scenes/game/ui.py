from pygame_gui import UIManager
from clutch_draw.game_state import GameState
from clutch_draw.ui.card import Card
from clutch_draw.ui.mouse import mouse_inside
from clutch_draw.ui.buttons import create_button

from pygame import MOUSEMOTION, MOUSEBUTTONUP, Color, Surface
from pygame.event import Event
from pygame.font import Font


class GameScreen:

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        screen: Surface,
        title_font: Font,
        text_font: Font,
        manager: UIManager,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.title_font = title_font
        self.text_font = text_font
        self.manager = manager

    def render(self, events: list[Event]) -> GameState:
        self.screen.fill("blue")
        back_button = create_button(self.title_font, "Back")
        back_button_x = 15
        back_button_y = 15
        self.screen.blit(back_button, (back_button_x, back_button_y))

        card_width = 100
        card_gap = 15
        num_cards = 5

        total_card_width = num_cards * card_width + (num_cards - 1) * card_gap

        print(f"Total card width: {total_card_width}")
        for i in range(num_cards):

            card = Card(
                title=f"Card {i + 1}",
                title_font=self.text_font,
                text_font=self.text_font,
                ability_text=f"Ability text {i + 1}",
                background_color=Color(255, 255, 255),
                title_color=Color(0, 0, 0),
            )
            card.render(
                self.screen,
                x=self.screen_width
                - total_card_width
                + i * (card_width + card_gap)
                - card_gap,
                y=self.screen_height - card.height,
            )

        next_state = GameState.GAME_SCREEN

        for event in events:
            if event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            if event.type == MOUSEBUTTONUP:
                if mouse_inside(event, back_button, back_button_x, back_button_y):
                    next_state = GameState.MAIN_MENU_SCREEN

        return next_state
