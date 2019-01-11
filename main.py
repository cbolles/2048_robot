from game_objects import Game
import os
from pathlib import Path
from users.human import Human


def main():
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    config_path = str(current_dir / 'resources' / 'config' / 'base_config.ini')
    print(config_path)
    user = Human(config_path)
    user.run()


if __name__ == '__main__':
    main()
