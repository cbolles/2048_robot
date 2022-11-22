import pygame
from twenty.controller import GameController
from twenty.user import User, HumanUser
from twenty.training.train import train


def main():
    """
    Main entry point for the game.
    """

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
    """

    train()




if __name__ == "__main__":
    main()
