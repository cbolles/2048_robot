from game_objects import Game
import os
from pathlib import Path
from users.basic_bot import BasicBot
from users.human import Human


def main():
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    config_path = str(current_dir / 'resources' / 'config' / 'base_config.ini')
    params = dict()
    params['game_display'] = True
    user = BasicBot(config_path, params)
    # user = Human(config_path)
    user.run()
    print(user.user_stats.user_score)


if __name__ == '__main__':
    main()
