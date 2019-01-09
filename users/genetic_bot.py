from random import random
from users.utils import User, Move
from game_objects import Stack


class DNA:
    def __init__(self, params):
        if len(params) > 0:
            self.merges_weight = params['merges_weight']
            self.height_largest_weight = params['height_largest_weight']
            self.height_lowest_weight = params['height_lowest_weight']
            self.height_average_weight = params['height_average_weight']
            self.num_discontinuities_weight = params['num_discontinuities_weight']
            self.num_discards_weight = params['num_discards_weight']
            self.fill_ratio_weight = params['fill_ratio_weight']
        else:
            self.random_init()

    def random_init(self):
        self.merges_weight = random() * 2 - 1
        self.height_largest_weight = random() * 2 - 1
        self.height_lowest_weight = random() * 2 - 1
        self.height_average_weight = random() * 2 - 1
        self.num_discontinuities_weight = random() * 2 - 1
        self.num_discards_weight = random() * 2 - 1
        self.fill_ratio_weight = random() * 2 - 1

    def evaluate(self, move):
        score = 0
        score += move.num_merges * self.merges_weight
        score += move.largest_height * self.height_largest_weight
        score += move.lowest_height * self.height_lowest_weight
        score += move.average_height * self.height_average_weight
        score += move.num_discontinuities * self.num_discontinuities_weight
        score += move.num_discards * self.num_discards_weight
        return score

    def __str__(self):
        return str(self.__dict__)


class GeneticBot(User):
    def __init__(self, config, game, dna_init={}):
        super(GeneticBot, self).__init__(config, game)
        self.dna = DNA(dna_init)
        self.fitness = 0

    def get_possible_moves(self):
        possible_moves = []
        next_tile = self.game.tile_queue.peak(0)
        for stack in self.game.stacks:
            if not stack.is_full() or stack.tiles[-1].value == next_tile.value:
                possible_moves.append(self.create_move(stack))
        if not self.game.discard_pile.is_full():
            possible_moves.append(self.create_move(self.game.discard_pile))
        for move in possible_moves:
            move.evaluation = self.dna.evaluate(move)
        return possible_moves

    def get_move(self, events):
        moves = self.get_possible_moves()
        moves = sorted(moves, key=lambda move: move.evaluation)
        if len(moves) == 0:
            return None
        return moves[-1]

    def evaluate_fitness(self):
        self.run()
        self.fitness = self.game.score_display.score
