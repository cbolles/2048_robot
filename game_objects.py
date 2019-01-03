'''
Contains all elements directly related to the mechanics of the game itself.
Each class contains its own ability to draw to a pygame screen and keep
track of its state.

All modification of game elements should be handled through the Game object,
game elements should only be used to access its state.

author: Collin Bolles
'''
import os
from pathlib import Path
import pygame
from random import randint
from configparser import ConfigParser
import abc


class Tile:
    '''
    Represents each individual tile that will be on the screen. The tile
    keeps track of its score as well as its position and image for use with
    pygame

    Attributes
    ----------
    value: int
        The value of the tile
    height: int
        The height of the tile as it will appear on the pygame screen
    width: int
        The width of the tile as it will appear on the pygame screen
    image: Surface
        The image representing the tile as it will appear on the pygame screen
    '''
    def __init__(self, value: int, height=143, width=93):
        '''
        The init function handles setting the correct height and width as
        well as getting the correct image to match the value passed in.

        Note
        ----
        The value passed be in must be in the following
        2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, or 2048

        Parameters
        ----------
        value: int
            The face value of the tile
        height: int
            The height that the tile will have on the pygame screen
        width: int
            The width that the tile will have on the pygame screen
        '''
        self.value = value
        self.height = height
        self.width = width
        self.image = self.get_image(value)

    def get_image(self, value: int) -> pygame.Surface:
        '''
        Helper method to get the corrent image based on the given value.

        Note
        ----
        The image is assumed to be located the directory resources/tiles at the same
        level as this file

        Parameters
        ----------
        value: int
            The value of the tile
        '''
        resources_dir = Path(os.path.dirname(os.path.abspath(__file__))) / 'resources'
        image_name = 'image_' + str(value) + '.png'
        image_path = str(resources_dir / 'tiles' / image_name)
        image = pygame.image.load(image_path)
        return pygame.transform.scale(image, (self.width, self.height))

    def draw(self, screen: pygame.Surface, x_pos: int, y_pos: int) -> None:
        '''
        Method used to draw the tile at a given x, y position to a given pygame screen

        Note
        ----
        The x and y positions are assumed to be on the screen

        Parameters
        ----------
        screen: pygame.Surface
            The pygame "screen" that the tile will be drawn onto
        x_pos: int
            The x coordinate on the screen to draw the tile
        x_pos: int
            The y coordinate on the screen to draw the tile
        '''
        screen.blit(self.image, (x_pos, y_pos))

    def __eq__(self, other) -> bool:
        '''
        Tiles are equal to each other if they have the same value

        Parameters
        ----------
        other: Tile
            The other tile to compare to

        Returns
        -------
        bool
            True if the values are equal, false if otherwise
        '''
        return self.value == other.value

    def __lt__(self, other) -> bool:
        '''
        The tile is less than another if its value is less than another

        Parameters
        ----------
        other: Tile
            The other tile to compare to

        Returns
        -------
        bool
            True if the value of this tile is less than the value of the other tile
        '''
        return self.value < other.value

    def __gt__(self, other) -> bool:
        '''
        The tile is greater than another if its value is greater than another

        Parameters
        ----------
        other: Tile
            The other tile to compare to

        Returns
        -------
        bool
            True if the value of this tile is greater than the value of the other tile
        '''
        return self.value > other.value

    def __str__(self) -> str:
        '''
        String representation of the object, used mostly for debugging

        Returns
        -------
        str
            Name of the class and the value of the tile
        '''
        return 'Tile: ' + str(self.value)


class Pile(abc.ABC):
    @abc.abstractclassmethod
    def is_full(self):
        pass

    @abc.abstractclassmethod
    def add_tile(self, tile):
        pass


