from pygame_gui import UIManager
from clutch_draw.game_state import GameState
from clutch_draw.ui.card import Card
from clutch_draw.ui.mouse import mouse_inside
from clutch_draw.ui.buttons import create_button

from pygame import MOUSEMOTION, MOUSEBUTTONUP, Color, Surface
from pygame.event import Event
from pygame.font import Font

from clutch_draw.ui.player import Player


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

        num_cards = 5
        our_hand: list[Card] = []
        opponent_hand: list[Card] = []

        for i in range(num_cards):

            our_hand.append(
                Card(
                    title=f"Card {i + 1}",
                    title_font=self.text_font,
                    text_font=self.text_font,
                    ability_text=f"Ability text {i + 1}",
                    background_color=Color(255, 255, 255),
                    title_color=Color(0, 0, 0),
                )
            )

            opponent_hand.append(
                Card(
                    title=f"Card {i + 1}",
                    title_font=self.text_font,
                    text_font=self.text_font,
                    ability_text=f"Ability text {i + 1}",
                    background_color=Color(255, 255, 255),
                    title_color=Color(0, 0, 0),
                )
            )

        self.opponent_player = Player(
            100, opponent_hand, self.screen_width, self.screen_height
        )
        self.our_player = Player(200, our_hand, self.screen_width, self.screen_height)

    def render(self, events: list[Event]) -> GameState:
        self.screen.fill("blue")
        take_damage_button = create_button(self.title_font, "Opponent Take Damage")
        take_damage_button_x = 15
        take_damage_button_y = 15
        self.screen.blit(
            take_damage_button, (take_damage_button_x, take_damage_button_y)
        )

        self.opponent_player.render(self.screen, x=200, y=100, hide_hand=True)
        self.our_player.render(self.screen, x=200, y=450, hide_hand=False)

        next_state = GameState.GAME_SCREEN

        for event in events:
            if event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            if event.type == MOUSEBUTTONUP:
                if mouse_inside(
                    event,
                    take_damage_button,
                    take_damage_button_x,
                    take_damage_button_y,
                ):
                    self.opponent_player.take_damage(10)
                    # next_state = GameState.MAIN_MENU_SCREEN

        return next_state
