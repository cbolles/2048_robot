import abc
from random import randint
from configparser import ConfigParser


class Pile(abc.ABC):
    @abc.abstractclassmethod
    def is_full(self):
        pass

    @abc.abstractclassmethod
    def add_tile(self, tile_value):
        pass


class Stack(Pile):
    def __init__(self, max_size, pile_id):
        self.tile_values = []
        self.max_size = max_size
        self.pile_id = pile_id

    def merge(self, multiplier):
        if len(self.tile_values) < 2 or not self.tile_values[-1] == self.tile_values[-2]:
            return 0
        result = self.tile_values.pop() + self.tile_values.pop()
        self.tile_values.append(result)
        return result * multiplier + self.merge(multiplier + 1)

    def add_tile(self, tile_value):
        self.tile_values.append(tile_value)
        return self.merge(1)

    def is_full(self):
        return len(self.tile_values) == self.max_size

    def get_worth(self):
        return sum(self.tile_values)

    def __len__(self):
        return len(self.tile_values)

    def __lt__(self, other):
        return self.get_worth() < other.get_worth()

    def __gt__(self, other):
        return self.get_worth() > other.get_worth()

    def __eq__(self, other):
        return self.pile_id == other.pile_id

    def __str__(self):
        return 'Stack with tiles: ' + str(self.tile_values)


class DiscardPile(Pile):
    def __init__(self, pile_id, max_discards=2):
        self.max_discards = max_discards
        self.pile_id = pile_id
        self.num_discards = 0

    def add_tile(self, tile_value):
        self.num_discards += 1

    def is_full(self):
        return self.num_discards == self.max_discards

    def clear_discards(self):
        self.num_discards = 0

    def __str__(self):
        return 'DiscardPile: ' + str(self.num_discards) + 'used out of ' + str(self.max_discards)


class TileQueue:
    def __init__(self):
        self.tile_values = [self.generate_tile_value(), self.generate_tile_value()]

    def generate_tile_value(self):
        prob = randint(1, 6)
        return pow(2, prob)

    def pull(self):
        tile_value = self.tile_values.pop(0)
        self.tile_values.append(self.generate_tile_value())
        return tile_value

    def peak(self, index):
        return self.tile_values[index]

    def __str__(self):
        return 'Tile Queue: ' + str(self.tile_values)


class GameModel:
    def __init__(self, game_config_path):
        config = ConfigParser()
        config.read(game_config_path)
        self.init_stacks(config)
        self.discard_pile = DiscardPile(len(self.stacks))
        self.tile_queue = TileQueue()
        self.score = 0

    def init_stacks(self, config):
        num_stacks = int(config['model']['num_stacks'])
        max_stack_size = int(config['model']['max_stack_size'])
        self.stacks = [Stack(max_stack_size, i) for i in range(0, num_stacks)]

    def get_pile(self, pile_id):
        for stack in self.stacks:
            if pile_id == stack.pile_id:
                return stack
        return self.discard_pile

    def make_move(self, pile):
        next_tile_value = self.tile_queue.pull()
        if isinstance(pile, DiscardPile):
            pile.add_tile(next_tile_value)
        else:
            self.score += pile.add_tile(next_tile_value)
            if len(pile) == 0:
                self.discard_pile.clear_discards()

    def game_over(self):
        for stack in self.stacks:
            if not stack.is_full():
                return False
        return self.discard_pile.is_full()

    def __str__(self):
        return 'Game: ' + str(self.score)
