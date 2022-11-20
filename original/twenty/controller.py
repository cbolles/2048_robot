from twenty.user import User
from twenty.view import GameView
from twenty.model import GameModel
import pygame
from typing import List


class GameController:
    def __init__(self, initial_state: List[List[int]], user: User):
        self.model = GameModel(initial_state)
        self.view = GameView(self.model)
        self.user = user

    def run(self):
        """
        Run the game.
        """
        while not self.model.game_over():
            self.view.draw()
            direction = self.user.get_direction()
            self.model = self.model.move(direction)

        print('Game Over')
