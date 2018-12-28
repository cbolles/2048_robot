import os
from pathlib import Path
import pygame
from random import randint
from configparser import ConfigParser


class Tile:
    def __init__(self, value, height=143, width=93):
        self.value = value
        self.height = height
        self.width = width
        self.image = self.get_image(value)

    def get_image(self, value):
        resources_dir = Path(os.path.dirname(os.path.abspath(__file__))) / 'resources'
        image_name = 'image_' + str(value) + '.png'
        image_path = str(resources_dir / 'tiles' / image_name)
        image = pygame.image.load(image_path)
        return pygame.transform.scale(image, (self.width, self.height))

    def draw(self, screen, xPos, yPos):
        screen.blit(self.image, (xPos, yPos))

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.value == other.value
        return False

    def __str__(self):
        return str(self.value)


class Stack:
    def __init__(self, xPos, yPos, max_size):
        self.tiles = []
        self.xPos = xPos
        self.yPos = yPos
        self.max_size = max_size

    def merge(self, multiplier):
        if len(self.tiles) < 2 or not self.tiles[-1] == self.tiles[-2]:
            return 0
        result = self.tiles.pop(-1).value + self.tiles.pop(-1).value
        self.tiles.append(Tile(result))
        return result * multiplier + self.merge(multiplier + 1)

    def add_tile(self, tile):
        # If adding a list of tiles
        if isinstance(tile, list) and len(self.tiles + tile) <= self.max_size:
            self.tiles = self.tiles + tile
        # If adding a single tile
        elif len(self.tiles) < self.max_size:
            self.tiles.append(tile)
        score_change = self.merge(1)
        if self.tiles[0] == Tile(2048):
            self.tiles = []
        return score_change

    def is_full(self):
        return len(self.tiles) == self.max_size

    def draw(self, screen):
        tileX = self.xPos
        tileY = self.yPos
        for tile in self.tiles:
            tile.draw(screen, tileX, tileY)
            tileY += tile.height / 3

    def __len__(self):
        return len(self.tiles)


class TileQueue:
    def __init__(self, xPos, yPos):
        self.tiles = self.init_tiles()
        self.xPos = xPos
        self.yPos = yPos

    def generate_tile(self):
        prob = randint(1, 6)
        return Tile(pow(2, prob))

    def init_tiles(self):
        return [self.generate_tile(), self.generate_tile()]

    def pull(self):
        tile = self.tiles.pop(0)
        self.tiles.append(self.generate_tile())
        return tile

    def draw(self, screen):
        tileX = self.xPos
        tileY = self.yPos
        for i in range(len(self.tiles) - 1, -1, -1):
            self.tiles[i].draw(screen, tileX, tileY)
            tileX += self.tiles[i].width


class ScoreDisplay:
    def __init__(self, xPos, yPos, color=(255, 255, 255)):
        self.xPos = xPos
        self.yPos = yPos
        self.score = 0
        self.color = color

    def draw(self, screen, font):
        text_surface = font.render('Score: ' + str(self.score), False, self.color)
        screen.blit(text_surface, (self.xPos, self.yPos))

    def increase_score(self, score):
        self.score += score


class DiscardPile:
    def __init__(self, xPos, yPos, height=100, width=50, max_discards=2):
        self.xPos = xPos
        self.yPos = yPos
        self.height = height
        self.width = width
        self.max_discards = max_discards
        self.num_discards = 0

    def add_discard(self):
        self.num_discards += 1

    def pile_full(self):
        return self.num_discards == self.max_discards

    def clear_discards(self):
        self.num_discards = 0

    def draw(self, screen):
        box_x = self.xPos
        box_y = self.yPos
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


class Game:
    def __init__(self, config_file_location):
        config = ConfigParser()
        config.read(config_file_location)
        self.size = self.get_pair(config['size']['screen_size'])
        self.init_stacks(config)
        self.init_tile_queue(config)
        self.init_score_display(config)
        self.init_discard_pile(config)

    def init_stacks(self, config):
        num_stacks = int(config['game_setup']['num_stacks'])
        max_size = int(config['game_setup']['max_stack_size'])
        stack_x, stack_y = self.get_pair(config['position']['stack_start'])
        distance = self.size[0] // num_stacks
        self.stacks = []
        for i in range(0, num_stacks):
            self.stacks.append(Stack(stack_x, stack_y, max_size))
            stack_x += distance

    def init_tile_queue(self, config):
        queue_x, queue_y = self.get_pair(config['position']['tile_queue'])
        self.tile_queue = TileQueue(queue_x, queue_y)

    def init_score_display(self, config):
        score_x, score_y = self.get_pair(config['position']['score_display'])
        self.score_display = ScoreDisplay(score_x, score_y)

    def init_discard_pile(self, config):
        pile_x, pile_y = self.get_pair(config['position']['discard_pile'])
        self.discard_pile = DiscardPile(pile_x, pile_y)

    def get_pair(self, raw_values):
        str_values = raw_values.split(',')
        pos_x = int(str_values[0])
        pos_y = int(str_values[1])
        return (pos_x, pos_y)

    def make_move(self, pile_number):
        # If adding to a stack
        if pile_number < len(self.stacks):
            stack = self.stacks[pile_number]
            if not stack.is_full():
                score_change = stack.add_tile(self.tile_queue.pull())
                self.score_display.increase_score(score_change)
                # 2048 Achieved
                if len(stack) == 0:
                    self.discard_pile.clear_discards()
        # If trying to add to discard pile
        else:
            if not self.discard_pile.pile_full():
                self.tile_queue.pull()
                self.discard_pile.add_discard()

    def draw(self, screen, font):
        screen.fill((0, 0, 0))
        for stack in self.stacks:
            stack.draw(screen)
        self.tile_queue.draw(screen)
        self.score_display.draw(screen, font)
        self.discard_pile.draw(screen)
        pygame.display.flip()