class Stack(Pile):
    '''
    Represents the possible regions on which the user can stack tiles onto.
    This does not include any discards that the user may make

    Attributes
    ----------
    x_pos: int
        The x position on the screen where the stack will be
    y_pos: int
        The y position on the screen where the stack will be
    tiles: `list` of Tile
    max_size: int
        The largest number of tiles the stack can hold before it is full
    pile_id: int
        The identifier of each individual stack
    '''
    def __init__(self, x_pos: int, y_pos: int, max_size: int, pile_id: int):
        '''
        Initializes the stack with an empty list of tiles and with a given max size
        and coordinates for use with pygame

        Parameters
        ----------
        x_pos: int
            The x position on the screen where the stack will be
        y_pos: int
            The y position on the screen where the stack will be
        max_size: int
            The largest number of tiles the stack can hold before it is full
        '''
        self.tiles = []
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.max_size = max_size
        self.pile_id = pile_id

    def merge(self, multiplier: int) -> int:
        '''
        Handles merging the tiles that have the same value. In addition, this methods
        keeps track of the score associated with each merge and the multiplier being
        applied to the score. This method is called recursivly with each successful
        merge

        Parameters
        ----------
        multiplier: int
            The value used to increase the score when multiple merges happen at once

        Return
        ------
        int
            Score generated from the merge with the given multiplier
        '''
        if len(self.tiles) < 2 or not self.tiles[-1] == self.tiles[-2]:
            return 0
        result = self.tiles.pop(-1).value + self.tiles.pop(-1).value
        self.tiles.append(Tile(result))
        return result * multiplier + self.merge(multiplier + 1)

    def add_tile(self, tile: Tile) -> int:
        '''
        Handles adding a given tile to the list of tiles. Returns the score created
        by adding the tile to the shack.

        Notes
        -----
        The tile being added is not validated. It is assumed that it is a valid move
        to add the given tile to the stack

        Parameters
        ----------
        tile: Tile, `list` of Tile
            The tile or tiles to be added to the array of tiles

        Return
        ------
        int
            The score associated with adding the given tile to the stack
        '''
        # If adding a list of tiles
        if isinstance(tile, list) and len(self.tiles + tile) <= self.max_size:
            self.tiles = self.tiles + tile
        # If adding a single tile
        else:
            self.tiles.append(tile)
        score_change = self.merge(1)
        if self.tiles[0] == Tile(2048):
            self.tiles = []
        return score_change

    def is_full(self) -> bool:
        '''
        Checks if the number of tile on the stack equals the max size of the stack

        Return
        ------
            bool
                True if the number of tiles on the stack equals the max size
        '''
        return len(self.tiles) == self.max_size

    def get_worth(self) -> int:
        '''
        Returns the total value of each tile in the stack

        Return
        ------
        int
            Total value of tile in stack
        '''
        return sum([tile.value for tile in self.tiles])

    def draw(self, screen: pygame.Surface) -> None:
        '''
        Handles drawing the stack onto the screen. The first tile is drawn
        from the x and y coordinate of the stack and each following tile is drawn
        another 1/3 of the height of a tile down

        Parameters
        ----------
        screen: pygame.Surface
            The screen on which to drawn the stack
        '''
        tile_x = self.x_pos
        tile_y = self.y_pos
        for tile in self.tiles:
            tile.draw(screen, tile_x, tile_y)
            tile_y += tile.height / 3

    def __len__(self) -> int:
        '''
        Length of a stack is defined as the number of tiles it has

        Return
        ------
        int
            The length of the number of tiles in the stack
        '''
        return len(self.tiles)

    def __lt__(self, other) -> bool:
        '''
        A stack is less than another if its worth is less than another

        Parameters
        ----------
        stack: Stack
            The other stack to compare to

        Return
        ------
        bool
            True if the worth of this stack is less than the worth of another
        '''
        return self.get_worth() < other.get_worth()

    def __gt__(self, other) -> bool:
        '''
        A stack is greater than another if its worth is greater than another

        Parameters
        ----------
        other: Stack
            The other stack to compare to

        Return
        ------
        bool
            True if the worth of this stack is greater than another
        '''
        return self.get_worth() > other.get_worth()

    def __eq__(self, other) -> bool:
        '''
        Stacks that have the same pile_id

        Paramters
        ---------
        other: Pile
            The other tile to compare to

        Return
        ------
        bool
            True if the worth of this tile is the same as another
        '''
        return self.pile_id == other.pile_id

    def __str__(self) -> str:
        '''
        To String used for debugging

        Return
        ------
        str
            The type of the class with all the tiles in the class
        '''
        return 'Stack with tiles: ' + str(self.tiles)


