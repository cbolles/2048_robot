from abc import ABC, abstractmethod
from twenty.model import Direction

class User(ABC):
    def move(self) -> Direction:
        """
        Get the next move from the user.
        """
        pass


class HumanUser(User):
    def move(self) -> Direction:
        """
        Get the next move from the user.
        """
        while True:
            event = pygame.key.get_pressed()
            if event[pygame.K_UP]:
                return Direction.UP
            elif event[pygame.K_DOWN]:
                return Direction.DOWN
            elif event[pygame.K_LEFT]:
                return Direction.LEFT
            elif event[pygame.K_RIGHT]:
                return Direction.RIGHT
