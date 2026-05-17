import random
from clutch_draw.ui.player import Player
from clutch_draw.ui.card import Card

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from clutch_draw.scenes.game.ui import GameScreen


class GameManager:
    def __init__(
        self,
        player: Player,
        opponent: Player,
        deck: list[Card],
        game_screen: "GameScreen",
    ):
        # Stores the player so that the health, shield and hand can be accessed
        self.player = player
        # Stores the AI opponent for the same reason
        self.opponent = opponent
        # Stores the deck of cards
        self.deck = deck
        self.turn = "player"
        # Keeping track of whose turn it is, can be either "Player" or "AI"
        self.game_screen = game_screen

    def play_card(self, current: Player, opponent: Player, card: Card):

        # Debugging output for testing to track the game state before the card is applied
        print("PLAYING CARD:", card.title)
        print("BEFORE -> Opponent Health:", opponent.health, "Shield:", opponent.shield)

        # Offence cards deal damage to the opponenet, taking into account any shield first
        if card.category == "Offence":

            # Playing a specific sound effect depending on the card used
            if card.title == "Hunter":
                self.game_screen.sfx_hunter.play()

            elif card.title == "Executer":
                self.game_screen.sfx_executer.play()

            elif card.title == "Ambusher":
                self.game_screen.sfx_ambusher.play()

            elif card.title == "Gunner":
                self.game_screen.sfx_gunner.play()

            # Initial damage value taken from the card
            damage = card.value

            # If the opponent has a shield it absorbs damage before health is affected
            if opponent.shield > 0:
                if damage <= opponent.shield:
                    opponent.shield -= damage
                    # Shield fully absorbs the damage
                    damage = 0
                else:
                    # Shield is broken and remaining damage carries over to the health
                    damage -= opponent.shield
                    opponent.shield = 0

            # Applying remaining damage to the health
            opponent.health -= damage

            # Preventing the health from dropping below 0
            if opponent.health < 0:
                opponent.health = 0

            # Debugging output for testing
            print("Damage Dealt:", card.value)

        # Defence cards provide the player with a shield as extra protection
        elif card.category == "Defence":

            # Playing a specific sound effect depending on the card used
            if card.title == "Soldier":
                self.game_screen.sfx_soldier.play()

            elif card.title == "Enforcer":
                self.game_screen.sfx_enforcer.play()

            elif card.title == "Guardian":
                self.game_screen.sfx_guardian.play()

            elif card.title == "Engineer":
                self.game_screen.sfx_engineer.play()

            # Increasing the current player's shield value based on the card value played
            current.shield += card.value

            # Debugging output for testing
            print("Shield Gained:", card.value)

        # Support cards regain the player's health
        elif card.category == "Support":

            # Playing a specific sound effect depending on the card used
            if card.title == "Doctor":
                self.game_screen.sfx_doctor.play()

            elif card.title == "Chemist":
                self.game_screen.sfx_chemist.play()

            elif card.title == "Scav":
                self.game_screen.sfx_scav.play()

            # Increasing the current player's health value based on the card value played
            current.health += card.value

            # Ensuring the health does not exceed the maximum value
            if current.health > 100:
                current.health = 100

            # Debugging output for testing
            print("Health Gained:", card.value)

        # Debugging output for testing to show the game state after the card effect has been applied
        print("AFTER -> Opponent Health:", opponent.health, "Shield:", opponent.shield)

    def take_turn(self, player: Player, opponent: Player, card: Card):

        # Playing the selected card and applying its effect
        self.play_card(player, opponent, card)

        # Switching the turn over to the AI opponent
        self.turn = "ai" if self.turn == "player" else "player"

    def ai_turn(self, difficulty="casual"):

        # ai randomly selects a card from its hand to play.
        card = self.choose_ai_card(self.opponent, self.player, difficulty)
        # ai takes its turn by playing the selected card and applying its effects, just like the player.
        self.take_turn(self.opponent, self.player, card)

    def choose_ai_card(self, ai: Player, player: Player, difficulty="casual") -> Card:

        # Casual gamemode AI behaves completely randomly
        if difficulty == "casual":
            return random.choice(ai.hand)

        # The Bronze Rank AI in the Competitive gamemode behaves in a basic rule-based decision making manner using simple heuristics
        if difficulty == "bronze":

            # If the AI's health is low, prioritise healing using a Support card
            if ai.health <= 30:
                support_cards = [c for c in ai.hand if c.category == "Support"]
                if support_cards:
                    return max(support_cards, key=lambda c: c.value)

            # If the AI's shield is low but its health is not critical, prioritise providing a shield by using a Defence card
            if ai.shield <= 10 and ai.health < 70:
                defence_cards = [c for c in ai.hand if c.category == "Defence"]
                if defence_cards:
                    return max(defence_cards, key=lambda c: c.value)

            # Otherwise, prioritise using an Offence card to attack and damage the player's health, selecting the card with the highest damage value in its hand
            offence_cards = [c for c in ai.hand if c.category == "Offence"]
            if offence_cards:
                return max(offence_cards, key=lambda c: c.value)

            # A fallback in case no specific category is available so that the game can continue playing as normal
            return random.choice(ai.hand)

        # The Silver Rank AI in the Competitive gamemode behaves semi-strategically with controlled randomness
        if difficulty == "silver":

            # Focuses only on playing Offence cards to apply pressure on the player
            offence_cards = [c for c in ai.hand if c.category == "Offence"]

            if offence_cards:

                # Sorting the cards in its hand by their damage value
                sorted_cards = sorted(offence_cards, key=lambda c: c.value)
                # Randomly selects from the top 2 cards instead of always choosing the better one out of the two
                # This introduces unpredictability while still maintaining strong play to provide the player with a harder challenege when trying to beat the AI
                return random.choice(sorted_cards[-2:])

            # Fallback
            return random.choice(ai.hand)

        # The Gold Rank AI in the Competitive gamemode behaves using an advanced heuristic-based evaluation system
        if difficulty == "gold":

            best_card = None
            best_score = (
                -999
            )  # Stores the highest evaluated score based on the heuristic evaluation of each card in the hand

            # Evaluating every card using this scoring system to find the highest value cards that would be best to use based on the situation
            for card in ai.hand:
                score = 0

                # Offence cards prioritise dealing damage and playing winning moves
                if card.category == "Offence":
                    score += (
                        card.value * 2
                    )  # The higher the damage value of the Offence card, the higher score and priority it is given

                    # Bonus score if the card can immediately win the game after playing it, system will try to use this Offence card over any other one in the hand
                    if player.health - card.value <= 0:
                        score += 100

                # Defence cards prioritise increasing shield when it is low to reduce incoming damage
                elif card.category == "Defence":
                    if ai.shield < 20:
                        score += (
                            50 - ai.shield
                        )  # Encourages shield building when the shield bar is low
                    else:
                        score -= 10  # A penalty to the score of a card is its use would be unecessary and cause excessive shielding

                # Support cards prioritise healing, but only when necessary
                elif card.category == "Support":
                    if ai.health < 50:
                        score += (
                            100 - ai.health
                        )  # Higher score and priority given when the health is low so healing is urgent
                    else:
                        score -= 20  # A penalty to the score of a card if its use would be unnecessary

                # Keeping track of the highest scoring card
                if score > best_score:
                    best_score = score
                    best_card = card

            # Returning the best evaluated card based on the heuristic scoring
            # It is then played in the "ai_turn()" method
            return best_card

        # Fallback for safety
        return random.choice(ai.hand)

    def check_game_over(self):
        # Checking if the player's health has reached 0, meaning the player has lost
        if (
            self.player.health <= 0
        ):  # Using <= 0 rather than just == 0 ensures robustness in case health values drop below zero due to future changes or errors
            return "loss"
        # Checking if the opponent's health has reached 0, meaning the player has won
        elif self.opponent.health <= 0:
            return "win"
        # If neither player has reached 0 health, the game is still ongoing
        return None

    # Calculating the player's level based on their XP, the XP required for the next level increases as the level increases
    def calculate_level(self, xp: int) -> tuple[int, int]:
        level = 1
        xp_needed = 100

        while xp >= xp_needed:
            xp -= xp_needed
            level += 1
            xp_needed = (
                100 + (level - 1) * 50
            )  # The XP requirement for the next level increases with each level

        return level, xp_needed
