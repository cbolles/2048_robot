'''
Contains the code to create a basic bot that will follow a perscribed algorithm
for playing 2048 solitaire. No machine learning is involved

author: Collin Bolles
'''
import pygame
from users.utils import User
from game_objects import Tile, Stack, Pile


class BasicBot(User):
    '''
    Bot that acts as a user making moves based of the perscribed algorithm for making moves
    '''
    def get_lowest_bottom(self, value: int) -> list:
        '''
        Get the stack with the tile that has the lowest value on the bottom that is greater than
        or equal to the given value

        Parameters
        ----------
        value: int
            The lowest value that the tile on the bottom of the stack can have

        Return
        ------
        `list` of Stack
            Returns a list containing stacks with values less than the passed in value
        '''
        if value == 2048:
            return []
        lowest_stacks = []
        for stack in self.game.stacks:
            if len(stack) == 0 or stack.tiles[-1].value == value:
                lowest_stacks.append(stack)
        if len(lowest_stacks) == 0:
            return self.get_lowest_bottom(value * 2)
        return lowest_stacks

    def get_lowest_score(self, stacks: list) -> int:
        '''
        Get the stack that has the lowest total score which is the sum of the tile
        values in the stack

        Parameters
        ----------
        stacks: `list` of stack
            A list of stacks to check for the lowest score

        Return
        ------
        Stack
            The stack with the lowest total score
        '''
        lowest_stack = None
        for stack in stacks:
            is_lower_worth = lowest_stack is None or stack.get_worth() < lowest_stack.get_worth()
            if not stack.is_full() and is_lower_worth:
                lowest_stack = stack
        return lowest_stack

    def get_highest_score(self, stacks: list) -> Stack:
        '''
        Get the stack that has the highest total score which is the sum of the tile
        values in the stack

        Parameters
        ----------
        stacks: `list` of Stack
            A list of stacks to check for the highest score

        Return
        ------
        stack
            The stack with the highest total score
        '''
        highest_stack = None
        for stack in stacks:
            is_higher_worth = highest_stack is None or stack.get_worth() > highest_stack.get_worth()
            if not stack.is_full() and (highest_stack is None or is_higher_worth):
                highest_stack = stack
        return highest_stack

    def get_optimal_stack(self, next_tile: Tile) -> Pile:
        '''
        Get the pile that the algorithm believes would be the best move

        Parameter
        ---------
        next_tile: Tile
            The next tile that the user has to play

        Return
        ------
        Stack
            The pile that the move will be

        '''
        lowest_stacks = self.get_lowest_bottom(next_tile.value)
        if len(lowest_stacks) == 0:
            if not self.game.discard_pile.is_full():
                return self.game.discard_pile
            else:
                return self.get_lowest_score(self.game.stacks)
        optimal_highest_stack = self.get_highest_score(lowest_stacks)
        if optimal_highest_stack is None:
            return self.get_highest_score(self.game.stacks)
        return self.get_highest_score(lowest_stacks)

    def get_move(self, events: list) -> Pile:
        '''
        Implemented method to get the next move being made by the user

        Parameter
        ---------
        events: pygame.event.EventList
            List of pygame events that may be used by the user
        '''
        return self.create_move(self.get_optimal_stack(self.game.tile_queue.peak(0)))
