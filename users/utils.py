from abc import ABC, abstractmethod
import pygame
from configparser import ConfigParser
from copy import deepcopy
from game_objects import Stack


class Move:
    def __init__(self, game, pile):
        self.initialize_values()
        self.game = deepcopy(game)
        self.original_pile = pile
        self.pile = self.game.get_pile(pile.pile_id)
        self.stack_move = isinstance(self.pile, Stack)
        original_height = 0
        if self.stack_move:
            original_height = len(pile)
        self.game.make_move(self.pile)
        if self.stack_move:
            self.set_num_merges(original_height)
        else:
            self.num_merges = 0
        self.set_num_discontinuities()
        self.set_num_tiles()
        self.set_score_change(game)
        self.set_largest_height()
        self.set_lowest_height()
        self.set_average_height()
        self.set_num_discards()

    def initialize_values(self):
        self.num_merges = 0
        self.num_discontinuities = 0
        self.num_tiles = 0
        self.score_change = 0
        self.largest_height = 0
        self.lowest_height = 0
        self.average_height = 0
        self.num_discards = 0
        self.evaluation = 0

    def set_num_merges(self, original_height):
        new_height = len(self.pile)
        if original_height != 0 and new_height == 0:
            self.num_merges = original_height
        else:
            self.num_merges = original_height + 1 - new_height

    def set_num_discontinuities(self):
        for stack in self.game.stacks:
            for i in range(0, len(stack) - 1):
                if stack.tiles[i].value < stack.tiles[i + 1].value:
                    self.num_discontinuities += 1

    def set_num_tiles(self):
        for stack in self.game.stacks:
            self.num_tiles += len(stack)

    def set_score_change(self, original_game):
        new_score = self.game.score_display.score
        old_score = original_game.score_display.score
        self.score_change = new_score - old_score

    def set_largest_height(self):
        largest_height = 0
        for stack in self.game.stacks:
            if len(stack) > largest_height:
                largest_height = len(stack)
        self.largest_height = largest_height

    def set_lowest_height(self):
        lowest_height = self.game.stacks[1].max_size
        for stack in self.game.stacks:
            if len(stack) < lowest_height:
                lowest_height = len(stack)
        self.lowest_height = lowest_height

    def set_average_height(self):
        total_height = 0
        for stack in self.game.stacks:
            total_height += len(stack)
        self.average_height = total_height / (len(self.game.stacks) - 1)

    def set_num_discards(self):
        self.num_discards = self.game.discard_pile.num_discards


class User(ABC):
    def __init__(self, config_location, game):
        config = ConfigParser()
        config.read(config_location)
        self.init_pygame(config)
        self.game = game

    def init_pygame(self, config):
        pygame.init()
        pygame.font.init()
        self.init_font(config)
        self.init_screen(config)
        self.init_clock(config)
        caption = config['pygame_setup']['app_name']
        pygame.display.set_caption(caption)

    def init_font(self, config):
        font_size = int(config['font']['font_size'])
        font_name = config['font']['font_name']
        self.font = pygame.font.SysFont(font_name, font_size)

    def init_screen(self, config):
        screen_size = self.get_pair(config['size']['screen_size'])
        self.screen = pygame.display.set_mode(screen_size)

    def init_clock(self, config):
        self.clock = pygame.time.Clock()
        self.framerate = int(config['pygame_setup']['framerate'])

    def get_pair(self, raw_values):
        str_values = raw_values.split(',')
        pos_x = int(str_values[0])
        pos_y = int(str_values[1])
        return (pos_x, pos_y)

    def create_move(self, pile):
        if pile is None:
            return None
        return Move(self.game, pile)

    @abstractmethod
    def get_move(self, events):
        pass

    def run(self):
        running = True
        self.game.draw(self.screen, self.font)
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            move = self.get_move(events)
            if move is not None:
                self.game.make_move(move.original_pile)
                self.game.draw(self.screen, self.font)
            running = not self.game.game_over()
        self.clock.tick(self.framerate)
        print('Game Over')
        print(self.game.score_display.score)
