import pygame
from pygame import Surface
from pygame.font import Font

from pathlib import Path

FONTS_PATH = Path(__file__).parent.parent.parent / "resources" / "fonts"


class Card:

    def __init__(
        self,
        title: str,
        title_font: Font,
        text_font: Font,
        ability_text: str,
        image_path: str,
        category: str,
        value: int,
    ) -> None:

        # Stores card data such as their dimensions, appearance, category and value
        self.width = 100
        self.height = 140

        self.title = title
        self.title_font = title_font
        self.text_font = text_font
        self.ability_text = ability_text
        self.image = pygame.image.load(image_path).convert_alpha()

        self.category = category  # Either Offence, Defence or Support
        self.value = value  # The numerical value/effect of the card

    # Renders the card at a given position and optionally scales it for animation
    def render(self, screen: Surface, x: int, y: int, scale: float = 1.0) -> None:

        # Normal rendering with no scaling
        if scale == 1.0:
            screen.blit(self.image, (x, y))

            card_centre_x = x + self.width // 2

            rect_centre_x = card_centre_x - 14
            rect_centre_y = y + 115

            circle_centre_x = card_centre_x + 20
            circle_centre_y = y + 115

            # Centres the title text onto the card, which is the name/role of the card/character
            title_surface = self.title_font.render(self.title, True, (255, 255, 255))

            screen.blit(
                title_surface,
                (
                    card_centre_x - title_surface.get_width() // 2,
                    y + 19,
                ),
            )

            # Does the same for the ability text, which is either "DMG", "SH" or "HP", briefly showing the user the card's action
            ability_text_surface = self.text_font.render(
                self.ability_text, True, (255, 255, 255)
            )

            screen.blit(
                ability_text_surface,
                (
                    rect_centre_x - ability_text_surface.get_width() // 2,
                    rect_centre_y - ability_text_surface.get_height() // 2,
                ),
            )

            # Does the same for the value text, which shows the user the numerical value of the action taking place
            value_surface = self.text_font.render(
                str(self.value), True, (255, 255, 255)
            )

            screen.blit(
                value_surface,
                (
                    circle_centre_x - value_surface.get_width() // 2,
                    circle_centre_y - value_surface.get_height() // 2,
                ),
            )

            return

        # Scaled rendering of the cards which is used for animations so that the user can see what is happening more clearly
        # All positions and texts are recalculated so that everything can stay aligned when scaled
        scaled_width = int(self.width * scale)
        scaled_height = int(self.height * scale)

        scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))

        # Adjusts the position of the card so that it appears to scale from its centre rather than the top-left corner
        draw_x = x - (scaled_width - self.width) // 2
        draw_y = y - (scaled_height - self.height) // 2

        screen.blit(scaled_image, (draw_x, draw_y))

        card_centre_x = draw_x + scaled_width // 2

        rect_centre_x = card_centre_x - int(14 * scale)
        rect_centre_y = draw_y + int(115 * scale)

        circle_centre_x = card_centre_x + int(20 * scale)
        circle_centre_y = draw_y + int(115 * scale)

        # The font size is scaled to match the card size
        title_font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", int(18 * scale))
        text_font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", int(14 * scale))

        # Text must be re-rendered so that it can match with the scaled font size
        title_surface = title_font.render(self.title, True, (255, 255, 255))

        screen.blit(
            title_surface,
            (card_centre_x - title_surface.get_width() // 2, draw_y + int(19 * scale)),
        )

        ability_text_surface = text_font.render(
            self.ability_text, True, (255, 255, 255)
        )

        screen.blit(
            ability_text_surface,
            (
                rect_centre_x - ability_text_surface.get_width() // 2,
                rect_centre_y - ability_text_surface.get_height() // 2,
            ),
        )

        value_surface = text_font.render(str(self.value), True, (255, 255, 255))

        screen.blit(
            value_surface,
            (
                circle_centre_x - value_surface.get_width() // 2,
                circle_centre_y - value_surface.get_height() // 2,
            ),
        )
