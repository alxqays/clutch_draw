import random


class GameManager:
    def __init__(self, player, opponent, deck):
        self.player = (
            player  # stores the player so that the health and hand can be accessed.
        )
        self.opponent = opponent  # stores the ai opponent.
        self.deck = deck  # stores the deck of cards.
        self.turn = "player"  # keep track of whose turn it is, can be "player" or "ai".

    def play_card(self, current, opponent, card):

        print("PLAYING CARD:", card.title)
        print("BEFORE -> Opponent Health:", opponent.health, "Shield:", opponent.shield)

        if card.category == "Offence":

            damage = card.value

            if opponent.shield > 0:
                if damage <= opponent.shield:
                    opponent.shield -= damage
                    damage = 0
                else:
                    damage -= opponent.shield
                    opponent.shield = 0

            opponent.health -= damage

            if opponent.health < 0:
                opponent.health = 0

            print("Damage Dealt:", card.value)

        elif card.category == "Defence":
            current.shield += (
                card.value
            )  # increases the current player's shield by the card's value.
            print("Shield Gained:", card.value)

        elif card.category == "Support":

            current.health += card.value

            if current.health > 100:
                current.health = 100

            print("Health Gained:", card.value)

            print(
                "AFTER -> Opponent Health:", opponent.health, "Shield:", opponent.shield
            )
            print("--------")

    def take_turn(self, player, opponent, card):
        self.play_card(
            player, opponent, card
        )  # plays the selected card and applies its effects.

        self.turn = (
            "ai" if self.turn == "player" else "player"
        )  # switches the turn to the other player.

    def ai_turn(self):
        card = random.choice(
            self.opponent.hand
        )  # ai randomly selects a card from its hand to play.
        return self.take_turn(
            self.opponent, self.player, card
        )  # ai takes its turn by playing the selected card and applying its effects, just like the player.

    def check_game_over(self):
        if self.player.health <= 0:
            return "loss"
        elif self.opponent.health <= 0:
            return "win"
        return None
