from random import random
from users.base_user import User
from copy import deepcopy
from game.game_model import Stack


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


class Move:
    def __init__(self, game_model, pile):
        self.initialize_values()
        self.game_model = deepcopy(game_model)
        self.original_pile = pile
        self.pile = self.game_model.get_pile(pile.pile_id)
        self.stack_move = isinstance(self.pile, Stack)
        original_height = 0
        if self.stack_move:
            original_height = len(pile)
        self.game_model.make_move(self.pile)
        if self.stack_move:
            self.set_num_merges(original_height)
        else:
            self.num_merges = 0
        self.set_num_discontinuities()
        self.set_num_tiles()
        self.set_score_change(game_model)
        self.set_largest_height()
        self.set_lowest_height()
        self.set_average_height()
        self.set_num_discards()
        self.set_fill_ratio()

    def initialize_values(self):
        self.num_merges = 0
        self.num_discontinuities = 0
        self.num_tiles = 0
        self.score_change = 0
        self.largest_height = 0
        self.lowest_height = 0
        self.average_height = 0
        self.num_discards = 0
        self.fill_ratio = 0
        self.evaluation = 0

    def set_num_merges(self, original_height):
        new_height = len(self.pile)
        if original_height != 0 and new_height == 0:
            self.num_merges = original_height
        else:
            self.num_merges = original_height + 1 - new_height

    def set_num_discontinuities(self):
        for stack in self.game_model.stacks:
            for i in range(0, len(stack) - 1):
                if stack.tile_values[i] < stack.tile_values[i + 1]:
                    self.num_discontinuities += 1

    def set_num_tiles(self):
        for stack in self.game_model.stacks:
            self.num_tiles += len(stack)

    def set_score_change(self, original_game_model):
        new_score = self.game_model.score
        old_score = original_game_model.score
        self.score_change = new_score - old_score

    def set_largest_height(self):
        largest_height = 0
        for stack in self.game_model.stacks:
            if len(stack) > largest_height:
                largest_height = len(stack)
        self.largest_height = largest_height

    def set_lowest_height(self):
        lowest_height = self.game_model.stacks[1].max_size
        for stack in self.game_model.stacks:
            if len(stack) < lowest_height:
                lowest_height = len(stack)
        self.lowest_height = lowest_height

    def set_average_height(self):
        total_height = 0
        for stack in self.game_model.stacks:
            total_height += len(stack)
        self.average_height = total_height / (len(self.game_model.stacks) - 1)

    def set_num_discards(self):
        self.num_discards = self.game_model.discard_pile.num_discards

    def set_fill_ratio(self):
        max_tiles = len(self.game_model.stacks) * self.game_model.stacks[0].max_size + self.game_model.discard_pile.max_discards
        self.fill_ratio = self.num_tiles / max_tiles


class GeneticBot(User):
    def __init__(self, config_path, params):
        dna_init = dict()
        if 'dna_init' in params:
            dna_init = params['dna_init']
        class_name = type(self).__name__
        super(GeneticBot, self).__init__(config_path, params, class_name)
        self.dna = DNA(dna_init)
        self.fitness = 0
        self.game_model = self.game_controller.game_model

    def create_move(self, pile):
        if pile is None:
            return None
        return Move(self.game_model, pile)

    def get_possible_moves(self):
        possible_moves = []
        next_tile_value = self.game_model.tile_queue.peak(0)
        for stack in self.game_model.stacks:
            if not stack.is_full() or stack.tile_values[-1] == next_tile_value:
                possible_moves.append(self.create_move(stack))
        if not self.game_model.discard_pile.is_full():
            possible_moves.append(self.create_move(self.game_model.discard_pile))
        for move in possible_moves:
            move.evaluation = self.dna.evaluate(move)
        return possible_moves

    def get_target_pile(self, events):
        moves = self.get_possible_moves()
        moves = sorted(moves, key=lambda move: move.evaluation)
        if len(moves) == 0:
            return None
        return moves[-1].original_pile

    def is_running(self):
        return not self.game_model.game_over()

    def evaluate_fitness(self):
        self.run()
        self.fitness = self.game_model.score
