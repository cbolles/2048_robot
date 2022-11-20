from enum import Enum
from typing import List
import copy


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class GameModel:
    """
    Representation of the game at a given step. Handles storing the state of
    the game and also provides the functionality for updating the state
    """
    def __init__(self, tiles: List[List[int]]):
        self.tiles = tiles

    def game_over(self) -> bool:
        """
        Return true when no additional tiles can be added to the board.
        """
        for row in self.tiles:
            for tile in row:
                if tile == 0:
                    return False
        return True

    def move(self, direction: Direction) -> GameModel:
        """
        Make a move in the given direction, returning a new GameModel
        """
        new_model = GameModel(copy.deepcopy(self.tiles))
        if direction == Direction.UP:
            new_model.move_up()
        elif direction == Direction.DOWN:
            new_model.move_down()
        elif direction == Direction.LEFT:
            new_model.move_left()
        elif direction == Direction.RIGHT:
            new_model.move_right()
        return new_model

    def move_up(self):
        """
        Move the tiles up, combining tiles as necessary.
        """
        for x in range(4):
            for y in range(4):
                if self.tiles[x][y] == 0:
                    continue

                # Move the tile up as far as possible
                while x > 0 and self.tiles[x - 1][y] == 0:
                    self.tiles[x - 1][y] = self.tiles[x][y]
                    self.tiles[x][y] = 0
                    x -= 1

                # Combine the tile with the one above it
                if x > 0 and self.tiles[x - 1][y] == self.tiles[x][y]:
                    self.tiles[x - 1][y] *= 2
                    self.tiles[x][y] = 0

    def move_down(self):
        """
        Move the tiles down, combining tiles as necessary.
        """
        for x in range(3, -1, -1):
            for y in range(4):
                if self.tiles[x][y] == 0:
                    continue

                # Move the tile down as far as possible
                while x < 3 and self.tiles[x + 1][y] == 0:
                    self.tiles[x + 1][y] = self.tiles[x][y]
                    self.tiles[x][y] = 0
                    x += 1

                # Combine the tile with the one below it
                if x < 3 and self.tiles[x + 1][y] == self.tiles[x][y]:
                    self.tiles[x + 1][y] *= 2
                    self.tiles[x][y] = 0

    def move_left(self):
        """
        Move the tiles left, combining tiles as necessary.
        """
        for x in range(4):
            for y in range(4):
                if self.tiles[x][y] == 0:
                    continue

                # Move the tile left as far as possible
                while y > 0 and self.tiles[x][y - 1] == 0:
                    self.tiles[x][y - 1] = self.tiles[x][y]
                    self.tiles[x][y] = 0
                    y -= 1

                # Combine the tile with the one to the left
                if y > 0 and self.tiles[x][y - 1] == self.tiles[x][y]:
                    self.tiles[x][y - 1] *= 2
                    self.tiles[x][y] = 0

    def move_right(self):
        """
        Move the tiles right, combining tiles as necessary.
        """
        for x in range(4):
            for y in range(3, -1, -1):
                if self.tiles[x][y] == 0:
                    continue

                # Move the tile right as far as possible
                while y < 3 and self.tiles[x][y + 1] == 0:
                    self.tiles[x][y + 1] = self.tiles[x][y]
                    self.tiles[x][y] = 0
                    y += 1

                # Combine the tile with the one to the right
                if y < 3 and self.tiles[x][y + 1] == self.tiles[x][y]:
                    self.tiles[x][y + 1] *= 2
                    self.tiles[x][y] = 0
