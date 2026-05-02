import random
import pygame
from pygame_gui import UIManager
from pygame import MOUSEBUTTONUP, Surface
from pygame.event import Event
from pygame.font import Font
from clutch_draw.game_logic.game_manager import GameManager
from clutch_draw.game_state import GameState
from clutch_draw.ui.card import Card
from clutch_draw.ui.player import Player
from clutch_draw.db.utils import Database
from clutch_draw.ui.buttons import create_button
from clutch_draw.ui.mouse import mouse_inside

from pathlib import Path

# Defininf file paths for resources
RESOURCES_PATH = Path(__file__).parent.parent.parent.parent / "resources"
FONTS_PATH = RESOURCES_PATH / "fonts"
IMAGES_PATH = RESOURCES_PATH / "images"
SOUNDS_PATH = RESOURCES_PATH / "sounds"


class GameScreen:

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        screen: Surface,
        title_font: Font,
        text_font: Font,
        manager: UIManager,
        user_data: dict,
        mode="casual",
        rank=None,
    ):
        # Storing screen dimensions so that they can be used when rendering UI elements
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        # Storing fonts with specific sizes for reuse when rendering text
        self.title_font = title_font
        self.text_font = text_font
        self.small_font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 12)
        # Storing UIManager for handling UI updates and event processing
        self.manager = manager
        # Storing the selected game mode and rank
        self.mode = mode
        self.rank = rank

        # Setting the background music volume
        # I have set it to be lower in this particular screen so that the sfx of all the cards can be heard by the user
        pygame.mixer.music.set_volume(0.3)

        # Loading the sound effects for all the different cards to provide audio feedback of their actions
        self.sfx_deal = pygame.mixer.Sound(str(SOUNDS_PATH / "card_dealing.mp3"))
        self.sfx_shuffle = pygame.mixer.Sound(SOUNDS_PATH / "card_movement.mp3")

        self.sfx_executer = pygame.mixer.Sound(str(SOUNDS_PATH / "knife.mp3"))
        self.sfx_hunter = pygame.mixer.Sound(str(SOUNDS_PATH / "arrow.mp3"))
        self.sfx_ambusher = pygame.mixer.Sound(str(SOUNDS_PATH / "grenade.mp3"))
        self.sfx_gunner = pygame.mixer.Sound(str(SOUNDS_PATH / "gunshot.mp3"))

        self.sfx_soldier = pygame.mixer.Sound(str(SOUNDS_PATH / "dog.mp3"))
        self.sfx_enforcer = pygame.mixer.Sound(str(SOUNDS_PATH / "shield.mp3"))
        self.sfx_guardian = pygame.mixer.Sound(str(SOUNDS_PATH / "cat.mp3"))
        self.sfx_engineer = pygame.mixer.Sound(str(SOUNDS_PATH / "shield.mp3"))

        self.sfx_doctor = pygame.mixer.Sound(str(SOUNDS_PATH / "heal.mp3"))
        self.sfx_chemist = pygame.mixer.Sound(str(SOUNDS_PATH / "potion.mp3"))
        self.sfx_scav = pygame.mixer.Sound(str(SOUNDS_PATH / "heal.mp3"))

        # Tracking whether the sfx for the played card has already been triggered or not
        self.sfx_played = False

        # Creating the deck and loading the card back images for each category into it
        self.deck = self.create_deck()
        self.card_backs = {
            "Offence": pygame.image.load(
                IMAGES_PATH / "offence_card_back.png"
            ).convert_alpha(),
            "Defence": pygame.image.load(
                IMAGES_PATH / "defence_card_back.png"
            ).convert_alpha(),
            "Support": pygame.image.load(
                IMAGES_PATH / "support_card_back.png"
            ).convert_alpha(),
        }

        # Creating the initial hands of cards for both players
        self.our_starting_hand = self.create_starting_hand()
        self.opponent_starting_hand = self.create_starting_hand()

        # Initialising both player objects with their health, empty hands and rendering data
        self.our_player = Player(
            100, [], self.screen_width, self.screen_height, self.card_backs
        )
        self.opponent_player = Player(
            100, [], self.screen_width, self.screen_height, self.card_backs
        )

        # Creating an instance of the GameManager in order to handle core game logic
        self.game_manager = GameManager(
            self.our_player, self.opponent_player, self.deck, self
        )

        # Initialising the animations machine starting phase
        self.turn_phase = "dealing"

        # The variables used to control the timing of animations and smooth transitions between states
        self.animation_timer = 0
        self.animation_duration = 60

        # Storing the currently active card being played/animated and its position on the screen
        self.active_card = None
        self.active_card_pos = (0, 0)

        # Doing the same but for the AI's active card
        self.ai_card = None
        self.ai_card_pos = (0, 0)

        # The variables used for handling card drawing animations for both players
        self.drawn_card = None
        self.ai_drawn_card = None
        self.draw_pos = (0, 0)
        self.draw_timer = 0

        # The variable to keep track of how many cards have been dealt to the players during the starting hand animation
        self.deal_index = 0

        # Stores the last card category played to influence future card draws (seen later)
        self.last_played_category = None
        self.ai_last_played_category = None

        # Storing a card that should be rendered above all other elements
        self.render_on_top = None

        self.first_round = True

        # The variables used to manage the transitions between player turns and turn indicators on the user's screen
        self.next_turn_phase = "turn_transition"
        self.transition_text = "Your Turn"
        self.transition_timer = 0
        self.transition_done = False
        self.current_turn = "player"

        # The variables used to track the end of the game and reward calculations
        self.game_over = False
        self.game_result = None
        self.xp_gained = 0
        self.results_processed = False

        # Tracking whether the game is currently paused or not, disabling the player from any gameplay interactions when True
        self.paused = False

        # Retrieving the stored user data for updating the player's progress after the match
        self.username = user_data["username"]
        self.xp = user_data["xp"]
        self.level = user_data["level"]
        self.wins = user_data["wins"]
        self.losses = user_data["losses"]

        # Calculating the XP required for the next level using the system imported from "GameManager"
        _, self.xp_to_next = self.game_manager.calculate_level(self.xp)

        # Defining the clickable area for returning to the main menu after the game ends
        self.menu_button_rect = pygame.Rect(
            self.screen_width // 2 - 100,
            self.screen_height // 2 + 80,
            200,
            60,
        )

        # Loading the background image using the path and scaling it to the screen's dimensions
        self.background = pygame.image.load(IMAGES_PATH / "orig_big.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.screen_width, self.screen_height)
        )

    # The card drawing system of the game, holds a slight bias on which card gets drawn based on the previous card category played and the rank of the game
    def draw_card(self, last_category, difficulty="casual"):

        if not self.deck:
            return None

        categories_in_hand = {c.category for c in self.our_player.hand}

        if "Offence" not in categories_in_hand:
            offence_cards = [c for c in self.deck if c.category == "Offence"]
            if offence_cards:
                card = random.choice(offence_cards)
                self.deck.remove(card)
                return card

        # Defines how strongly the draw system favours repeatig the previous card category based on the rank of the game

        bias_map = {
            "casual": 0.5,
            "bronze": 0.6,
            "silver": 0.7,
            "gold": 0.8,
        }

        bias = bias_map.get(difficulty, 0.5)

        # If a previous category exists, there is a chance to draw a similar card
        if last_category and random.random() < bias:
            filtered = [c for c in self.deck if c.category == last_category]
            if filtered:
                card = random.choice(filtered)
                self.deck.remove(card)
                return card

        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

    # Creating and returning the full deck of cards available for play in the game
    # Acts as a global pool, to be used for dealing starting cards and returning and drawing cards throughout the game
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
                22,
            ),
            Card(
                "Gunner",
                self.text_font,
                self.small_font,
                "DMG",
                "resources/images/gunner.png",
                "Offence",
                26,
            ),
            Card(
                "Executer",
                self.text_font,
                self.small_font,
                "DMG",
                "resources/images/executer.png",
                "Offence",
                24,
            ),
            Card(
                "Ambusher",
                self.text_font,
                self.small_font,
                "DMG",
                "resources/images/ambusher.png",
                "Offence",
                28,
            ),
            # Defence
            Card(
                "Soldier",
                self.text_font,
                self.small_font,
                "SH",
                "resources/images/soldier.png",
                "Defence",
                16,
            ),
            Card(
                "Enforcer",
                self.text_font,
                self.small_font,
                "SH",
                "resources/images/enforcer.png",
                "Defence",
                22,
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
                "Engineer",
                self.text_font,
                self.small_font,
                "SH",
                "resources/images/engineer.png",
                "Defence",
                20,
            ),
            # Support
            Card(
                "Chemist",
                self.text_font,
                self.small_font,
                "HP",
                "resources/images/chemist.png",
                "Support",
                22,
            ),
            Card(
                "Scav",
                self.text_font,
                self.small_font,
                "HP",
                "resources/images/scav.png",
                "Support",
                20,
            ),
            Card(
                "Doctor",
                self.text_font,
                self.small_font,
                "HP",
                "resources/images/doctor.png",
                "Support",
                26,
            ),
        ]

    # Creates a starting hand of 2 Offence cards, 2 Defence cards and 1 Support card for both players and removes these cards from the deck
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

        # Allows the player to return to the "Main Menu" screen if a click has been detected on the appropriate button in the game over overlay
        if self.game_over:
            for event in events:
                if event.type == MOUSEBUTTONUP:
                    if self.menu_button_rect.collidepoint(event.pos):
                        return GameState.MAIN_MENU_SCREEN

        # Drawing the background image onto the screen
        self.screen.blit(
            self.background, (0, 0)
        )  # (0, 0) refers to the top-left position of the screen

        # Drawing the same semi-transparent overlay that is in other screens
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(
            120
        )  # Even though this is not more of a functional screen but rather an actual game screen, the overlay is kept darker
        # this is because of the amount of UI on the screen that the user needs to be focused on
        overlay.fill((0, 0, 0))
        self.screen.blit(
            overlay, (0, 0)
        )  # (0, 0) refers to the top-left position of the screen

        # Creating the "Pause"/"Resume" and "Quit" buttons
        label = "Resume" if self.paused else "Pause"
        self.pause_button = create_button(self.title_font, label, 140, 50)
        self.quit_button = create_button(self.title_font, "Quit", 140, 50)

        # Positioning the buttons
        pause_x = 40
        pause_y = self.screen_height - self.pause_button.get_height() - 80
        quit_x = pause_x
        quit_y = pause_y + self.pause_button.get_height() + 10

        # Drawing them onto the screen
        self.screen.blit(self.pause_button, (pause_x, pause_y))
        self.screen.blit(self.quit_button, (quit_x, quit_y))

        # Processing all input events made by the user
        for event in events:

            if event.type == MOUSEBUTTONUP and not self.game_over:

                # Checking if the user's mouse if inside the button's surface/rectangle and if it has been clicked on
                if mouse_inside(event, self.pause_button, pause_x, pause_y):
                    self.paused = not self.paused
                    # If the "Pause" button is clicked the pause overlay displays onto the user's screen,
                    # and all interaction with the screen is blocked until the user clicks "Resume"

                # Checking if the user's mouse if inside the button's surface/rectangle and if it has been clicked on
                if mouse_inside(event, self.quit_button, quit_x, quit_y):
                    return GameState.MAIN_MENU_SCREEN
                    # If the "Quit" button is clicked the game stops and the user gets redirected to the "Main Menu" screen

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused

                if event.key == pygame.K_q:
                    return GameState.MAIN_MENU_SCREEN

            if event.type == pygame.KEYDOWN and not self.paused and not self.game_over:

                if self.turn_phase == "player_idle":

                    key_map = {
                        pygame.K_1: 0,
                        pygame.K_2: 1,
                        pygame.K_3: 2,
                        pygame.K_4: 3,
                        pygame.K_5: 4,
                    }

                    if event.key in key_map:
                        index = key_map[event.key]

                        if index < len(self.our_player.hand):
                            card = self.our_player.hand[index]

                            for c, x, y in self.our_player.card_positions:
                                if c == card:
                                    self.active_card = card
                                    self.active_card_pos = (x, y)
                                    break

                            self.our_player.hand.remove(card)
                            self.last_played_category = card.category

                            self.turn_phase = "player_animating"
                            self.animation_timer = 0

                    elif event.key == pygame.K_d and self.turn_phase == "player_idle":
                        self.turn_phase = "player_draw"

        # Defining the card dimensions for positioning them in the hand and deck visuals
        card_width = 100
        card_gap = 15

        # Positioning the stacked deck of cards onto the screen
        deck_x = self.screen_width // 6
        deck_y = 375
        # Defining a clickable area for the deck
        deck_rect = pygame.Rect(deck_x - 50, deck_y - 70, 100, 140)

        # Rendering a stacked visual of the deck of cards using their rotated card backs
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

        # Rendering both players details
        self.opponent_player.render(self.screen, x=200, y=100, hide_hand=True)
        self.our_player.render(self.screen, x=200, y=480, hide_hand=False)

        # Getting the position of the user's mouse for hover detection later
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # When the user's mouse is on a card it gets englared to provide a hovering effect for better visual clarity of the card
        if self.turn_phase == "player_idle" and not self.paused:
            for card, x, y in self.our_player.card_positions:
                rect = pygame.Rect(x, y, 100, 140)
                if rect.collidepoint(mouse_x, mouse_y):
                    self.render_on_top = (card, x, y, 2.2)
                    break

        # "State Machine" which controls all gameplay phases including their animations, turns and transitions
        # Each "turn_phase" represents a different stage of the game flow

        if not self.game_over and not self.paused:

            if self.turn_phase == "dealing":
                self.animation_timer += 1

                if self.animation_timer >= 15:

                    if self.deal_index < 5:

                        self.sfx_deal.play()

                        self.our_player.hand.append(
                            self.our_starting_hand[self.deal_index]
                        )
                        self.opponent_player.hand.append(
                            self.opponent_starting_hand[self.deal_index]
                        )
                        self.deal_index += 1
                        self.animation_timer = 0
                    else:
                        self.turn_phase = "player_idle"
                        self.animation_timer = 0

            elif self.turn_phase == "player_idle" and not self.paused:
                for event in events:
                    if event.type == MOUSEBUTTONUP:
                        mouse_x, mouse_y = event.pos

                        # Clicking the deck to draw a card
                        if (
                            deck_rect.collidepoint(event.pos)
                            and len(self.our_player.hand) < 5
                        ):
                            self.turn_phase = "player_draw"
                            break

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

                if self.animation_timer == 0:
                    self.sfx_shuffle.play()
                    self.sfx_played = False

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

                if not self.sfx_played:
                    self.game_manager.play_card(
                        self.our_player, self.opponent_player, self.active_card
                    )
                    self.sfx_played = True

                self.animation_timer += 1

                cx = self.screen_width // 2 - 50
                cy = self.screen_height // 2 - 70

                self.render_on_top = (self.active_card, cx, cy, 2.2)

                if self.animation_timer >= 50:
                    self.turn_phase = "player_pause"
                    self.animation_timer = 0

            elif self.turn_phase == "player_pause":
                self.animation_timer += 1

                cx = self.screen_width // 2 - 50
                cy = self.screen_height // 2 - 70

                self.render_on_top = (self.active_card, cx, cy, 2.2)

                if self.animation_timer >= 45:

                    self.turn_phase = "player_to_deck"
                    self.animation_timer = 0

            elif self.turn_phase == "player_to_deck":

                if self.animation_timer == 0:
                    self.sfx_shuffle.play()

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
                    if self.first_round:
                        self.next_turn_phase = "ai_animating"
                    else:
                        self.next_turn_phase = "ai_thinking"
                    self.transition_timer = 0

                    self.draw_timer = 0
                    self.ai_drawn_card = None

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

            # AI Draw

            elif self.turn_phase == "ai_draw_anim":

                if self.draw_timer == 0:
                    self.sfx_shuffle.play()

                if self.ai_drawn_card is None:
                    difficulty = "casual"
                    if self.mode == "competitive":
                        difficulty = self.rank

                    self.ai_drawn_card = self.draw_card(
                        self.ai_last_played_category, difficulty
                    )

                    if self.ai_drawn_card is None:
                        self.turn_phase = "ai_thinking"
                        self.draw_timer = 0
                        return GameState.GAME_SCREEN

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

                if self.draw_timer == 0:
                    self.sfx_shuffle.play()

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

                    self.current_turn = "player"

                    self.turn_phase = "turn_transition"
                    self.transition_text = "Your Turn"
                    self.next_turn_phase = "player_idle"

                    self.draw_timer = 0
                    self.animation_timer = 0

            elif self.turn_phase == "ai_thinking":

                self.animation_timer += 1

                if self.animation_timer >= 45:

                    difficulty = "casual"
                    if self.mode == "competitive":
                        difficulty = self.rank

                    draw_chance = {
                        "casual": 0.3,
                        "bronze": 0.25,
                        "silver": 0.2,
                        "gold": 0.15,
                    }.get(difficulty, 0.25)

                    if len(self.opponent_player.hand) >= 5:
                        self.turn_phase = "ai_animating"

                    else:

                        if len(self.opponent_player.hand) < 3:
                            should_draw = True
                        else:

                            should_draw = random.random() < draw_chance

                        if should_draw:
                            self.turn_phase = "ai_draw_anim"
                        else:
                            self.turn_phase = "ai_animating"

                    self.animation_timer = 0

            # AI Play

            elif self.turn_phase == "ai_animating":

                if self.animation_timer == 0:
                    self.sfx_shuffle.play()
                    self.sfx_played = False

                if self.ai_card is None:

                    difficulty = "casual"

                    if self.mode == "competitive":
                        difficulty = self.rank

                    self.ai_card = self.game_manager.choose_ai_card(
                        self.opponent_player, self.our_player, difficulty
                    )

                    index = self.opponent_player.hand.index(self.ai_card)

                    # Recalculating card layout for opponent hand positioning during its animations
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

                    self.opponent_player.hand.remove(self.ai_card)

                    self.ai_last_played_category = self.ai_card.category

                    self.animation_timer = 0

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

                if not self.sfx_played:
                    self.game_manager.play_card(
                        self.opponent_player, self.our_player, self.ai_card
                    )
                    self.sfx_played = True

                self.animation_timer += 1

                cx = self.screen_width // 2 - 50
                cy = self.screen_height // 2 - 70

                self.render_on_top = (self.ai_card, cx, cy, 2.2)

                if self.animation_timer >= 50:
                    self.turn_phase = "ai_pause"
                    self.animation_timer = 0

            elif self.turn_phase == "ai_pause":

                self.animation_timer += 1

                cx = self.screen_width // 2 - 50
                cy = self.screen_height // 2 - 70

                self.render_on_top = (self.ai_card, cx, cy, 2.2)

                if self.animation_timer >= 45:

                    self.turn_phase = "ai_to_deck"
                    self.animation_timer = 0

            elif self.turn_phase == "ai_to_deck":

                if self.animation_timer == 0:
                    self.sfx_shuffle.play()

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
                    self.next_turn_phase = "player_idle"
                    self.draw_timer = 0
                    self.drawn_card = None
                    self.animation_timer = 0

            # Player Draw

            elif self.turn_phase == "player_draw":

                if len(self.our_player.hand) >= 5:
                    return GameState.GAME_SCREEN

                if self.drawn_card is None:

                    difficulty = "casual"
                    if self.mode == "competitive":
                        difficulty = self.rank

                    self.drawn_card = self.draw_card(
                        self.last_played_category, difficulty
                    )

                    if self.drawn_card is None:
                        return GameState.GAME_SCREEN

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

                if self.draw_timer == 0:
                    self.sfx_shuffle.play()

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

                if self.draw_timer == 0:
                    self.sfx_shuffle.play()

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

                    self.current_turn = "ai"

                    self.turn_phase = "turn_transition"
                    self.transition_text = "Opponent's Turn"
                    self.next_turn_phase = "ai_thinking"

            if self.turn_phase == "player_idle":
                font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 25)
                text = font.render(
                    "1-5: Play Card   |   D: Draw", True, (255, 255, 255)
                )

                self.screen.blit(
                    text,
                    (
                        self.screen_width // 2 - text.get_width() // 2,
                        650,
                    ),
                )

        # End of "State Machine", everything has been processed above

        # Rendering hovered or animating card in top of all other elements to ensure clear visibility
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

        if self.turn_phase == "turn_transition":

            font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 80)

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

            font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 40)
            color = (0, 255, 0) if is_player_turn else (255, 80, 80)

            text_surface = font.render(turn_text, True, color)

            self.screen.blit(
                text_surface,
                (
                    self.screen_width // 2 - text_surface.get_width() // 2,
                    40,
                ),
            )

            mode_font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf")

            mode_text = self.mode

            if self.mode == "competitive" and self.rank:
                mode_text += f" ({self.rank})"

            mode_surface = mode_font.render(mode_text, True, (255, 255, 255))

            self.screen.blit(mode_surface, (20, 20))

        # Processing and calculating the end of the game results and rewards
        if not self.game_over:
            result = self.game_manager.check_game_over()

            if result:
                self.game_over = True
                self.game_result = result

        if self.game_over and not self.results_processed:

            if self.game_result == "win":
                self.xp_gained = 50
                self.wins += 1
            else:
                self.xp_gained = 20
                self.losses += 1

            self.xp += self.xp_gained

            self.level, self.xp_to_next = self.game_manager.calculate_level(self.xp)

            db = Database()
            db.update_account(
                self.username,
                self.xp,
                self.level,
                self.wins,
                self.losses,
            )

            self.results_processed = True

        if self.paused and not self.game_over:

            overlay = pygame.Surface((self.screen_width, self.screen_height))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 80)
            text = font.render("Paused", True, (255, 255, 255))

            self.screen.blit(
                text,
                (
                    self.screen_width // 2 - text.get_width() // 2,
                    self.screen_height // 2 - text.get_height() // 2,
                ),
            )

        # Rendering the game over screen with results and rewards as an overlay on the user's screen
        if self.game_over:

            overlay = pygame.Surface((self.screen_width, self.screen_height))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            font_big = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 80)

            if self.game_result == "win":
                result_text = "YOU WIN"
                color = (0, 255, 0)
            else:
                result_text = "YOU LOSE"
                color = (255, 80, 80)

            result_surface = font_big.render(result_text, True, color)

            self.screen.blit(
                result_surface,
                (
                    self.screen_width // 2 - result_surface.get_width() // 2,
                    self.screen_height // 2 - 120,
                ),
            )

            # XP text
            font_small = pygame.font.Font(FONTS_PATH // "Apocalypse.ttf", 40)

            xp_surface = font_small.render(
                f"XP Gained: {self.xp_gained}", True, (255, 255, 255)
            )

            self.screen.blit(
                xp_surface,
                (
                    self.screen_width // 2 - xp_surface.get_width() // 2,
                    self.screen_height // 2,
                ),
            )

            pygame.draw.rect(self.screen, (40, 40, 40), self.menu_button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), self.menu_button_rect, 3)

            font = pygame.font.Font(FONTS_PATH / "Apocalypse.ttf", 30)
            text_surface = font.render("MAIN MENU", True, (255, 255, 255))

            self.screen.blit(
                text_surface,
                (
                    self.menu_button_rect.centerx - text_surface.get_width() // 2,
                    self.menu_button_rect.centery - text_surface.get_height() // 2,
                ),
            )

        # Rendering these buttons on top of everything else on the screen so that animations and overlays don't cover them
        self.screen.blit(self.pause_button, (pause_x, pause_y))
        self.screen.blit(self.quit_button, (quit_x, quit_y))

        # Returning the next game state so that the main game loop can handle screen transitions and update the display
        return GameState.GAME_SCREEN
