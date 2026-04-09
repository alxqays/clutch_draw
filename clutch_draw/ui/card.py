from pygame import Surface

from pygame.font import Font

import pygame


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

        self.width = 100
        self.height = 140

        self.title = title
        self.title_font = title_font
        self.text_font = text_font
        self.ability_text = ability_text
        self.image = pygame.image.load(image_path).convert_alpha()

        self.category = category
        self.value = value

    def render(self, screen: Surface, x: int, y: int, scale: float = 1.0) -> None:

        if scale == 1.0:
            screen.blit(self.image, (x, y))

            card_centre_x = x + self.width // 2

            rect_centre_x = card_centre_x - 14
            rect_centre_y = y + 115

            circle_centre_x = card_centre_x + 20
            circle_centre_y = y + 115

            title_surface = self.title_font.render(self.title, True, (255, 255, 255))

            screen.blit(
                title_surface,
                (
                    card_centre_x - title_surface.get_width() // 2,
                    y + 19,
                ),
            )

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

        scaled_width = int(self.width * scale)
        scaled_height = int(self.height * scale)

        scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))

        draw_x = x - (scaled_width - self.width) // 2
        draw_y = y - (scaled_height - self.height) // 2

        screen.blit(scaled_image, (draw_x, draw_y))

        card_centre_x = draw_x + scaled_width // 2

        rect_centre_x = card_centre_x - int(14 * scale)
        rect_centre_y = draw_y + int(115 * scale)

        circle_centre_x = card_centre_x + int(20 * scale)
        circle_centre_y = draw_y + int(115 * scale)

        title_font = pygame.font.Font("resources/fonts/Apocalypse.ttf", int(18 * scale))
        text_font = pygame.font.Font("resources/fonts/Apocalypse.ttf", int(14 * scale))

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
