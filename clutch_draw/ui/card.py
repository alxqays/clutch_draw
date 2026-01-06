from pygame import Color, Surface

from pygame.font import Font


class Card:

    def __init__(
        self,
        title: str,
        title_font: Font,
        text_font: Font,
        ability_text: str,
        background_color: Color,
        title_color: Color,
    ) -> None:
        self.width = 100
        self.height = 140

        self.title = title
        self.title_font = title_font
        self.text_font = text_font
        self.ability_text = ability_text
        self.color = background_color
        self.title_color = title_color

    def render(self, screen: Surface, x: int, y: int) -> None:
        card_surface = Surface((self.width, self.height))
        card_surface.fill(self.color)

        title_surface = self.title_font.render(self.title, True, self.title_color)

        card_surface.blit(
            title_surface,
            (
                self.width // 2 - title_surface.get_width() // 2,
                10,
            ),
        )

        ability_text_surface = self.text_font.render(
            self.ability_text, True, self.title_color
        )

        card_surface.blit(
            ability_text_surface,
            (
                self.width // 2 - ability_text_surface.get_width() // 2,
                self.height // 2 - ability_text_surface.get_height() // 2,
            ),
        )
        screen.blit(card_surface, (x, y))
