import pygame
from users.utils import User


class BasicBot(User):
    def get_lowest_bottom(self, value):
        if value == 2048:
            return []
        lowest_stacks = []
        for i in range(0, len(self.game.stacks)):
            tiles = self.game.stacks[i].tiles
            if len(tiles) == 0 or tiles[-1].value == value:
                lowest_stacks.append(i)
        if len(lowest_stacks) == 0:
            return self.get_lowest_bottom(value * 2)
        return lowest_stacks

    def get_lowest_score(self, stack_ids):
        lowest_id = -1
        for stack_id in stack_ids:
            is_lower_worth = self.game.stacks[stack_id].get_worth() < self.game.stacks[lowest_id].get_worth()
            if not self.game.stacks[stack_id].is_full() and (lowest_id == -1 or is_lower_worth):
                lowest_id = stack_id
        return lowest_id

    def get_highest_score(self, stack_ids):
        highest_id = -1
        for stack_id in stack_ids:
            is_higher_worth = self.game.stacks[stack_id].get_worth() > self.game.stacks[highest_id].get_worth()
            if not self.game.stacks[stack_id].is_full() and (highest_id == -1 or is_higher_worth):
                highest_id = stack_id
        return highest_id

    def get_optimal_stack(self, next_tile):
        lowest_stack_ids = self.get_lowest_bottom(next_tile.value)
        if len(lowest_stack_ids) == 0:
            if not self.game.discard_pile.pile_full():
                return len(self.game.stacks)
            else:
                return self.get_lowest_score([i for i in range(0, len(self.game.stacks))])
        optimal_highest_stack = self.get_highest_score(lowest_stack_ids)
        if optimal_highest_stack == -1:
            return self.get_highest_score([i for i in range(0, len(self.game.stacks))])
        return self.get_highest_score(lowest_stack_ids)

    def run(self):
        running = True
        self.game.draw(self.screen, self.font)
        while running:
            running = not self.game.game_over()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pile_number = self.get_optimal_stack(self.game.tile_queue.peak(0))
            self.game.make_move(pile_number)
            self.game.draw(self.screen, self.font)
            self.clock.tick(self.framerate)
        print('Game Over')
        print(self.game.score_display.score)