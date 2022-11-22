from enum import Enum
from typing import List, Tuple
import copy
import random
import numpy as np


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
    def __init__(self, tiles: List[List[int]], score: int = 0):
        self.tiles = np.array(tiles, dtype=np.int32)
        self.score = score

    def game_over(self) -> bool:
        """
        Return true when no additional tiles can be added to the board.
        """
        for row in self.tiles:
            for tile in row:
                if tile == 0:
                    return False
        return True

    def get_empty_positions(self) -> List[Tuple[int, int]]:
        """
        Return a list of (x, y) positions that are empty.
        """
        empty_positions = []
        for x in range(4):
            for y in range(4):
                if self.tiles[x][y] == 0:
                    empty_positions.append((x, y))
        return empty_positions

    def add_tile(self):
        """
        Randomly add a tile to the board. 90% chance of a 2, 10% chance of a 4.
        The tile is places randomly in a position that is currently empty.
        """
        empty_positions = self.get_empty_positions()
        if len(empty_positions) == 0:
            throw("No empt<tf_agents.networks.q_network.QNetwork object at 0x7feb69ee40d0>: Inconsistent dtypes or shapes between `inputs` and `input_tensor_spec`y positions")

        x, y = random.choice(empty_positions)
        self.tiles[x][y] = 2 if random.random() < 0.9 else 4

    def move(self, direction: Direction):
        """
        Make a move in the given direction, returning a new GameModel.
        After the move takes place, a new tile is added to the board.
        """
        new_model = GameModel(copy.deepcopy(self.tiles))
        new_model.score = self.score

        if direction == Direction.UP:
            new_model.move_up()
        elif direction == Direction.DOWN:
            new_model.move_down()
        elif direction == Direction.LEFT:
            new_model.move_left()
        elif direction == Direction.RIGHT:
            new_model.move_right()

        new_model.add_tile()
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
                    self.score += self.tiles[x - 1][y]


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
                    self.score += self.tiles[x + 1][y]

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
                    self.score += self.tiles[x][y - 1]

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
                    self.score += self.tiles[x][y + 1]

    def __repr__(self):
        return str(self.tiles)
