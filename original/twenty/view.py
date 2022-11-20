import pygame
from twenty.model import GameModel

class TileView:
    """
    View for a single tile. Displays the number.
    """
    def __init__(self, screen, number: int):
        self.screen = screen
        self.number = number
        self.font = pygame.font.SysFont("monospace", 50)

    def draw(self, x: int, y: int):
        """
        Draw the tile on the screen.
        """
        text = self.font.render(str(self.number), 1, (255, 255, 255))
        self.screen.blit(text, (y, x))


class GameView:
    """
    Implements the view logic for the 2048 game. This has the ability to take
    in a board and produce the cooresponding view of the tiles.
    """
    def __init__(self, screen, board: GameModel):
        self.screen = screen
        self.board = board

    def update(self, board: GameModel):
        """
        Update the view to display the new board.
        """
        self.board = board

    def draw(self):
        """
        Draws the board to the screen.
        """
        # Clear the screen to black
        self.screen.fill((0, 0, 0))

        # Print all of the numbers
        for x in range(4):
            for y in range(4):
                TileView(self.screen, self.tiles[x][y]).draw(x * 100, y * 100)

        pygame.display.update()

