class Ability:

    def __init__(self, name: str, damage: int, mana_cost: int) -> None:
        self.name = name
        self.damage = damage
        self.mana_cost = mana_cost

    def play_sound(self) -> None:
        if self.name == "Fireball":
            print("Playing fireball sound effect")
        elif self.name == "Heal":
            print("Playing healing sound effect")


class Fireball(Ability):
    def play_sound(self) -> None:
        sound = load_sound("fireball.wav")
        sound.play()


class Heal(Ability):
    def play_sound(self) -> None:
        sound = load_sound("angelic.wav")
        sound.play()


class ShieldBlock(Ability):
    pass


class Character:

    def __init__(self, name: str, starting_hp: int, ability: Ability) -> None:
        self.name = name
        self.current_hp = starting_hp
        self.max_hp = starting_hp
        self.ability = ability

    def use_ability(self, target: "Character") -> None:
        print(f"{self.name} uses {self.ability.name} on {target.name}!")
        target.take_damage(self.ability.damage)
        self.ability.play_sound()

    def heal(self, amount: int) -> None:
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def take_damage(self, damage: int) -> None:
        """
        Reduces the character's HP by the specified damage amount.

        :param self: Description
        :param damage: Description
        :type damage: int
        """
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0

        if self.current_hp == 0:
            self.die()

    def die(self) -> None:
        print(f"{self.name} has died.")


warrior = Character("Warrior", 150, ShieldBlock("Shield Block", 0, 0))
mage = Character("Mage", 100, Fireball("Fireball", 40, 20))
rogue = Character("Rogue", 120, Heal("Heal", -30, 15))
healer = Character("Healer", 110, Heal("Heal", -50, 25))

mage.use_ability(warrior)
warrior.use_ability(rogue)

warrior.take_damage(30)
mage.heal(20)
rogue.take_damage(50)
