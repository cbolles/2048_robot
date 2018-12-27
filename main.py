import pygame
from game_objects import Tile, Stack, TileQueue, ScoreDisplay


# Default Values
SIZE = (1200, 800)
NUM_STACKS = 4
FONT_SIZE = 30
FRAMERATE = 10

# Initialize Pygame
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', FONT_SIZE)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("2048 Solitaire")
clock = pygame.time.Clock()

# Game Objects
stacks = []
tile_queue = TileQueue(60, 650)
score_display = ScoreDisplay(1000, 0, font)

# Test values
test_tiles = [Tile(8), Tile(4), Tile(2)]


def generate_stacks(startX, startY):
    stackX = startX
    stackY = startY
    distance = SIZE[0] // NUM_STACKS
    for i in range(0, NUM_STACKS):
        stacks.append(Stack(stackX, stackY))
        stackX += distance
        # Test stacks
        stacks[i].add_tile(test_tiles)


def update_game_objects():
    screen.fill((0, 0, 0))
    for stack in stacks:
        stack.draw(screen)
    tile_queue.draw(screen)
    score_display.draw(screen)
    pygame.display.flip()


def stack_change(mouse_x, mouse_y):
    print(mouse_x, mouse_y)
    for stack in stacks:
        if stack.collision_box.collidepoint(mouse_x, mouse_y):
            score_change = stack.add_tile(tile_queue.pull())
            print(score_change)
            score_display.increase_score(score_change)
            update_game_objects()
            return


def main():
    # Initalize Game Objects
    generate_stacks(0, 20)
    running = True
    update_game_objects()
    while running:
        # Listen for quite request from user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                stack_change(mouse_x, mouse_y)
        clock.tick(FRAMERATE)


if __name__ == '__main__':
    main()
