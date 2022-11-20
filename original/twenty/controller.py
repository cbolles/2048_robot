from twenty.user import User
from twenty.view import GameView
from twenty.model import GameModel
import pygame
from typing import List


class GameController:
    def __init__(self, initial_state: List[List[int]], user: User):
        self.model = GameModel(initial_state)

        screen = pygame.display.set_mode((400, 400))
        pygame.init()
        self.view = GameView(screen, self.model)

        self.user = user

    def run(self):
        """
        Run the game.
        """
        while not self.model.game_over():
            self.view.draw()
            direction = self.user.move()
            self.model = self.model.move(direction)
            self.view.update(self.model)

        print('Game Over')
