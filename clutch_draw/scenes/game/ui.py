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
        self.small_font = pygame.font.Font("resources/fonts/Apocalypse.ttf", 12)
        self.manager = manager

        self.deck = self.create_deck()
        self.card_backs = {
            "Offence": pygame.image.load(
                "resources/images/offence_card_back.png"
            ).convert_alpha(),
            "Defence": pygame.image.load(
                "resources/images/defence_card_back.png"
            ).convert_alpha(),
            "Support": pygame.image.load(
                "resources/images/support_card_back.png"
            ).convert_alpha(),
        }

        self.our_starting_hand = self.create_starting_hand()
        self.opponent_starting_hand = self.create_starting_hand()

        self.our_player = Player(
            100, [], self.screen_width, self.screen_height, self.card_backs
        )
        self.opponent_player = Player(
            100, [], self.screen_width, self.screen_height, self.card_backs
        )

        self.game_manager = GameManager(
            self.our_player, self.opponent_player, self.deck
        )

        self.turn_phase = "dealing"

        self.animation_timer = 0
        self.animation_duration = 40

        self.active_card = None
        self.active_card_pos = (0, 0)

        self.ai_card = None
        self.ai_card_pos = (0, 0)

        self.drawn_card = None
        self.ai_drawn_card = None

        self.draw_pos = (0, 0)
        self.draw_timer = 0

        self.deal_index = 0

        self.last_played_category = None
        self.ai_last_played_category = None

        self.render_on_top = None

        self.first_round = True

        self.next_turn_phase = "turn_transition"
        self.transition_text = "Your Turn"
        self.transition_timer = 0

        self.transition_done = False
        self.current_turn = "player"

    def create_deck(self):
        return [
            # Offence
            Card(
                "Hunter",
                self.text_font,
                self.small_font,
                "DMG",
                "resources/images/hunter.png",
                "Offence",
                20,
            ),
            Card(
                "Raider",
                self.text_font,
                self.small_font,
                "DMG",
                "resources/images/guardian.png",
                "Offence",
                25,
            ),
            Card(
                "Smuggler",
                self.text_font,
                self.small_font,
                "DMG",
                "resources/images/guardian.png",
                "Offence",
                22,
            ),
            Card(
                "Executer",
                self.text_font,
                self.small_font,
                "DMG",
                "resources/images/guardian.png",
                "Offence",
                30,
            ),
            Card(
                "Ambusher",
                self.text_font,
                self.small_font,
                "DMG",
                "resources/images/guardian.png",
                "Offence",
                18,
            ),
            # Defence
            Card(
                "Soldier",
                self.text_font,
                self.small_font,
                "SH",
                "resources/images/soldier.png",
                "Defence",
                15,
            ),
            Card(
                "Enforcer",
                self.text_font,
                self.small_font,
                "SH",
                "resources/images/guardian.png",
                "Defence",
                20,
            ),
            Card(
                "Guardian",
                self.text_font,
                self.small_font,
                "SH",
                "resources/images/guardian.png",
                "Defence",
                18,
            ),
            Card(
                "Gunner",
                self.text_font,
                self.small_font,
                "SH",
                "resources/images/guardian.png",
                "Defence",
                25,
            ),
            Card(
                "Bunker",
                self.text_font,
                self.small_font,
                "SH",
                "resources/images/guardian.png",
                "Defence",
                12,
            ),
            # Support
            Card(
                "Supply Runner",
                self.text_font,
                self.small_font,
                "HP",
                "resources/images/guardian.png",
                "Support",
                22,
            ),
            Card(
                "Field Medic",
                self.text_font,
                self.small_font,
                "HP",
                "resources/images/guardian.png",
                "Support",
                20,
            ),
            Card(
                "Survivor",
                self.text_font,
                self.small_font,
                "HP",
                "resources/images/guardian.png",
                "Support",
                15,
            ),
            Card(
                "Scav",
                self.text_font,
                self.small_font,
                "HP",
                "resources/images/guardian.png",
                "Support",
                18,
            ),
            Card(
                "Doctor",
                self.text_font,
                self.small_font,
                "HP",
                "resources/images/doctor.png",
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

        card_width = 100
        card_gap = 15

        deck_x = self.screen_width // 6
        deck_y = 375

        # deck visuals

        for i, angle in enumerate([-15, -8, 0, 8, 15][::-1]):
            if self.deck:
                card = self.deck[-(i + 1)] if i < len(self.deck) else self.deck[0]
                back_image = self.card_backs.get(
                    card.category, self.card_backs["Defence"]
                )
            else:
                back_image = self.card_backs["Defence"]

            rotated = pygame.transform.rotate(back_image, angle)
            rect = rotated.get_rect(center=(deck_x, deck_y))
            self.screen.blit(rotated, (rect.x + i, rect.y - i))

        self.opponent_player.render(self.screen, x=200, y=100, hide_hand=True)
        self.our_player.render(self.screen, x=200, y=480, hide_hand=False)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.turn_phase == "player_idle":
            for card, x, y in self.our_player.card_positions:
                rect = pygame.Rect(x, y, 100, 140)
                if rect.collidepoint(mouse_x, mouse_y):
                    card.render(self.screen, x, y, scale=2.2)
                    break

        # State Machine

        if self.turn_phase == "dealing":
            self.animation_timer += 1

            if self.animation_timer >= 15:
                if self.deal_index < 5:
                    self.our_player.hand.append(self.our_starting_hand[self.deal_index])
                    self.opponent_player.hand.append(
                        self.opponent_starting_hand[self.deal_index]
                    )
                    self.deal_index += 1
                    self.animation_timer = 0
                else:
                    self.turn_phase = "player_idle"
                    self.animation_timer = 0

        elif self.turn_phase == "player_idle":
            for event in events:
                if event.type == MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos

                    for card, x, y in self.our_player.card_positions:
                        rect = pygame.Rect(x, y, 100, 140)

                        if rect.collidepoint(mouse_x, mouse_y):
                            self.active_card = card
                            self.active_card_pos = (x, y)
                            self.our_player.hand.remove(card)

                            self.last_played_category = card.category

                            self.turn_phase = "player_animating"
                            self.animation_timer = 0
                            break

        elif self.turn_phase == "player_animating":
            self.animation_timer += 1
            progress = min(self.animation_timer / self.animation_duration, 1)

            cx = self.screen_width // 2 - 50
            cy = self.screen_height // 2 - 70

            x = self.active_card_pos[0] + (cx - self.active_card_pos[0]) * progress
            y = self.active_card_pos[1] + (cy - self.active_card_pos[1]) * progress

            self.render_on_top = (self.active_card, int(x), int(y), 2.2)

            if progress >= 1:
                self.turn_phase = "player_showing"
                self.animation_timer = 0

        elif self.turn_phase == "player_showing":
            self.animation_timer += 1
            cx = self.screen_width // 2 - 50
            cy = self.screen_height // 2 - 70

            self.render_on_top = (self.active_card, cx, cy, 2.2)

            if self.animation_timer >= 35:
                self.turn_phase = "player_pause"
                self.animation_timer = 0

        elif self.turn_phase == "player_pause":
            self.animation_timer += 1

            cx = self.screen_width // 2 - 50
            cy = self.screen_height // 2 - 70

            self.render_on_top = (self.active_card, cx, cy, 2.2)

            if self.animation_timer >= 30:
                self.game_manager.play_card(
                    self.our_player, self.opponent_player, self.active_card
                )
                self.turn_phase = "player_to_deck"
                self.animation_timer = 0

        elif self.turn_phase == "player_to_deck":
            self.animation_timer += 1
            progress = min(self.animation_timer / self.animation_duration, 1)

            cx = self.screen_width // 2 - 50
            cy = self.screen_height // 2 - 70

            x = cx + (deck_x - cx) * progress
            y = cy + (deck_y - cy) * progress

            self.render_on_top = (self.active_card, int(x), int(y), 2.2)

            if progress >= 1:
                if self.active_card is not None:
                    self.deck.append(self.active_card)
                self.active_card = None

                self.current_turn = "ai"

                self.turn_phase = "turn_transition"
                self.transition_text = "Opponent's Turn"
                self.next_turn_phase = (
                    "ai_animating" if self.first_round else "ai_draw_anim"
                )
                self.transition_timer = 0

                self.draw_timer = 0
                self.ai_drawn_card = None

        # ✅ FIXED TRANSITION
        elif self.turn_phase == "turn_transition":

            self.transition_timer += 1

            if self.transition_timer >= 90:
                self.transition_done = True

            if self.transition_done:
                self.transition_done = False
                self.transition_timer = 0

                if self.next_turn_phase == "player_draw":
                    self.turn_phase = "player_pre_draw"
                else:
                    self.turn_phase = self.next_turn_phase

        elif self.turn_phase == "player_pre_draw":
            self.animation_timer += 1

            if self.animation_timer >= 2:
                self.turn_phase = "player_draw"
                self.animation_timer = 0

        # =========================
        # AI DRAW (only after round 1)
        # =========================

        elif self.turn_phase == "ai_draw_anim":

            if self.draw_timer == 0:
                self.ai_drawn_card = None

            if self.ai_drawn_card is None:
                available = [
                    c for c in self.deck if c.category == self.ai_last_played_category
                ]

                if not available:
                    available = self.deck

                if available:
                    self.ai_drawn_card = random.choice(available)
                    self.deck.remove(self.ai_drawn_card)
                    self.draw_pos = (deck_x, deck_y)

            self.draw_timer += 1
            progress = min(self.draw_timer / 55, 1)

            scale = 1.5

            card_w = int(100 * scale)
            card_h = int(140 * scale)

            cx = self.screen_width // 2
            cy = self.screen_height // 2

            x = self.draw_pos[0] + (cx - self.draw_pos[0]) * progress
            y = self.draw_pos[1] + (cy - self.draw_pos[1]) * progress

            draw_x = x - card_w // 2
            draw_y = y - card_h // 2

            self.render_on_top = (
                self.card_backs[self.ai_drawn_card.category],
                int(draw_x),
                int(draw_y),
                scale,
            )

            if progress >= 1:
                self.turn_phase = "ai_draw_pause"
                self.draw_timer = 0

        elif self.turn_phase == "ai_draw_pause":

            self.draw_timer += 1

            scale = 2.2

            card_w = int(100 * scale)
            card_h = int(140 * scale)

            cx = self.screen_width // 2
            cy = self.screen_height // 2

            draw_x = cx - card_w // 2
            draw_y = cy - card_h // 2

            self.render_on_top = (
                self.card_backs[self.ai_drawn_card.category],
                draw_x,
                draw_y,
                scale,
            )

            if self.draw_timer >= 55:
                self.turn_phase = "ai_draw_to_hand"
                self.draw_timer = 0

        elif self.turn_phase == "ai_draw_to_hand":

            self.draw_timer += 1
            progress = min(self.draw_timer / 55, 1)

            cx = self.screen_width // 2 - 50
            cy = self.screen_height // 2 - 70

            target_x = 200
            target_y = 100

            x = cx + (target_x - cx) * progress
            y = cy + (target_y - cy) * progress

            self.render_on_top = (
                self.card_backs[self.ai_drawn_card.category],
                int(x),
                int(y),
                1.5,
            )

            if progress >= 1:
                if self.ai_drawn_card is not None:
                    self.opponent_player.hand.append(self.ai_drawn_card)
                self.ai_drawn_card = None

                self.turn_phase = "ai_thinking"
                self.animation_timer = 0

        elif self.turn_phase == "ai_thinking":

            self.animation_timer += 1

            if self.animation_timer >= 30:
                self.turn_phase = "ai_animating"
                self.animation_timer = 0

        # =========================
        # AI PLAY
        # =========================

        elif self.turn_phase == "ai_animating":

            if self.ai_card is None:

                self.ai_card = random.choice(self.opponent_player.hand)

                # GET POSITION BEFORE REMOVAL
                index = self.opponent_player.hand.index(self.ai_card)

                card_width = 100
                card_gap = 15

                total_width = (
                    len(self.opponent_player.hand) * card_width
                    + (len(self.opponent_player.hand) - 1) * card_gap
                )
                start_x = (self.screen_width - total_width) // 2

                card_x = start_x + index * (card_width + card_gap)
                card_y = 100

                self.ai_card_pos = (card_x, card_y)

                # REMOVE IMMEDIATELY
                self.opponent_player.hand.remove(self.ai_card)

                self.ai_last_played_category = self.ai_card.category

                self.animation_timer = 0  # reset properly

            self.animation_timer += 1
            progress = min(self.animation_timer / self.animation_duration, 1)

            cx = self.screen_width // 2 - 50
            cy = self.screen_height // 2 - 70

            x = self.ai_card_pos[0] + (cx - self.ai_card_pos[0]) * progress
            y = self.ai_card_pos[1] + (cy - self.ai_card_pos[1]) * progress

            self.render_on_top = (self.ai_card, int(x), int(y), 2.2)

            if progress >= 1:
                self.turn_phase = "ai_showing"
                self.animation_timer = 0

        elif self.turn_phase == "ai_showing":

            self.animation_timer += 1

            cx = self.screen_width // 2 - 50
            cy = self.screen_height // 2 - 70

            self.render_on_top = (self.ai_card, cx, cy, 2.2)

            if self.animation_timer >= 35:
                self.turn_phase = "ai_pause"
                self.animation_timer = 0

        elif self.turn_phase == "ai_pause":

            self.animation_timer += 1

            cx = self.screen_width // 2 - 50
            cy = self.screen_height // 2 - 70

            self.render_on_top = (self.ai_card, cx, cy, 2.2)

            if self.animation_timer >= 30:
                self.game_manager.play_card(
                    self.opponent_player, self.our_player, self.ai_card
                )
                self.turn_phase = "ai_to_deck"
                self.animation_timer = 0

        elif self.turn_phase == "ai_to_deck":

            self.animation_timer += 1
            progress = min(self.animation_timer / self.animation_duration, 1)

            cx = self.screen_width // 2 - 50
            cy = self.screen_height // 2 - 70

            x = cx + (deck_x - cx) * progress
            y = cy + (deck_y - cy) * progress

            self.render_on_top = (self.ai_card, int(x), int(y), 2.2)

            if progress >= 1:
                if self.ai_card is not None:
                    self.deck.append(self.ai_card)

                self.ai_card = None
                self.current_turn = "player"

                if self.first_round:
                    self.first_round = False

                self.turn_phase = "turn_transition"
                self.transition_text = "Your Turn"
                self.next_turn_phase = "player_draw"
                self.draw_timer = 0
                self.drawn_card = None
                self.animation_timer = 0

        # =========================
        # PLAYER DRAW
        # =========================

        elif self.turn_phase == "player_draw":

            if self.drawn_card is None:

                available = [
                    c for c in self.deck if c.category == self.last_played_category
                ]

                if not available:
                    available = self.deck

                if available:
                    self.drawn_card = random.choice(available)
                    self.deck.remove(self.drawn_card)

                    self.draw_pos = (deck_x, deck_y)
                    self.draw_timer = 0

            cx = self.screen_width // 2 - 50
            cy = self.screen_height // 2 - 70

            self.render_on_top = (
                self.card_backs[self.drawn_card.category],
                int(self.draw_pos[0]),
                int(self.draw_pos[1]),
                1.5,
            )

            self.turn_phase = "player_draw_anim"

        elif self.turn_phase == "player_draw_anim":

            self.draw_timer += 1
            progress = min(self.draw_timer / 55, 1)

            cx = self.screen_width // 2 - 50
            cy = self.screen_height // 2 - 70

            x = self.draw_pos[0] + (cx - self.draw_pos[0]) * progress
            y = self.draw_pos[1] + (cy - self.draw_pos[1]) * progress

            self.render_on_top = (
                self.card_backs[self.drawn_card.category],
                int(x),
                int(y),
                1.5,
            )

            if progress >= 1:
                self.turn_phase = "player_draw_reveal"
                self.draw_timer = 0

        elif self.turn_phase == "player_draw_reveal":

            self.draw_timer += 1

            cx = self.screen_width // 2 - 50
            cy = self.screen_height // 2 - 70

            self.render_on_top = (self.drawn_card, cx, cy, 2.2)

            if self.draw_timer >= 55:
                self.turn_phase = "player_draw_to_hand"
                self.draw_timer = 0

        elif self.turn_phase == "player_draw_to_hand":

            self.draw_timer += 1
            progress = min(self.draw_timer / 55, 1)

            hand_index = len(self.our_player.hand)

            total_width = (hand_index + 1) * card_width + hand_index * card_gap
            start_x = (self.screen_width - total_width) // 2

            target_x = start_x + hand_index * (card_width + card_gap)
            target_y = 480

            cx = self.screen_width // 2 - 50
            cy = self.screen_height // 2 - 70

            x = cx + (target_x - cx) * progress
            y = cy + (target_y - cy) * progress

            self.render_on_top = (self.drawn_card, int(x), int(y), 1.5)

            if progress >= 1:
                if self.drawn_card is not None:
                    self.our_player.hand.append(self.drawn_card)
                self.drawn_card = None

                self.turn_phase = "player_idle"

        # =========================
        # DRAW ON TOP
        # =========================

        if self.render_on_top:
            card, x, y, scale = self.render_on_top

            if isinstance(card, pygame.Surface):
                scaled = pygame.transform.scale(
                    card, (int(100 * scale), int(140 * scale))
                )
                self.screen.blit(scaled, (x, y))
            else:
                card.render(self.screen, x, y, scale)

            self.render_on_top = None

        # TRANSITION TEXT
        if self.turn_phase == "turn_transition":

            font = pygame.font.Font("resources/fonts/Apocalypse.ttf", 80)

            color = (
                (0, 255, 0) if self.transition_text == "Your Turn" else (255, 80, 80)
            )

            text_surface = font.render(self.transition_text, True, color)

            self.screen.blit(
                text_surface,
                (
                    self.screen_width // 2 - text_surface.get_width() // 2,
                    self.screen_height // 2 - text_surface.get_height() // 2,
                ),
            )

        if self.turn_phase != "turn_transition":

            is_player_turn = self.current_turn == "player"

            turn_text = "Your Turn" if is_player_turn else "Opponent's Turn"

            font = pygame.font.Font("resources/fonts/Apocalypse.ttf", 40)
            color = (0, 255, 0) if is_player_turn else (255, 80, 80)

            text_surface = font.render(turn_text, True, color)

            self.screen.blit(
                text_surface,
                (
                    self.screen_width // 2 - text_surface.get_width() // 2,
                    40,
                ),
            )

        result = self.game_manager.check_game_over()
        if result:
            print(result)

        return GameState.GAME_SCREEN
