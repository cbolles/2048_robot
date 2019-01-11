from abc import ABC, abstractmethod
from game.game_controller import GameController
from configparser import ConfigParser
from time import time, sleep


class UserStats:
    def __init__(self, user_type):
        self.moves_made = 0
        self.user_type = user_type
        self.user_score = 0
        self.start_time = 0
        self.end_time = 0
        self.time_taken = 0

    def start(self):
        self.start_time = time()

    def finish(self):
        self.end_time = time()
        self.time_taken = self.end_time - self.start_time


class User(ABC):
    def __init__(self, params, user_type):
        game_config_path = params['game_config_path']
        config = ConfigParser()
        config.read(game_config_path)
        self.refresh_rate = int(config['user']['refresh_rate'])
        self.game_controller = GameController(game_config_path, dict())
        self.user_stats = UserStats(user_type)

    @abstractmethod
    def get_target_pile(self):
        pass

    @abstractmethod
    def is_running(self):
        pass

    def run(self):
        running = True
        self.user_stats.start()
        while running:
            target_pile = self.get_target_pile()
            if target_pile is not None:
                self.game_controller.make_move(target_pile)
                self.user_stats.moves_made += 1
            running = self.is_running()
            sleep(self.refresh_rate)
        self.user_stats.finish()
