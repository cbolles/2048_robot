import pygame
from twenty.controller import GameController
from twenty.user import User, HumanUser


def main():
    """
    Main entry point for the game.
    """
    initial_state = [
        [0, 0, 0, 2],
        [0, 0, 0, 0],
        [0, 2, 0, 0],
        [0, 0, 0, 0],
    ]
    user = HumanUser()
    controller = GameController(initial_state, user)
    controller.run()


if __name__ == "__main__":
    main()
