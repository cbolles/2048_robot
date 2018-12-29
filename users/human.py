import pygame
from users.utils import User


class Human(User):
    def get_move(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                return int(pygame.key.name(event.key))
        return -1
