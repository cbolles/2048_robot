'''
Contains the code to create a basic bot that will follow a perscribed algorithm
for playing 2048 solitaire. No machine learning is involved

author: Collin Bolles
'''
import pygame
from users.utils import User
from game_objects import Tile


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
        `list` of int
            Returns a list containing ids of stacks with values less than the passed in value
        '''
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

    def get_lowest_score(self, stack_ids: list) -> int:
        '''
        Get the stack that has the lowest total score which is the sum of the tile
        values in the stack

        Parameters
        ----------
        stack_ids: `list` of int
            A list of stack_ids to check for the lowest score

        Return
        ------
        int
            The id of the stack with the lowest total score
        '''
        lowest_id = -1
        for stack_id in stack_ids:
            is_lower_worth = self.game.stacks[stack_id].get_worth() < self.game.stacks[lowest_id].get_worth()
            if not self.game.stacks[stack_id].is_full() and (lowest_id == -1 or is_lower_worth):
                lowest_id = stack_id
        return lowest_id

    def get_highest_score(self, stack_ids: list) -> int:
        '''
        Get the stack that has the highest total score which is the sum of the tile
        values in the stack

        Parameters
        ----------
        stack_ids: `list` of int
            A list of stack_ids to check for the highest score

        Return
        ------
        int
            The id of the stack with the highest total score
        '''
        highest_id = -1
        for stack_id in stack_ids:
            is_higher_worth = self.game.stacks[stack_id].get_worth() > self.game.stacks[highest_id].get_worth()
            if not self.game.stacks[stack_id].is_full() and (highest_id == -1 or is_higher_worth):
                highest_id = stack_id
        return highest_id

    def get_optimal_stack(self, next_tile: Tile) -> int:
        '''
        Get the stack that the algorithm believes would be the best move

        Parameter
        ---------
        next_tile: Tile
            The next tile that the user has to play

        Return
        ------
        int
            The id of the pile that the move will be

        '''
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

    def get_move(self, events: pygame.event.EventList) -> int:
        '''
        Implemented method to get the next move being made by the user

        Parameter
        ---------
        events: pygame.event.EventList
            List of pygame events that may be used by the user
        '''
        return self.get_optimal_stack(self.game.tile_queue.peak(0))