class DiscardPile(Pile):
    '''
    Represents discards made by the user. The actual Tiles discardsed are not kept
    track of, only the number of discards

    Attributes
    ----------
    x_pos: int
        The x coordinate where to display the discard pile
    y_pos: int
        The y coordinate where to display the discard pile
    height: int
        The height of the discard pile for display
    width: int
        The width of the discard pile for display
    max_discards: int
        The maximum number of discards that can be made
    pile_id: int
        The unique id of the discard pil
    '''
    def __init__(self, x_pos: int, y_pos: int, pile_id: int, height=100, width=50, max_discards=2):
        '''
        Initializes the discard pile with a given x and y coordinate, height, width,
        and maximum number of discards that can be made by the user

        Parameters
        ----------
        x_pos: int
            The x coordinate where to display the discard pile
        y_pos: int
            The y coordinate where to display the discard pile
        height: int
            The height of the discard pile for display
        width: int
            The width of the discard pile for display
        max_discards: int
            The maximum number of discards that the user can make
        pile_id: int
            The unique id of the discard pile
        '''
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.height = height
        self.width = width
        self.max_discards = max_discards
        self.num_discards = 0
        self.pile_id = pile_id

    def add_tile(self, tile: Tile) -> None:
        '''
        Increases the number of discards that have been made

        Note
        ----
        Validation to ensure that the number of discards is not beyound the
        maximum size is not made here
        '''
        self.num_discards += 1

    def is_full(self) -> bool:
        '''
        Retuns if the number of discards that have been made equals the max
        number of discards

        Return
        ------
        bool
            True if the max number of discards equal the number of discards made
        '''
        return self.num_discards == self.max_discards

    def clear_discards(self) -> None:
        '''
        Sets the number of discards made to zero
        '''
        self.num_discards = 0

    def draw(self, screen: pygame.Surface) -> None:
        '''
        Handles displaying the discards pile and the number of discards to the screen.
        The discards are represented by red rectangles and the available spaces for
        discards are represented by rectangles outlines in white
        '''
        box_x = self.x_pos
        box_y = self.y_pos
        box_height = self.height / self.max_discards
        box_width = self.width
        color_fill = (255, 0, 0)
        color_outline = (255, 255, 255)
        for i in range(0, self.max_discards):
            if i < self.num_discards:
                pygame.draw.rect(screen, color_fill, (box_x, box_y, box_width, box_height))
            else:
                pygame.draw.rect(screen, color_outline, (box_x, box_y, box_width, box_height), 3)
            box_y -= box_height

    def __str__(self) -> str:
        '''
        String representation of the object with the name of the class and the number
        of discards used out of the total
        '''
        return 'DiscardPile: ' + str(self.num_discards) + ' used out of ' + str(self.max_discards) + ' discards'


class TileQueue:
    '''
    Represents the tiles that the user will have to pick from to make a move

    Attributes
    ----------
    x_pos: int
        The x coordinate for the object to appear on a pygame screen
    y_pos: int
        The y coordinate for the object to appear on a pygame screen
    tiles: `list` of Tile
        The tiles that the user will have to pick from
    '''
    def __init__(self, x_pos: int, y_pos: int):
        '''
        Initalizes the object with a given x and y coordinate and a list with
        randomly generated tiles

        Parameters
        ----------
        x_pos: int
            The x coordinate for the object to appear on a pygame screen
        y_pos: int
            The y coordinate for the object to appear on a pygame screen
        '''
        self.tiles = self.init_tiles()
        self.x_pos = x_pos
        self.y_pos = y_pos

    def generate_tile(self) -> Tile:
        '''
        Used to generate a tile randomly

        Return
        ------
        Tile
            A tile with a value randomly 2, 4, 8, 16, 32, or 64
        '''
        prob = randint(1, 6)
        return Tile(pow(2, prob))

    def init_tiles(self) -> list:
        '''
        Used to initalize the tile queue

        Return
        ------
        `list` of Tile
            A list with two randomly generated tiles
        '''
        return [self.generate_tile(), self.generate_tile()]

    def pull(self) -> Tile:
        '''
        Takes the first Tile in the queue

        Returns
        -------
        Tile
            The tile removed from the begining of the array
        '''
        tile = self.tiles.pop(0)
        self.tiles.append(self.generate_tile())
        return tile

    def peak(self, index: int) -> Tile:
        '''
        Used to look at Tile in the queue without removing it

        Parameter
        ---------
        index: int
            The location in the list to get the tile at

        Returns
        -------
        Tile
            The tile at the given index
        '''
        return self.tiles[index]

    def draw(self, screen: pygame.Surface) -> None:
        '''
        Display the tiles in the tile queue to a pygame surface. Tiles are displayed
        starting at the x and y coordinate of the tile queue and moved towards the right

        Parameters
        ----------
        screen: pygame.Surface
            The surface to display the queue on
        '''
        tile_x = self.x_pos
        tile_y = self.y_pos
        for i in range(len(self.tiles) - 1, -1, -1):
            self.tiles[i].draw(screen, tile_x, tile_y)
            tile_x += self.tiles[i].width

    def __str__(self) -> str:
        '''
        To String that returns the name of the class and the tiles in the queue
        Return
        ------
        str
            The name of the class and the tiles in the queue
        '''
        return 'Tile Queue: ' + str(self.tiles)


