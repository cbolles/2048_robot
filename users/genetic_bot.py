from random import random
from users.utils import User
from copy import deepcopy


class DNA:
    def __init__(self, params):
        if len(params) > 0:
            self.merges_weight = params['merges_weight']
            self.height_largest_weight = params['height_largest_weight']
            self.height_lowest_weight = params['height_lowest_weight']
            self.height_average_weight = params['height_average_weight']
            self.num_discontinuities_weight = params['num_discontinuities_weight']
            self.num_discards_weight = params['num_discards_weight']
        else:
            self.random_init()

    def random_init(self):
        self.merges_weight = random()
        self.height_largest_weight = random()
        self.height_lowest_weight = random()
        self.height_average_weight = random()
        self.num_discontinuities_weight = random()
        self.num_discards_weight = random()

    def evaluate(self, move):
        score = 0
        score += move.num_merges * self.merges_weight
        score += move.height_largest * self.height_largest_weight
        score += move.height_lowest * self.height_lowest_weight
        score += move.height_average * self.height_average_weight
        score += move.num_discontinuities * self.num_discontinuities_weight
        score += move.num_discards * self.num_discards_weight
        return score

    def __str__(self):
        return str(self.__dict__)


class Move:
    def __init__(self):
        self.stack_number = 0
        self.num_merges = 0
        self.height_largest = 0
        self.height_lowest = 0
        self.height_average = 0
        self.num_discontinuities = 0
        self.num_discards = 0
        self.evaluation = 0

    def set_num_merges(self, game, stack_id, original_height):
        new_height = len(game.stacks[stack_id])
        if original_height != 0 and new_height == 0:
            self.num_merges = original_height
        else:
            self.num_merges = original_height + 1 - new_height

    def set_largest_height(self, game):
        self.height_largest = len(sorted(game.stacks, key=lambda stack: len(stack.tiles))[-1].tiles)

    def set_lowest_height(self, game):
        self.height_lowest = len(sorted(game.stacks, key=lambda stack: len(stack.tiles))[0].tiles)

    def set_average_height(self, game):
        all_heights = [len(stack.tiles) for stack in game.stacks]
        self.height_average = sum(all_heights) / len(all_heights)

    def set_num_discontinuities(self, game, stack_id):
        self.num_discontinuities = 0
        stack = game.stacks[stack_id]
        for i in range(0, len(stack.tiles) - 1):
            if stack.tiles[i].value < stack.tiles[i + 1].value:
                self.num_discontinuities += 1

    def set_num_discards(self, game):
        return game.discard_pile.num_discards

    def set_evaluation(self, dna):
        self.evaluation = dna.evaluate(self)

    def set_stats(self, game, stack_id, dna):
        temp_game = deepcopy(game)
        original_stack_height = 0
        if stack_id != len(game.stacks):
            original_stack_height = len(temp_game.stacks[stack_id])
        temp_game.make_move(stack_id)
        if stack_id != len(temp_game.stacks):
            self.set_num_merges(temp_game, stack_id, original_stack_height)
            self.set_num_discontinuities(temp_game, stack_id)
        self.stack_number = stack_id
        self.set_largest_height(temp_game)
        self.set_lowest_height(temp_game)
        self.set_average_height(temp_game)
        self.set_num_discards(temp_game)
        self.set_evaluation(dna)


class GeneticBot(User):
    def __init__(self, config, game, dna_init={}):
        super(GeneticBot, self).__init__(config, game)
        self.dna = DNA(dna_init)
        self.fitness = 0

    def get_move_stats(self, tile, stack_id):
        move = Move()
        move.set_stats(self.game, stack_id, self.dna)
        return move

    def get_possible_moves(self):
        possible_moves = []
        next_tile = self.game.tile_queue.peak(0)
        for i in range(0, len(self.game.stacks)):
            if not self.game.stacks[i].is_full() or self.game.stacks[i].tiles[-1].value == next_tile.value:
                possible_moves.append(self.get_move_stats(next_tile, i))
        if not self.game.discard_pile.pile_full():
            possible_moves.append(self.get_move_stats(next_tile, len(self.game.stacks)))
        return possible_moves

    def get_move(self, event):
        moves = self.get_possible_moves()
        return sorted(moves, key=lambda move: move.evaluation)[-1].stack_number

    def evaluate_fitness(self):
        self.run()
        self.fitness = self.game.score
