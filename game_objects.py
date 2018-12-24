import os
from pathlib import Path
import pygame


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


class Stack:
    def __init__(self, xPos, yPos):
        self.tiles = []
        self.xPos = xPos
        self.yPos = yPos

    def add_tile(self, tile):
        # If adding a list of tiles
        if isinstance(tile, list):
            self.tiles = self.tiles + tile
        # If adding a single tile
        else:
            self.tiles.append(tile)

    def draw(self, screen):
        tileX = self.xPos
        tileY = self.yPos
        for tile in self.tiles:
            tile.draw(screen, tileX, tileY)
            tileY += tile.height / 3


class TileQueue:
    def __init__(self, xPos, yPos):
        self.tiles = self.init_tiles()
        self.xPos = xPos
        self.yPos = yPos

    def init_tiles(self):
        # TODO: Add proper generator
        return [Tile(2), Tile(4)]

    def pull(self):
        # TODO: Get the next value in queue and generate next value
        pass

    def draw(self, screen):
        tileX = self.xPos
        tileY = self.yPos
        for tile in self.tiles:
            tile.draw(screen, tileX, tileY)
            tileX += tile.width / 2
