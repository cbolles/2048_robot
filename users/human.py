import pygame
from users.utils import User


class Human(User):
    def run(self):
        running = True
        self.game.draw(self.screen, self.font)
        while running:
            running = not self.game.game_over()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    pile_number = int(pygame.key.name(event.key))
                    self.game.make_move(pile_number)
                    self.game.draw(self.screen, self.font)
            self.clock.tick(self.framerate)
        print('Game Over')
        print(self.game.score_display.score)
