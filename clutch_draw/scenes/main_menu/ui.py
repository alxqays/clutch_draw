from pygame_gui import UIManager
from clutch_draw.game_state import GameState
from clutch_draw.ui.mouse import mouse_inside
from clutch_draw.ui.buttons import create_button

from pygame.font import Font
from pygame import MOUSEBUTTONUP, Surface, Color
from pygame.event import Event

import pygame

from clutch_draw.db.utils import Database


def calculate_level(xp):
    level = 1
    xp_needed = 100

    while xp >= xp_needed:
        xp -= xp_needed
        level += 1
        xp_needed += 50

    return level, xp, xp_needed


class MainMenuScreen:

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        screen: Surface,
        button_font: Font,
        title_font: Font,
        manager: UIManager,
        user_data: dict,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.button_font = button_font
        self.title_font = title_font
        self.manager = manager

        self.background = pygame.image.load("resources/images/orig_big.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.screen_width, self.screen_height)
        )

        self.db = Database()

        self.username = user_data["username"]
        self.xp = user_data["xp"]
        self.level = user_data["level"]
        self.xp_to_next = 100 + (self.level - 1) * 50
        self.wins = user_data["wins"]
        self.losses = user_data["losses"]

        self.profile_rect = pygame.Rect(self.screen_width - 260, 30, 210, 55)

        self.profile_expanded_rect = pygame.Rect(self.screen_width - 320, 30, 300, 230)

    def render(self, events: list[Event]) -> GameState:

        title_font = pygame.font.Font("resources/fonts/Apocalypse.ttf", 32)
        text_font = pygame.font.Font("resources/fonts/Apocalypse.ttf", 20)
        small_font = pygame.font.Font("resources/fonts/Apocalypse.ttf", 16)

        play_button = create_button(self.button_font, "Play")
        options_button = create_button(self.button_font, "Options")
        exit_button = create_button(self.button_font, "Exit")

        self.screen.blit(self.background, (0, 0))

        title_text = self.title_font.render("Main Menu", True, Color(255, 255, 255))
        border_text = self.title_font.render("Main Menu", True, Color(0, 0, 0))

        title_x = self.screen_width // 2 - title_text.get_width() // 2
        title_y = self.screen_height // 2 - title_text.get_height() // 2 - 65

        border = 5

        self.screen.blit(border_text, (title_x - border, title_y))  # left
        self.screen.blit(border_text, (title_x + border, title_y))  # right
        self.screen.blit(border_text, (title_x, title_y - border))  # top
        self.screen.blit(border_text, (title_x, title_y + border))  # bottom

        self.screen.blit(title_text, (title_x, title_y))

        play_button_x = self.screen_width // 2 - play_button.get_width() // 2
        play_button_y = self.screen_height - play_button.get_height() - 280
        options_button_x = self.screen_width // 2 - options_button.get_width() // 2
        options_button_y = self.screen_height - options_button.get_height() - 180
        exit_button_x = self.screen_width // 2 - exit_button.get_width() // 2
        exit_button_y = self.screen_height - exit_button.get_height() - 80

        self.screen.blit(play_button, (play_button_x, play_button_y))
        self.screen.blit(options_button, (options_button_x, options_button_y))
        self.screen.blit(exit_button, (exit_button_x, exit_button_y))

        next_state = GameState.MAIN_MENU_SCREEN

        for event in events:

            if event.type == MOUSEBUTTONUP:
                if mouse_inside(event, play_button, play_button_x, play_button_y):
                    next_state = GameState.GAME_SETUP_SCREEN
                if mouse_inside(
                    event, options_button, options_button_x, options_button_y
                ):
                    next_state = GameState.OPTIONS_SCREEN
                if mouse_inside(event, exit_button, exit_button_x, exit_button_y):
                    print("Exit clicked")
                    pygame.quit()
                    raise SystemExit

        mouse_pos = pygame.mouse.get_pos()
        hovering_profile = self.profile_rect.collidepoint(mouse_pos)

        pygame.draw.rect(self.screen, (0, 0, 0), self.profile_rect)

        # level circle
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            (self.profile_rect.x + 30, self.profile_rect.y + 30),
            18,
        )

        name_font = pygame.font.Font("resources/fonts/Apocalypse.ttf", 26)
        level_font = pygame.font.Font("resources/fonts/Apocalypse.ttf", 24)

        level_text = level_font.render(str(self.level), True, (0, 0, 0))
        self.screen.blit(
            level_text,
            (
                self.profile_rect.x + 30 - level_text.get_width() // 2,
                self.profile_rect.y + 30 - level_text.get_height() // 2,
            ),
        )

        # username
        username_text = name_font.render(self.username, True, (255, 255, 255))
        self.screen.blit(
            username_text,
            (self.profile_rect.x + 65, self.profile_rect.y + 15),
        )

        if hovering_profile:

            pygame.draw.rect(self.screen, (0, 0, 0), self.profile_expanded_rect)
            pygame.draw.rect(
                self.screen, (255, 255, 255), self.profile_expanded_rect, 2
            )

            padding = 12
            line_gap = 38

            start_x = self.profile_expanded_rect.x + padding
            start_y = self.profile_expanded_rect.y + padding

            # username + level
            title_surface = title_font.render(
                f"(Lvl {self.level}) {self.username} ", True, (255, 255, 255)
            )

            # XP
            xp_surface = text_font.render(
                f"XP: {self.xp}/{self.xp_to_next}", True, (255, 255, 255)
            )

            # Wins/Losses
            wins_surface = text_font.render(f"WINS: {self.wins}", True, (255, 255, 255))

            losses_surface = text_font.render(
                f"LOSSES: {self.losses}", True, (255, 255, 255)
            )

            total_games = self.wins + self.losses

            total_surface = text_font.render(
                f"GAMES: {total_games}", True, (255, 255, 255)
            )

            unlock_colour = (0, 255, 0) if self.level >= 5 else (255, 80, 80)
            unlock_surface = small_font.render(
                (
                    "Competitive Unlocked"
                    if self.level >= 5
                    else "Competitive unlocks at Level 5"
                ),
                True,
                unlock_colour,
            )

            self.screen.blit(title_surface, (start_x, start_y))

            self.screen.blit(xp_surface, (start_x, start_y + line_gap))

            self.screen.blit(wins_surface, (start_x, start_y + line_gap * 2))

            self.screen.blit(losses_surface, (start_x, start_y + line_gap * 3))

            self.screen.blit(total_surface, (start_x, start_y + line_gap * 4))

            self.screen.blit(unlock_surface, (start_x, start_y + line_gap * 5))

        return next_state
