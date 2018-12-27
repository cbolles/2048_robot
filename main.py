from game_objects import Game
import os
from pathlib import Path
from users import Human


def main():
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    config_path = str(current_dir / 'resources' / 'config' / 'basic_ui.ini')
    game = Game(config_path)
    human = Human(config_path, game)
    human.run()


if __name__ == '__main__':
    main()
