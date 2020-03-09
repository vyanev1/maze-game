#  Author: CS1527 Course Team
#  Date: 9 January 2020
#  Version: 1.0

from getch1 import *
import sys


class Hero:
    """this is the hero class, further define it please"""
    def __init__(self, game, x, y):
        """set the coordinate of the hero in the maze"""
        self._coordX = x
        self._coordY = y
        self.health = 100
        self.coins = 1000  # gold coins the hero has.
        self.game = game

    def move(self, environment):
        """move in the maze, it is noted this function may not work in the debug mode"""
        ch2 = getch()

        temp_x = self._coordX
        temp_y = self._coordY

        if ch2 == b'\xe0':
            return ch2

        elif ch2 == b'H' or ch2 == b"w":
            # the up arrow key was pressed
            print("\nup key pressed\n")
            self._coordY -= 1

        elif ch2 == b'P' or ch2 == b"s":
            # the down arrow key was pressed
            print("\ndown key pressed\n")
            self._coordY += 1

        elif ch2 == b'K' or ch2 == b"a":
            # the left arrow key was pressed
            print("\nleft key pressed\n")
            self._coordX -= 1

        elif ch2 == b'M' or ch2 == b"d":
            # the right arrow key was pressed
            print("\nright key pressed\n")
            self._coordX += 1

        elif ch2 in (b"M", b"m"):
            environment.print_environment()
            return self.move(environment)

        elif ch2 in (b"H", b"h"):
            print("W / up arrow key: move up\n" +
                  "S / down arrow key: move down\n" +
                  "A / left arrow key: move left\n" +
                  "D / right arrow key: move left\n" +
                  "M: open map\n" +
                  "H: show all available commands\n")
            return self.move(environment)

        # print(f"Old coordinates: ({temp_x},{temp_y})\nNew coordinates:({self._coordX},{self._coordY})")

        # if the move you are about to do is not to a wall
        if environment.get_coord(self._coordX, self._coordY) != 1:

            # perform a normal move
            if environment.get_coord(self._coordX, self._coordY) == 0:
                environment.set_coord(self._coordX, self._coordY, 2)
            # if you declare an empty move (just click enter) don't change anything
            elif environment.get_coord(self._coordX, self._coordY) == 2:
                return ch2
            # if the hero steps at a goblin's position activate the goblin's abilities
            elif environment.get_coord(self._coordX, self._coordY) == 3:
                environment.set_coord(self._coordX, self._coordY, 2)
                goblin = environment.objects[(self._coordX, self._coordY)]
                goblin.visited = True
                goblin.activate_ability(self.game)
            # if the hero steps at a monster's position activate the monster's abilities
            elif environment.get_coord(self._coordX, self._coordY) == 4:
                monster = environment.objects[(self._coordX, self._coordY)]
                monster.visited = True
                monster.activate_ability(self.game)
                # retain the monster on the map

            # if the character previously stepped on a monster retain the monster on the map
            if environment.get_coord(temp_x, temp_y) == 4:
                pass
            else:
                environment.set_coord(temp_x, temp_y, 0)

        # stop the hero from moving into a wall
        else:
            self._coordX = temp_x
            self._coordY = temp_y
            print("You cannot move through a wall.")
            return self.move(environment)

        return ch2

    def move_debug(self, environment):

        """move in the maze, you need to press the enter key after keying in
        direction, and this works in the debug mode"""

        ch2 = sys.stdin.read(2).strip()

        temp_x = self._coordX
        temp_y = self._coordY

        if ch2 == "w":
            # the up arrow key was pressed
            print("up key pressed")
            self._coordY -= 1

        elif ch2 == "s":
            # the down arrow key was pressed
            print("down key pressed")
            self._coordY += 1

        elif ch2 == "a":
            # the left arrow key was pressed
            print("left key pressed")
            self._coordX -= 1

        elif ch2 == "d":
            # the right arrow key was pressed
            print("right key pressed")
            self._coordX += 1

        print(f"Old coordinates: ({temp_x},{temp_y})\nNew coordinates:({self._coordX},{self._coordY})")

        # if the move you are about to do is not to a wall
        if environment.get_coord(self._coordX, self._coordY) != 1:

            # perform a normal move
            if environment.get_coord(self._coordX, self._coordY) == 0:
                environment.set_coord(self._coordX, self._coordY, 2)
            # if you declare an empty move (just click enter) don't change anything
            elif environment.get_coord(self._coordX, self._coordY) == 2:
                return ch2
            # if the hero steps at a goblin's position activate the goblin's abilities
            elif environment.get_coord(self._coordX, self._coordY) == 3:
                environment.set_coord(self._coordX, self._coordY, 2)
                goblin = environment.objects[(self._coordX, self._coordY)]
                goblin.activate_ability(self.game)
            # if the hero steps at a monster's position activate the monster's abilities
            elif environment.get_coord(self._coordX, self._coordY) == 4:
                monster = environment.objects[(self._coordX, self._coordY)]
                monster.activate_ability(self.game)
                # retain the monster on the map

            # if the character previously stepped on a monster retain the monster on the map
            if environment.get_coord(temp_x, temp_y) == 4:
                pass
            else:
                environment.set_coord(temp_x, temp_y, 0)

        # stop the hero from moving into a wall
        else:
            self._coordX = temp_x
            self._coordY = temp_y
            print("You cannot move through a wall.")
            return self.move(environment)

        return ch2

    def set_coord(self, x, y):
        self._coordX = x
        self._coordY = y
