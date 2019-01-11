from game.game_view import GameView
from game.game_model import GameModel, DiscardPile
import pygame


class InvalidMoveException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class DisplayNotInitializedException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class GameController:
    def __init__(self, game_config_path, params):
        self.game_config_path = game_config_path
        self.display_game = True
        self.game_model = GameModel(game_config_path)
        if 'game_display' in params:
            self.display_game = params['game_display']
        if self.display_game:
            self.game_view = GameView(game_config_path)
            self.game_view.draw(self.game_model)

    def validate_move(self, pile):
        if isinstance(pile, DiscardPile):
            if self.game_model.discard_pile.is_full():
                raise InvalidMoveException('Discard pile is full')
        else:
            next_tile_value = self.game_model.tile_queue.peak(0)
            if pile.is_full() and not pile.tile_values[-1] == next_tile_value:
                raise InvalidMoveException('Stack full and next tile does not match top tile')

    def make_move(self, pile):
        self.validate_move(pile)
        target_pile = self.game_model.get_pile(pile.pile_id)
        self.game_model.make_move(target_pile)
        if self.display_game:
            self.game_view.draw(self.game_model)

    def get_events(self):
        if self.display_game:
            return self.game_view.get_events()
        raise DisplayNotInitializedException('Cannot got pygame events')

    def is_running(self):
        return self.game_model.game_over()
