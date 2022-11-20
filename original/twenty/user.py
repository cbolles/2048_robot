from abc import ABC, abstractmethod
from twenty.model import Direction
import pygame


class User(ABC):
    def move(self) -> Direction:
        """
        Get the next move from the user.
        """
        pass


class HumanUser(User):
    def move(self) -> Direction:
        """
        Get the next move from the user. This user works based on the
        arrow keys.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        return Direction.UP
                    elif event.key == pygame.K_DOWN:
                        return Direction.DOWN
                    elif event.key == pygame.K_LEFT:
                        return Direction.LEFT
                    elif event.key == pygame.K_RIGHT:
                        return Direction.RIGHT
                    elif event.key == pygame.K_ESCAPE:
                        exit()

            pygame.time.wait(10)
