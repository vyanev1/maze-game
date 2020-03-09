#  Author: CS1527 Course Team
#  Date: 9 January 2020
#  Version: 1.0
import random
from getch1 import *
from time import sleep


class Goblin:
    def __init__(self, type, x, y):
        self.type = type
        self._coordX = x
        self._coordY = y
        self.visited = False

    @staticmethod
    def random_goblin(game, x, y):
        # generate randomly the type of goblin and return the appropriate class instance
        type = random.choice(["Wealth", "Health", "Gamer"])

        if type == "Wealth":
            return WealthGoblin(game, type, x, y)
        elif type == "Health":
            return HealthGoblin(game, type, x, y)
        elif type == "Gamer":
            return GamerGoblin(game, type, x, y)

    def __str__(self):
        return self.type + " goblin"


class WealthGoblin(Goblin):
    def __init__(self, game, type, x, y):
        super().__init__(type, x, y)
        # give the hero random number of coins for a chance of random %
        # ability = (coins,chance)
        # adjust the goblin's ability depending on the difficulty level
        difficulty = game.difficulty
        self.ability = (random.randrange(50, 201)/difficulty, random.randrange(40, 101)/difficulty)

    def activate_ability(self, game):
        coinsWon = self.give_coins()
        game.myHero.coins += coinsWon

        sleep(1)
        print(f"You just approached a {self}" +
              f" at coordinates ({self._coordX},{self._coordY}) with an ability of {self.ability}!\n" +
              f"The hero has a {self.ability[1]} chance to win {self.ability[0]} coins.")
        sleep(1)
        print(f"Your hero won {coinsWon} coins.")
        sleep(1)
        print(f"You now have {game.myHero.coins} coins.")
        sleep(2)

    def give_coins(self):
        # generate a random number between 1 and 100 and check if it's in the ability's percentage region
        number = random.randrange(1, 101)
        if number <= self.ability[1]:
            # return the coin amount if the number is lucky
            return self.ability[0]
        else:
            # else give nothing
            return 0


class HealthGoblin(Goblin):
    def __init__(self, game, type, x, y):
        super().__init__(type, x, y)
        # recover random amount of health for a chance of a random %
        # ability = (health,chance)
        # adjust the goblin's ability depending on the difficulty level
        self.ability = (random.randrange(0, 101)/game.difficulty, random.randrange(40, 101)/game.difficulty)

    def activate_ability(self, game):
        healthRestored = self.restore_health()
        game.myHero.health += healthRestored
        if game.myHero.health > 100:
            game.myHero.health = 100

        sleep(1)
        print(f"You just approached a {self}" +
              f" at coordinates ({self._coordX},{self._coordY}) with an ability of {self.ability}!\n" +
              f"The hero has a {self.ability[1]} chance to regain {self.ability[0]} health.")
        sleep(1)
        print(f"Your hero gained {healthRestored} health.")
        sleep(1)
        print(f"You now have {game.myHero.health} health.")
        sleep(2)

    def restore_health(self):
        # generate a random number between 1 and 100 and check if it's in the ability's percentage region
        number = random.randrange(1, 101)
        if number <= self.ability[1]:
            # restore hero health if the number is lucky
            return self.ability[0]
        else:
            # else restore 0 health
            return 0


class GamerGoblin(Goblin):
    def __init__(self, game, type, x, y):
        super().__init__(type, x, y)
        # play rock-paper-scissors
        # if the hero wins the game, they will be given a specified number of coins and health points

        # adjust the goblin's ability depending on the difficulty level
        # ability = (coins,health)
        self.ability = (random.randrange(50, 201)/game.difficulty, random.randrange(0, 101)/game.difficulty)

    def activate_ability(self, game):
        sleep(1)
        print(f"You just approached a {self}" +
              f" at coordinates ({self._coordX},{self._coordY}) with an ability of {self.ability}!\n" +
              f"A game will be played and if the hero wins the game," +
              f" they will get {self.ability[0]} coins and {self.ability[1]} health.")
        sleep(1)
        coinsWon, healthRestored = self.give_coins_health()
        game.myHero.coins += coinsWon
        game.myHero.health += healthRestored

        sleep(1)
        print(f"Your hero gained {healthRestored} health and {coinsWon} coins.")
        sleep(1)
        print(f"You now have {game.myHero.health} health and {game.myHero.coins} coins.")
        sleep(2)

    def give_coins_health(self):
        # play rock-paper-scissors
        # if the hero wins give him coins and health
        # if the goblin wins give the hero nothing

        result = rock_paper_scissors()
        if result:
            return self.ability[0], self.ability[1]
        else:
            return 0, 0


def rock_paper_scissors():
    # return True if the hero wins, otherwise return False
    print("You need to play rock-paper-scissors. Please declare your move.")
    print("Press 'R' for rock, 'P' for paper, and 'S' for scissors.")
    round = 1
    roundsWon = 0
    roundsLost = 0

    while roundsLost < 2 and roundsWon < 2:
        print(f"Round {round}!")
        ch2 = getch()
        while ch2 == b'\xe0':
            ch2 = getch()
        if ch2 in (b'r', b'R'):
            heroMove = "rock"
        elif ch2 in (b'p', b'P'):
            heroMove = "paper"
        elif ch2 in (b's', b'S'):
            heroMove = "scissors"
        else:
            print("Please press a valid button.")
            continue

        monsterMove = random.choice(["rock", "paper", "scissors"])
        print(f"Hero played {heroMove}.")
        print(f"Monster played {monsterMove}.")

        if heroMove == monsterMove:
            print(f"You both played {heroMove}, you need to declare a move again.")
        elif heroMove == "rock" and monsterMove == "scissors":
            roundsWon += 1
        elif heroMove == "paper" and monsterMove == "rock":
            roundsWon += 1
        elif heroMove == "scissors" and monsterMove == "paper":
            roundsWon += 1
        else:
            roundsLost += 1

        round += 1

    if roundsWon >= 2:
        print("You won!")
        return True
    else:
        print("You lost!")
        return False
