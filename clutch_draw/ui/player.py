from pygame import Surface
from clutch_draw.ui.card import Card
from pygame.font import Font
from pygame import Color
import pygame


class Player:
    def __init__(
        self,
        health: int,
        hand: list[Card],
        screen_width: int,
        screen_height: int,
        card_backs: dict,
    ):
        self.health = health
        self.hand = hand
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.shield = 0
        self.card_positions = []
        self.card_backs = card_backs

    def render(self, screen: Surface, x: int, y: int, hide_hand: bool = False) -> None:

        card_width = 100
        card_height = 140
        card_gap = 15

        health_font = Font("resources/fonts/Apocalypse.ttf", 36)

        total_width = len(self.hand) * card_width + (len(self.hand) - 1) * card_gap
        start_x = (self.screen_width - total_width) // 2

        hand_right_edge = start_x + total_width

        right_x = hand_right_edge + 80

        health_surface = health_font.render(
            f"Health: {self.health}", True, Color(255, 0, 0)
        )

        screen.blit(health_surface, (right_x, y + 50))

        shield_surface = health_font.render(
            f"Shield: {self.shield}", True, Color(0, 100, 255)
        )

        screen.blit(shield_surface, (right_x, y + 80))

        self.card_positions = []

        for i, card in enumerate(self.hand):

            total_width = len(self.hand) * card_width + (len(self.hand) - 1) * card_gap
            start_x = (self.screen_width - total_width) // 2

            card_x = start_x + i * (card_width + card_gap)
            card_y = y

            if hide_hand:
                back = self.card_backs.get(card.category)

                if back:
                    screen.blit(back, (card_x, card_y))
                else:
                    pygame.draw.rect(
                        screen,
                        Color(60, 60, 60),
                        (card_x, card_y, card_width, card_height),
                    )
            else:
                card.render(
                    screen,
                    x=card_x,
                    y=card_y,
                )

            self.card_positions.append((card, card_x, card_y))

    def take_damage(self, amount: int) -> None:
        self.health -= amount
        if self.health < 0:
            self.health = 0
