import pygame
from users.utils import User


class Human(User):
    def get_move(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                target_num = int(pygame.key.name(event.key))
                target_pile = None
                if target_num < len(self.game.stacks):
                    target_pile = self.game.stacks[target_num]
                else:
                    target_pile = self.game.discard_pile
                return self.create_move(target_pile)
        return None
