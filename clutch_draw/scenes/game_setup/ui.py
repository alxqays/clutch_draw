from pygame_gui import UIManager
from clutch_draw.game_state import GameState
from clutch_draw.ui.mouse import mouse_inside
from clutch_draw.ui.buttons import create_button

from pygame import MOUSEMOTION, MOUSEBUTTONUP, Surface
from pygame.event import Event
from pygame.font import Font
import pygame


class GameSetupScreen:

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        screen: Surface,
        title_font: Font,
        manager: UIManager,
        user_data: dict,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.title_font = title_font
        self.manager = manager

        self.background = pygame.image.load("resources/images/orig_big.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.screen_width, self.screen_height)
        )

        self.level = user_data["level"]
        self.selected_mode = "casual"
        self.selected_rank = None

    def render(self, events: list[Event]) -> GameState:

        self.screen.blit(self.background, (0, 0))

        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        casual_button = create_button(self.title_font, "Casual")
        comp_button = create_button(self.title_font, "Competitive")

        bronze_button = create_button(self.title_font, "Bronze")
        silver_button = create_button(self.title_font, "Silver")
        gold_button = create_button(self.title_font, "Gold")

        play_button = create_button(self.title_font, "Play")
        back_button = create_button(self.title_font, "Back")

        centre_x = self.screen_width // 2

        casual_x = centre_x - casual_button.get_width() - 20
        casual_y = 200

        comp_x = centre_x + 20
        comp_y = 200

        bronze_x = centre_x - bronze_button.get_width() - 150
        silver_x = centre_x - silver_button.get_width() // 2
        gold_x = centre_x + 150

        rank_y = 350

        play_x = centre_x - play_button.get_width() // 2
        play_y = 500

        back_x = centre_x - back_button.get_width() // 2
        back_y = 580

        self.screen.blit(casual_button, (casual_x, casual_y))
        self.screen.blit(comp_button, (comp_x, comp_y))

        if self.level < 5:
            overlay = pygame.Surface(
                (comp_button.get_width(), comp_button.get_height())
            )
            overlay.set_alpha(90)
            overlay.fill((100, 100, 100))
            self.screen.blit(overlay, (comp_x, comp_y))

        if self.selected_mode == "competitive":
            self.screen.blit(bronze_button, (bronze_x, rank_y))
            self.screen.blit(silver_button, (silver_x, rank_y))
            self.screen.blit(gold_button, (gold_x, rank_y))

        if self.selected_mode == "casual":
            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                (
                    casual_x,
                    casual_y,
                    casual_button.get_width(),
                    casual_button.get_height(),
                ),
                5,
            )

        elif self.selected_mode == "competitive":
            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                (comp_x, comp_y, comp_button.get_width(), comp_button.get_height()),
                5,
            )

        if self.selected_mode == "competitive":

            if self.selected_rank == "bronze":
                pygame.draw.rect(
                    self.screen,
                    (0, 255, 0),
                    (
                        bronze_x,
                        rank_y,
                        bronze_button.get_width(),
                        bronze_button.get_height(),
                    ),
                    5,
                )

            elif self.selected_rank == "silver":
                pygame.draw.rect(
                    self.screen,
                    (0, 255, 0),
                    (
                        silver_x,
                        rank_y,
                        silver_button.get_width(),
                        silver_button.get_height(),
                    ),
                    5,
                )

            elif self.selected_rank == "gold":
                pygame.draw.rect(
                    self.screen,
                    (0, 255, 0),
                    (gold_x, rank_y, gold_button.get_width(), gold_button.get_height()),
                    5,
                )

        self.screen.blit(play_button, (play_x, play_y))
        self.screen.blit(back_button, (back_x, back_y))

        font = pygame.font.Font("resources/fonts/Apocalypse.ttf", 20)

        if self.level < 5:
            lock_text = font.render(
                "Competitive unlocks at Level 5", True, (225, 80, 80)
            )
            self.screen.blit(lock_text, (centre_x - lock_text.get_width() // 2, 300))

        if self.selected_mode == "competitive":
            if self.level < 10:
                silver_text = font.render(
                    "Silver unlocks at Level 10", True, (255, 80, 80)
                )
                self.screen.blit(silver_text, (silver_x, rank_y + 60))

            if self.level < 15:
                gold_text = font.render("Gold unlocks at Level 15", True, (255, 80, 80))
                self.screen.blit(gold_text, (gold_x, rank_y + 60))

        next_state = GameState.GAME_SETUP_SCREEN

        for event in events:
            if event.type == MOUSEBUTTONUP:

                if mouse_inside(event, back_button, back_x, back_y):
                    return GameState.MAIN_MENU_SCREEN

                if mouse_inside(event, casual_button, casual_x, casual_y):
                    self.selected_mode = "casual"
                    self.selected_rank = None

                elif mouse_inside(event, comp_button, comp_x, comp_y):
                    if self.level >= 5:
                        self.selected_mode = "competitive"
                    else:
                        self.selected_mode = "casual"

                if self.selected_mode == "competitive":

                    if mouse_inside(event, bronze_button, bronze_x, rank_y):
                        self.selected_rank = "bronze"

                    elif mouse_inside(event, silver_button, silver_x, rank_y):
                        if self.level >= 10:
                            self.selected_rank = "silver"

                    elif mouse_inside(event, gold_button, gold_x, rank_y):
                        if self.level >= 15:
                            self.selected_rank = "gold"

                if mouse_inside(event, play_button, play_x, play_y):

                    if self.selected_mode == "competitive":

                        if self.level < 5:
                            return GameState.GAME_SETUP_SCREEN

                        if not self.selected_rank:
                            return GameState.GAME_SETUP_SCREEN

                    self.final_mode = self.selected_mode
                    self.final_rank = self.selected_rank

                    return GameState.GAME_SCREEN

        return next_state
