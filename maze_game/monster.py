#  Author: CS1527 Course Team
#  Date: 9 January 2020
#  Version: 1.0
import random
import math
from goblin import rock_paper_scissors
from time import sleep


class Monster:
    def __init__(self, type, x, y):
        self.type = type
        self._coordX = x
        self._coordY = y
        self.visited = False

    @staticmethod
    def random_monster(game, x, y):
        # generate randomly the type of goblin and return the appropriate class instance
        type = random.choice(["Thief", "Fighter", "Gamer"])

        if type == "Thief":
            return ThiefMonster(game, type, x, y)
        elif type == "Fighter":
            return FighterMonster(game, type, x, y)
        elif type == "Gamer":
            return GamerMonster(game, type, x, y)

    def __str__(self):
        return self.type + " monster"


class ThiefMonster(Monster):
    def __init__(self, game, type, x, y):
        super().__init__(type, x, y)
        # steal from the hero number of coins for a % chance
        # ability = (coins,chance)
        # adjust the monster's ability depending on the difficulty level
        self.ability = (random.randrange(50, 101)*math.sqrt(game.difficulty), random.randrange(20, 101)*math.sqrt(game.difficulty))

    def activate_ability(self, game):
        coinsLost = self.steal_coins()
        game.myHero.coins -= coinsLost

        sleep(1)
        print(f"You just approached a {self}" +
              f" at coordinates ({self._coordX},{self._coordY}) with an ability of {self.ability}!\n" +
              f"The hero has a {self.ability[1]} chance to lose {self.ability[0]} coins.")
        sleep(1)
        print(f"Your hero lost {coinsLost} coins.")
        sleep(1)
        print(f"You now have {game.myHero.coins} coins.")
        sleep(2)

    def steal_coins(self):
        # generate a random number between 1 and 100 and check if it's in the ability's percentage region
        number = random.randrange(1, 101)
        if number <= self.ability[1]:
            # steal the coin amount if the number is 'lucky'
            return self.ability[0]
        else:
            # else steal nothing
            return 0


class FighterMonster(Monster):
    def __init__(self, game, type, x, y):
        super().__init__(type, x, y)
        # drop amount of hero's health for a chance of a random %
        # ability = (health,chance)
        # adjust the monster's ability depending on the difficulty level
        self.ability = (random.randrange(10, 20)*math.sqrt(game.difficulty), random.randrange(20, 101)*math.sqrt(game.difficulty))

    def activate_ability(self, game):
        healthLost = self.fight()
        game.myHero.health -= healthLost
        if game.myHero.health <= 0:
            game.myHero.health = 0

        sleep(1)
        print(f"You just approached a {self}" +
              f" at coordinates ({self._coordX},{self._coordY}) with an ability of {self.ability}!\n" +
              f"The hero has a {self.ability[1]} chance to lose {self.ability[0]} health.")
        sleep(1)
        print(f"Your hero lost {healthLost} health.")
        sleep(1)
        print(f"You now have {game.myHero.health} health.")
        sleep(2)

    def fight(self):
        # generate a random number between 1 and 100 and check if it's in the ability's percentage region
        number = random.randrange(1, 101)
        if number <= self.ability[1]:
            # drop the hero's health if the number is 'lucky'
            return self.ability[0]
        else:
            # else drop 0 health
            return 0


class GamerMonster(Monster):
    def __init__(self, game, type, x, y):
        super().__init__(type, x, y)
        # play rock-paper-scissors
        # if the monster wins the game, the hero will lose specified number of coins and health points
        # adjust the monster's ability depending on the difficulty level
        # ability = (coins,health)
        self.ability = (random.randrange(50, 101)*math.sqrt(game.difficulty), random.randrange(10, 20)*math.sqrt(game.difficulty))

    def activate_ability(self, game):
        sleep(1)
        print(f"You just approached a {self}" +
              f" at coordinates ({self._coordX},{self._coordY}) with an ability of {self.ability}!\n" +
              f"A game will be played and if the monster wins the game," +
              f" the player will lose {self.ability[0]} coins and {self.ability[1]} health.")
        sleep(1)
        coinsLost, healthLost = self.lose_coins_health()
        game.myHero.coins -= coinsLost
        game.myHero.health -= healthLost
        if game.myHero.health <= 0:
            game.myHero.health = 0
        sleep(1)
        print(f"Your hero lost {healthLost} health and {coinsLost} coins.")
        sleep(1)
        print(f"You now have {game.myHero.health} health and {game.myHero.coins} coins.")
        sleep(2)

    def lose_coins_health(self):
        # play rock-paper-scissors
        # if the hero loses the game he loses coins and health
        # if the hero wins he loses nothing

        result = rock_paper_scissors()
        if not result:
            return self.ability[0], self.ability[1]
        else:
            return 0, 0