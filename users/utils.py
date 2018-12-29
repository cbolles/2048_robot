from abc import ABC, abstractmethod
import pygame
from configparser import ConfigParser


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

    @abstractmethod
    def run(self):
        pass
