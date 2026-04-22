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

    def choose_ai_card(self, ai, player, difficulty="casual"):

        if difficulty == "casual":
            return random.choice(ai.hand)

        if difficulty == "bronze":

            if ai.health <= 30:
                support_cards = [c for c in ai.hand if c.category == "Support"]
                if support_cards:
                    return max(support_cards, key=lambda c: c.value)

            if ai.shield <= 10 and ai.health < 70:
                defence_cards = [c for c in ai.hand if c.category == "Defence"]
                if defence_cards:
                    return max(defence_cards, key=lambda c: c.value)

            offence_cards = [c for c in ai.hand if c.category == "Offence"]
            if offence_cards:
                return max(offence_cards, key=lambda c: c.value)

            return random.choice(ai.hand)

        if difficulty == "silver":

            offence_cards = [c for c in ai.hand if c.category == "Offence"]

            if offence_cards:
                sorted_cards = sorted(offence_cards, key=lambda c: c.value)
                return random.choice(sorted_cards[-2:])

            return random.choice(ai.hand)

        if difficulty == "gold":

            best_card = None
            best_score = -999

            for card in ai.hand:
                score = 0

                if card.category == "Offence":
                    score += card.value * 2

                    if player.health - card.value <= 0:
                        score += 100

                elif card.category == "Support":
                    if ai.health < 50:
                        score += 100 - ai.health
                    else:
                        score -= 20

                elif card.category == "Defence":
                    if ai.shield < 20:
                        score += 50 - ai.shield
                    else:
                        score -= 10

                if score > best_score:
                    best_score = score
                    best_card = card

            return best_card

        return random.choice(ai.hand)

    def check_game_over(self):
        if self.player.health <= 0:
            return "loss"
        elif self.opponent.health <= 0:
            return "win"
        return None

    def calculate_level(xp: int) -> tuple[int, int]:
        level = 1
        xp_needed = 100

        while xp >= xp_needed:
            xp -= xp_needed
            level += 1
            xp_needed = 100 + (level - 1) * 50

        return level, xp_needed
