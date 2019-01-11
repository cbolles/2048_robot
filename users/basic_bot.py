'''
Contains the code to create a basic bot that will follow a perscribed algorithm
for playing 2048 solitaire. No machine learning is involved

author: Collin Bolles
'''
from users.base_user import User


class BasicBot(User):
    def __init__(self, config_path, params):
        class_name = type(self).__name__
        super(BasicBot, self).__init__(config_path, params, class_name)
        self.game_model = self.game_controller.game_model

    def get_lowest_bottom(self, value: int) -> list:
        if value == 2048:
            return []
        lowest_stacks = []
        for stack in self.game_model.stacks:
            if len(stack) == 0 or stack.tile_values[-1] == value:
                lowest_stacks.append(stack)
        if len(lowest_stacks) == 0:
            return self.get_lowest_bottom(value * 2)
        return lowest_stacks

    def get_lowest_score(self, stacks: list) -> int:
        lowest_stack = None
        for stack in stacks:
            is_lower_worth = lowest_stack is None or stack.get_worth() < lowest_stack.get_worth()
            if not stack.is_full() and is_lower_worth:
                lowest_stack = stack
        return lowest_stack

    def get_highest_score(self, stacks: list):
        highest_stack = None
        for stack in stacks:
            is_higher_worth = highest_stack is None or stack.get_worth() > highest_stack.get_worth()
            if not stack.is_full() and (highest_stack is None or is_higher_worth):
                highest_stack = stack
        return highest_stack

    def get_optimal_stack(self, next_tile_value):
        lowest_stacks = self.get_lowest_bottom(next_tile_value)
        if len(lowest_stacks) == 0:
            if not self.game_model.discard_pile.is_full():
                return self.game_model.discard_pile
            else:
                return self.get_lowest_score(self.game_model.stacks)
        optimal_highest_stack = self.get_highest_score(lowest_stacks)
        if optimal_highest_stack is None:
            return self.get_highest_score(self.game_model.stacks)
        return self.get_highest_score(lowest_stacks)

    def get_target_pile(self, events):
        return self.get_optimal_stack(self.game_model.tile_queue.peak(0))

    def is_running(self):
        return not self.game_model.game_over()
