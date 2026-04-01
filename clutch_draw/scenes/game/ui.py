import pygame
from pygame_gui import UIManager
from clutch_draw.game_logic.game_manager import GameManager
from clutch_draw.game_state import GameState
from clutch_draw.ui.card import Card
from clutch_draw.ui.mouse import mouse_inside

from pygame import MOUSEMOTION, MOUSEBUTTONUP, Color, Surface
from pygame.event import Event
from pygame.font import Font

from clutch_draw.ui.player import Player
import random


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
        self.deck = self.create_deck()

        our_hand = self.create_starting_hand()
        opponent_hand = self.create_starting_hand()

        self.opponent_player = Player(
            100, opponent_hand, self.screen_width, self.screen_height
        )
        self.our_player = Player(100, our_hand, self.screen_width, self.screen_height)

        self.game_manager = GameManager(
            self.our_player, self.opponent_player, self.deck
        )

    def create_deck(self):
        return [
            # Offence
            Card(
                "Hunter",
                self.text_font,
                self.text_font,
                "Deal 20",
                Color(200, 100, 100),
                Color(0, 0, 0),
                "Offence",
                20,
            ),
            Card(
                "Raider",
                self.text_font,
                self.text_font,
                "Deal 25",
                Color(200, 100, 100),
                Color(0, 0, 0),
                "Offence",
                25,
            ),
            Card(
                "Smuggler",
                self.text_font,
                self.text_font,
                "Deal 22",
                Color(200, 100, 100),
                Color(0, 0, 0),
                "Offence",
                22,
            ),
            Card(
                "Executioner",
                self.text_font,
                self.text_font,
                "Deal 30",
                Color(200, 100, 100),
                Color(0, 0, 0),
                "Offence",
                30,
            ),
            Card(
                "Ambusher",
                self.text_font,
                self.text_font,
                "Deal 18 (Ignores Shield)",
                Color(200, 100, 100),
                Color(0, 0, 0),
                "Offence",
                18,
            ),
            # Defence
            Card(
                "Soldier",
                self.text_font,
                self.text_font,
                "+1 Shield",
                Color(200, 100, 100),
                Color(0, 0, 0),
                "Defence",
                15,
            ),
            Card(
                "Enforcer",
                self.text_font,
                self.text_font,
                "+20 Shield",
                Color(200, 100, 100),
                Color(0, 0, 0),
                "Defence",
                20,
            ),
            Card(
                "Guardian",
                self.text_font,
                self.text_font,
                "+18 Shield",
                Color(200, 100, 100),
                Color(0, 0, 0),
                "Defence",
                18,
            ),
            Card(
                "Heavy Gunner",
                self.text_font,
                self.text_font,
                "+25 Shield",
                Color(200, 100, 100),
                Color(0, 0, 0),
                "Defence",
                25,
            ),
            Card(
                "Bunker Buster",
                self.text_font,
                self.text_font,
                "+12 Shield",
                Color(200, 100, 100),
                Color(0, 0, 0),
                "Defence",
                12,
            ),
            # Support
            Card(
                "Supply Runner",
                self.text_font,
                self.text_font,
                "+22 Health",
                Color(200, 100, 100),
                Color(0, 0, 0),
                "Support",
                22,
            ),
            Card(
                "Field Medic",
                self.text_font,
                self.text_font,
                "+20 Health",
                Color(200, 100, 100),
                Color(0, 0, 0),
                "Support",
                20,
            ),
            Card(
                "Survivor",
                self.text_font,
                self.text_font,
                "+15 Health",
                Color(200, 100, 100),
                Color(0, 0, 0),
                "Support",
                15,
            ),
            Card(
                "Scavenger",
                self.text_font,
                self.text_font,
                "+18 Health",
                Color(200, 100, 100),
                Color(0, 0, 0),
                "Support",
                18,
            ),
            Card(
                "Doctor",
                self.text_font,
                self.text_font,
                "+25 Health",
                Color(200, 100, 100),
                Color(0, 0, 0),
                "Support",
                25,
            ),
        ]

    def create_starting_hand(self):

        hand = []

        for category, count in [("Offence", 2), ("Defence", 2), ("Support", 1)]:
            available = [c for c in self.deck if c.category == category]
            selected = random.sample(available, count)

            for card in selected:
                self.deck.remove(card)

            hand.extend(selected)

        return hand

    def render(self, events: list[Event]) -> GameState:

        self.screen.fill("grey")

        self.opponent_player.render(self.screen, x=200, y=100, hide_hand=True)
        self.our_player.render(self.screen, x=200, y=450, hide_hand=False)

        next_state = GameState.GAME_SCREEN

        for event in events:
            if event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos

            if event.type == MOUSEBUTTONUP:

                mouse_x, mouse_y = event.pos
                print("Mouse clicked at:", mouse_x, mouse_y)

                if self.game_manager.turn == "player":

                    for card, x, y in self.our_player.card_positions:

                        print("Checking card at:", x, y)

                        rect = pygame.Rect(x, y, 100, 140)

                        if rect.collidepoint(mouse_x, mouse_y):

                            print("CARD CLICKED:", card.title)

                            self.game_manager.take_turn(
                                self.our_player, self.opponent_player, card
                            )

        if self.game_manager.turn == "ai":
            self.game_manager.ai_turn()

        result = self.game_manager.check_game_over()
        if result:
            print(result)

        return next_state
