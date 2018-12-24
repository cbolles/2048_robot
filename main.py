import pygame
from game_objects import Tile, Stack, TileQueue


# Default Values
SIZE = (1200, 800)
NUM_STACKS = 4

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("2048 Solitaire")

# Game Objects
stacks = []
tile_queue = TileQueue(20, 650)

# Test values
test_tiles = [Tile(2), Tile(4), Tile(8)]


def generate_stacks(startX, startY):
    stackX = startX
    stackY = startY
    distance = SIZE[0] // NUM_STACKS
    for i in range(0, NUM_STACKS):
        stacks.append(Stack(stackX, stackY))
        stackX += distance
        # Test stacks
        stacks[i].add_tile(test_tiles)


def main():
    # Initalize Game Objects
    generate_stacks(0, 20)
    running = True
    while running:
        # Listen for quite request from user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for stack in stacks:
            stack.draw(screen)
        tile_queue.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
