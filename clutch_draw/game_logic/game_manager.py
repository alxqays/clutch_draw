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

    def draw_card(self, category):
        valid_cards = [
            c for c in self.deck if c.category == category
        ]  # only draw cards of the same category as the card that was played.
        chosen = random.choice(
            valid_cards
        )  # randomly selects a card from the valid cards.
        self.deck.remove(
            chosen
        )  # removes the card from the deck so that no duplicates exist.
        return chosen  # returns the drawn card to be added to the player's hand.

    def take_turn(self, player, opponent, card):
        self.play_card(
            player, opponent, card
        )  # plays the selected card and applies its effects.

        player.hand.remove(card)  # removes the played card from the player's hand.
        self.deck.append(card)  # returns the played card to the deck.

        new_card = self.draw_card(
            card.category
        )  # draws a new card of the same category to replace the one that was played.
        player.hand.append(new_card)  # adds the drawn card to the player's hand.

        self.turn = (
            "ai" if self.turn == "player" else "player"
        )  # switches the turn to the other player.

        return new_card  # reveals the new card that was drawn to the player.

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
