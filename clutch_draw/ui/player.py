import pygame
from pygame import Surface, Color
from pygame.font import Font
from clutch_draw.ui.card import Card
from pathlib import Path

FONTS_PATH = Path(__file__).parent.parent.parent / "resources" / "fonts"


class Player:
    def __init__(
        self,
        health: int,
        hand: list[Card],
        screen_width: int,
        screen_height: int,
        card_backs: dict,
    ):
        # Stores and displays the player's stats such as their health, shield and hand of cards
        self.health = health
        self.hand = hand
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.shield = 0  # The shield provides the player extra protection by absorbing any damage before health absorbs it
        self.card_positions = (
            []
        )  # Stores the positions of the player's cards so that they can be interacted with
        self.card_backs = card_backs

    # Renders the player's hand, health and shield onto the screen
    def render(self, screen: Surface, x: int, y: int, hide_hand: bool = False) -> None:

        # Dimensions of the cards
        card_width = 100
        card_height = 140
        card_gap = 15  # Spacing between the cards in the hand

        health_font = Font(FONTS_PATH / "Apocalypse.ttf", 36)

        # Calculates the total width of the hand so that it can be centred on the screen
        total_width = len(self.hand) * card_width + (len(self.hand) - 1) * card_gap
        start_x = (self.screen_width - total_width) // 2

        hand_right_edge = start_x + total_width
        right_x = hand_right_edge + 80  # Positioning for the health and shield bars

        border = 3  # The thickness of the text outline

        # Rendering health text/bar with an outline
        health_main_text = health_font.render(
            f"HEALTH: {self.health}", True, Color(255, 0, 0)
        )
        health_border_text = health_font.render(
            f"HEALTH: {self.health}", True, Color(0, 0, 0)
        )  # Outline is black to make the text stand out

        health_x = right_x
        health_y = y + 50

        # Drawing the outline by rendering it multiple times, each time with a slight offset
        screen.blit(health_border_text, (health_x - border, health_y))
        screen.blit(health_border_text, (health_x + border, health_y))
        screen.blit(health_border_text, (health_x, health_y - border))
        screen.blit(health_border_text, (health_x, health_y + border))

        screen.blit(
            health_main_text, (health_x, health_y)
        )  # The text is drawn on top of the outline

        # Rendering shield text/bar with the same outline
        shield_main_text = health_font.render(
            f"SHIELD: {self.shield}", True, Color(0, 100, 255)
        )
        shield_border_text = health_font.render(
            f"SHIELD: {self.shield}", True, Color(0, 0, 0)
        )

        shield_y = health_y + 40

        screen.blit(shield_border_text, (health_x - border, shield_y))
        screen.blit(shield_border_text, (health_x + border, shield_y))
        screen.blit(shield_border_text, (health_x, shield_y - border))
        screen.blit(shield_border_text, (health_x, shield_y + border))

        screen.blit(shield_main_text, (health_x, shield_y))

        self.card_positions = []  # Resets the positions of the cards each frame

        for i, card in enumerate(self.hand):

            # Calculating the position of each card in the hand
            total_width = len(self.hand) * card_width + (len(self.hand) - 1) * card_gap
            start_x = (self.screen_width - total_width) // 2

            card_x = start_x + i * (card_width + card_gap)
            card_y = y

            if hide_hand:

                # Drawing the backs of the cards instead of the fronts (used for the opponent so that the player can't see their cards)
                back = self.card_backs.get(card.category)

                if back:
                    screen.blit(back, (card_x, card_y))
                else:
                    # Fallback in case no image for a card is found
                    pygame.draw.rect(
                        screen,
                        Color(60, 60, 60),
                        (card_x, card_y, card_width, card_height),
                    )
            else:
                # Drawing the cards
                card.render(
                    screen,
                    x=card_x,
                    y=card_y,
                )

            # Storing the positions of the cards for click detections
            self.card_positions.append((card, card_x, card_y))

    # Reducing the player's health and preventing it from going below 0
    def take_damage(self, amount: int) -> None:
        self.health -= amount
        if self.health < 0:
            self.health = 0
