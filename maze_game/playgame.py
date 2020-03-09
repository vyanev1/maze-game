from hero import Hero
from goblin import Goblin
from monster import Monster
from maze_gen_recursive import make_maze_recursion
from copy import deepcopy
import random

WALL_CHAR = "#"
SPACE_CHAR = "-"
HERO_CHAR = "H"
GOBLIN_CHAR = "G"
MONSTER_CHAR = "M"


class _Environment:
    """Environment includes Maze+Monster+Goblin"""
    objects = {}

    def __init__(self, maze):
        self._environment = deepcopy(maze)

    def set_coord(self, x, y, val):
        self._environment[y][x] = val

    def get_coord(self, x, y):
        return self._environment[y][x]

    def print_environment(self):
        """print out the environment in the terminal"""
        for row in self._environment:
            row_str = str(row)
            row_str = row_str.replace("1", WALL_CHAR)  # replace the wall character
            row_str = row_str.replace("0", SPACE_CHAR)  # replace the space character
            row_str = row_str.replace("2", HERO_CHAR)  # replace the hero character
            row_str = row_str.replace("3", GOBLIN_CHAR)  # replace the goblin character
            row_str = row_str.replace("4", MONSTER_CHAR)  # replace the monster character

            print("".join(row_str))

    def all_types_exist(self, t):
        for subclass in t.__subclasses__():
            boolean = False
            for object in self.objects.values():
                if subclass == type(object):
                    boolean = True
            if not boolean:
                return False
        return True

    def type_exists(self, t):
        for key in self.objects:
            element = self.objects[key]
            if type(element) == t:
                return True
        return False

    def all_monsters_visited(self):
        for key in self.objects:
            object = self.objects[key]
            if type(object) in Monster.__subclasses__() and not object.visited:
                return False
        return True


class Game:

    _count = 0

    def __init__(self, diff):
        self.difficulty = diff
        self.maze = make_maze_recursion(17, 17)
        self.MyEnvironment = _Environment(self.maze)  # initial environment is the maze itself
        self._count = 0
        self.myHero = self.generate_hero()
        self.generate_goblins()
        self.generate_monsters()

    def generate_goblins(self):
        count = 0
        while count < 5:
            x = random.randrange(1, 17)
            y = random.randrange(1, 17)

            if self.MyEnvironment.get_coord(x, y) not in [1, 2, 3, 4]:
                # generate a random goblin object at those coordinates
                goblin = Goblin.random_goblin(self, x, y)
                if not(self.MyEnvironment.type_exists(type(goblin))) or self.MyEnvironment.all_types_exist(Goblin):
                    self.MyEnvironment.set_coord(x, y, 3)
                    self.MyEnvironment.objects[(x, y)] = goblin
                    count += 1
                    print(f"{goblin} at coordinates ({x},{y})")

    def generate_monsters(self):
        count = 0
        while count < 5:
            x = random.randrange(1, 17)
            y = random.randrange(1, 17)

            if self.MyEnvironment.get_coord(x, y) not in [1, 2, 3, 4]:
                # generate a random monster object at those coordinates
                monster = Monster.random_monster(self, x, y)
                if not(self.MyEnvironment.type_exists(type(monster))) or self.MyEnvironment.all_types_exist(Monster):
                    self.MyEnvironment.set_coord(x, y, 4)
                    self.MyEnvironment.objects[(x, y)] = monster
                    count += 1
                    print(f"{monster} at coordinates ({x},{y})")

    def generate_hero(self):
        count = 0
        while count < 1:
            x = random.randrange(1, 17)
            y = random.randrange(1, 17)

            if self.MyEnvironment.get_coord(x, y) not in [1, 2, 3, 4]:
                count += 1
                hero = Hero(self, x, y)
                self.MyEnvironment.set_coord(x, y, 2)
                print(f"Hero at coordinates ({x},{y})")
                return hero

    def play(self):
        self.MyEnvironment.print_environment()

        while True:
            ch2 = self.myHero.move(self.MyEnvironment)
            if ch2 != b'\xe0':
                self.myHero.health -= 1
                self.MyEnvironment.print_environment()
                self._count += 1
                print(f"Hero stats:\n- health: {self.myHero.health}\n- coins: {self.myHero.coins}")
                print("============================", self._count)

                if self.myHero.health <= 0:
                    print("Your hero died! Try again!")
                    break
                elif self.MyEnvironment.all_monsters_visited():
                    print("You won the game! Congratulations!")
                    self.update_leaderboard()
                    break

        self.print_leaderboard()
        input("Type enter to exit.")

    def play_debug(self):
        self.MyEnvironment.print_environment()

        while True:
            self.myHero.move_debug(self.MyEnvironment)
            self.myHero.health -= 1
            self.MyEnvironment.print_environment()
            self._count += 1
            print(f"Hero stats:\n- health: {self.myHero.health}\n- coins: {self.myHero.coins}")
            print("============================", self._count)

            if self.myHero.health <= 0:
                print("Your hero died! Try again!")
                break
            elif self.MyEnvironment.all_monsters_visited():
                print("You won the game! Congratulations!")
                self.update_leaderboard()
                break
        self.print_leaderboard()
        input("Type enter to exit.")

    def print_leaderboard(self):
        f = open("leaderboard.txt", "r")
        # transform the string in the file into a list of lists of words
        leaderboard = [line.split() for line in f.read().splitlines()]
        # transform the number of moves string into an integer so that we can sort by it
        for line in leaderboard:
            line[0] = int(line[0])
            line[1] = int(line[1])
        leaderboard = sorted(leaderboard, key=lambda x: x[0])

        print("\n==============================" +
              "\n======== LEADERBOARD =========" +
              "\n==============================")
        count = 0
        for line in leaderboard:
            if count >= 10:
                break
            elif line[1] == self.difficulty:
                print(f"{line[2]}: {line[0]} moves")
                count += 1
        f.close()

    @staticmethod
    def update_leaderboard():
        name = input("Type in your name:")
        f = open("leaderboard.txt", "a")
        f.write(f"{self._count} {self.difficulty} {name}\n")
        f.close()

if __name__ == "__main__":
    try:
        difficulty = int(input('''Type the number for your difficulty level
        1: Easy
        2: Medium
        3: Hard
        4: Very Hard\n'''))
    except ValueError:
        print("Please enter a valid number.")
        difficulty = int(input())

    myGame = Game(difficulty)
    myGame.play()