from twenty.view import GameView
import pygame


def main():
    """
    Main entry point for the game.
    """
    screen = pygame.display.set_mode((400, 400))
    pygame.init()
    game = GameView(screen)
    game.draw()

    while True:
        event = pygame.key.get_pressed()
        if event[pygame.KEYDOWN]:
            break


if __name__ == "__main__":
    main()