class ScoreDisplay:
    '''
    Represents the score the game has and the details needed to display the score on a
    pygame surface

    Attributes
    ----------
    x_pos: int
        The x coordinate to display the score on a pygame surface
    y_pos: int
        The y coordinate to display the score on a pygame surface
    '''
    def __init__(self, x_pos: int, y_pos: int, color=(255, 255, 255)):
        '''
        Initalizes the object with a given x and y coordinate, a color for the text, and
        a score with the value of zero

        Parameters
        ----------
        x_pos: int
            The x coordinate to display the score on a pygame surface
        y_pos: int
            The y coordinate to display the score on a pygame surface
        color: `list` of int
            The RGB color of the text to display, defaulted to white
        '''
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.score = 0
        self.color = color

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        '''
        Display the score at a given x and y coordinate

        Parameters
        ----------
        screen: pygame.Surface
            The surface on which to display the score
        font: pygame.font.Font
            The font in which to dosplay the score
        '''
        text_surface = font.render('Score: ' + str(self.score), False, self.color)
        screen.blit(text_surface, (self.x_pos, self.y_pos))

    def increase_score(self, score_change: int) -> None:
        '''
        Handles increasing the score by a given amount

        Parameters
        ----------
        score: int
            The amount to increase the score by
        '''
        self.score += score_change

    def __str__(self) -> str:
        '''
        String representation of the object used for debugging

        Return
        ------
        str
            The name of the class and the score
        '''
        return 'ScoreDisplay: ' + str(self.score)


class InvalidMoveException(Exception):
    '''
    Generic exception used whenever an invald move is made
    '''
    def __init__(self, message):
        '''
        Initializes a generic exception with the given error message

        Parameters
        ----------
        message: str
            The error message generated by the invalid move
        '''
        Exception.__init__(self, message)


