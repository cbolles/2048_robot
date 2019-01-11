from pathlib import Path
import os
import pygame
from configparser import ConfigParser
from enum import Enum


class Color(Enum):
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)


class TileView:
    def __init__(self, value, height, width):
        self.height = height
        self.width = width
        self.image = self.get_image(value)

    def get_image(self, value):
        current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        image_name = 'image_' + str(value) + '.png'
        resource_dir = current_dir / '..' / 'resources'
        image_path = str(resource_dir / image_name)
        image = pygame.image.load(image_path)
        return pygame.transform.scale(image, (self.width, self.height))

    def draw(self, screen, x_pos, y_pos):
        screen.blit(self.image, (x_pos, y_pos))


class GameView:
    @staticmethod
    def parse_pair(value):
        raw_values = value.split(',')
        return int(raw_values[0]), int(raw_values[1])

    @staticmethod
    def generate_tile_views(tile_dimensions):
        tile_values = [pow(2, i) for i in range(1, 11)]
        tile_views = dict()
        height = tile_dimensions[0]
        width = tile_dimensions[1]
        for tile_value in tile_values:
            tile_views[tile_value] = TileView(tile_value, height, width)
        return tile_views

    def __init__(self, view_config_path):
        self.config = ConfigParser()
        self.config.read(view_config_path)
        pygame.init()
        pygame.font.init()
        self.init_font()
        self.init_screen()
        self.init_tiles()
        self.init_stack_positions()
        self.discard_pile_pos = GameView.parse_pair(self.config['view']['discard_pile_pos'])
        self.discard_pile_dim = GameView.parse_pair(self.config['view']['discard_pile_dim'])
        self.tile_queue_pos = GameView.parse_pair(self.config['view']['tile_queue'])
        self.score_pos = GameView.parse_pair(self.config['view']['score_display'])

    def init_font(self):
        font_name = self.config['view']['font_name']
        font_size = int(self.config['view']['font_size'])
        self.font = pygame.font.SysFont(font_name, font_size)

    def init_screen(self):
        self.screen_size = GameView.parse_pair(self.config['view']['screen_size'])
        self.screen = pygame.display.set_mode(self.screen_size)

    def init_tiles(self):
        tile_dimensions = GameView.parse_pair(self.config['view']['tile_size'])
        self.tile_views = GameView.generate_tile_views(tile_dimensions)

    def init_stack_positions(self):
        self.stack_positions = []
        num_stacks = int(self.config['view']['num_stacks'])
        stack_spacing = self.screen_size[0] // num_stacks
        start_pos = GameView.parse_pair(self.config['view']['stack_start'])
        for i in range(0, num_stacks):
            stack_pos = (start_pos[0] + stack_spacing * i, start_pos[1])
            self.stack_positions.append(stack_pos)

    def draw_stack(self, stack_pos, stack_model):
        tile_x = stack_pos[0]
        tile_y = stack_pos[1]
        tile_delta = self.tile_views[2].height / 3
        for tile_value in stack_model.tile_values:
            self.tile_views[tile_value].draw(self.screen, tile_x, tile_y)
            tile_y += tile_delta

    def draw_discard_pile(self, game_model):
        box_x = self.discard_pile_pos[0]
        box_y = self.discard_pile_pos[1]
        box_height = self.discard_pile_dim[1]
        box_width = self.discard_pile_dim[0]
        for i in range(0, game_model.discard_pile.max_discards):
            if i < game_model.discard_pile.num_discards:
                pygame.draw.rect(self.screen, Color.RED.value, (box_x, box_y, box_width, box_height))
            else:
                pygame.draw.rect(self.screen, Color.WHITE.value, (box_x, box_y, box_width, box_height), 3)
            box_y -= box_height

    def draw_tile_queue(self, game_model):
        tile_x = self.tile_queue_pos[0]
        tile_y = self.tile_queue_pos[1]
        tile_delta = self.tile_views[2].width
        for tile_value in game_model.tile_queue.tile_values:
            self.tile_views[tile_value].draw(self.screen, tile_x, tile_y)
            tile_x += tile_delta

    def draw_score(self, game_model):
        text_surface = self.font.render('Score: ' + str(game_model.score), False, Color.WHITE.value)
        self.screen.blit(text_surface, self.score_pos)

    def get_events(self):
        return pygame.event.get()

    def draw(self, game_model):
        self.screen.fill(Color.BLACK.value)
        # Draw stacks
        for i in range(0, len(game_model.stacks)):
            self.draw_stack(self.stack_positions[i], game_model.stacks[i])
        self.draw_discard_pile(game_model)
        self.draw_tile_queue(game_model)
        self.draw_score(game_model)
        pygame.display.flip()