class Game:
    '''
    The class that handles combining all the game elements together to run the
    2048 game. This class handles both the logic of the moves as well as the display
    of the game

    Attributes
    ----------
    size: `list` of int
        The size of the pygame screen as an array with width, height
    stacks: `list` of Stack
        List of stacks that the user can add tiles onto
    tile_queue: TileQueue
        The tile queue that will store the next possible tiles to be used
    score_display: ScoreDisplay
        Handles the score and the display of the score to the user
    '''
    def __init__(self, config_file_location: str):
        '''
        Initializes the object using configurations find in the file located at
        the given config file location

        Parameters
        ----------
        config_file_location: str
            The location of the config file to initilize the game elements with
        '''
        config = ConfigParser()
        config.read(config_file_location)
        self.size = self.get_pair(config['size']['screen_size'])
        self.init_stacks(config)
        self.init_tile_queue(config)
        self.init_score_display(config)
        self.init_discard_pile(config)

    def init_stacks(self, config: ConfigParser) -> None:
        '''
        Initalizes the stacks with the coordinates and maximum sizes from the
        configuration file
        '''
        self.stacks = []
        num_stacks = int(config['game_setup']['num_stacks'])
        max_size = int(config['game_setup']['max_stack_size'])
        stack_x, stack_y = self.get_pair(config['position']['stack_start'])
        distance = self.size[0] // num_stacks
        for i in range(0, num_stacks):
            self.stacks.append(Stack(stack_x, stack_y, max_size, i))
            stack_x += distance

    def init_tile_queue(self, config: ConfigParser) -> None:
        '''
        Initalizes the tile queue with the coordinates from the configuration
        file
        '''
        queue_x, queue_y = self.get_pair(config['position']['tile_queue'])
        self.tile_queue = TileQueue(queue_x, queue_y)

    def init_score_display(self, config: ConfigParser) -> None:
        '''
        Initializes the score display with the coordinates from the
        configuration file
        '''
        score_x, score_y = self.get_pair(config['position']['score_display'])
        self.score_display = ScoreDisplay(score_x, score_y)

    def init_discard_pile(self, config: ConfigParser) -> None:
        '''
        Initalizes the discard pile with the coordinates from the configuration
        file
        '''
        pile_x, pile_y = self.get_pair(config['position']['discard_pile'])
        self.discard_pile = DiscardPile(pile_x, pile_y, len(self.stacks))

    def get_pair(self, raw_values: str) -> list:
        '''
        Takes in a string that has coordinates in the formate 'x,y' and converts
        the input to a list of ints

        Parameters:
        ----------
        raw_values: str
            String with a pair of values in CSV formate

        Return
        ------
        `list` of int
            The pair has a list of integers
        '''
        str_values = raw_values.split(',')
        pos_x = int(str_values[0])
        pos_y = int(str_values[1])
        return (pos_x, pos_y)

    def get(self, pile: Pile) -> Pile:
        for stack in self.stacks:
            if pile.pile_id == stack.pile_id:
                return stack
        return self.discard_pile

    def validate(self, pile) -> None:
        '''
        Handles validating a move. A move is invalid if
        1) The pile number is not found
        2) The pile number is to the discard pile, but it is full
        3) The pile number is to a Stack, but the Stack is full and the new tile
        value does not match the value on the bottom of the Stack
        Invalid moves will throw an InvalidMoveException

        Parameters
        ----------
        pile: Pile
            The pile to make the move on either a stack or a discard pile
        '''
        # If the requested pile is the discard pile, check if the pile is full
        if isinstance(pile, DiscardPile):
            if self.discard_pile.is_full():
                raise InvalidMoveException('Discard pile is full')
        # If the requested pile is a stack, check if the stack can accept another tile
        else:
            next_tile = self.tile_queue.peak(0)
            if pile.is_full() and not pile.tiles[-1] == next_tile:
                raise InvalidMoveException('Stack full and next tile does not match top tile')

    def make_move(self, move) -> None:
        '''
        Validate the move request then move the Tile from the top of the tile queue
        to the target pile. Handles if 2048 is achieved including clearing the discards

        Parameters
        ----------
        move: Move
            Contains the information about the impact of the move and the target pile
            id
        '''
        pile = move.original_pile
        self.validate(pile)
        next_tile = self.tile_queue.pull()
        # If adding to the discard
        if isinstance(pile, DiscardPile):
            self.discard_pile.add_tile(next_tile)
        # If adding to a stack
        else:
            score_change = pile.add_tile(next_tile)
            # 2048 achieved
            if len(pile) == 0:
                self.discard_pile.clear_discards()
            self.score_display.increase_score(score_change)

    def game_over(self) -> bool:
        '''
        Checks to see if each pile is full

        Return
        ------
        bool
            True if every pile including the discard pile is full
        '''
        for stack in self.stacks:
            if not stack.is_full():
                return False
        return self.discard_pile.is_full()

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        '''
        Handles drawing all of the game elements to a given screen

        Parameters
        ----------
        screen: pygame.Surface
            pygame surface to draw the game elements to
        font: pygame.font.Font
            pygame Font to draw the score using
        '''
        screen.fill((0, 0, 0))
        for stack in self.stacks:
            stack.draw(screen)
        self.tile_queue.draw(screen)
        self.score_display.draw(screen, font)
        self.discard_pile.draw(screen)
        pygame.display.flip()

    def __str__(self) -> str:
        '''
        String representation of the game

        Return
        ------
        String with the name of the class and the score of the game
        '''
        return 'Game: ' + str(self.score_display.score)
