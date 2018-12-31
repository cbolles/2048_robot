from game_objects import Game
import os
from pathlib import Path
from users.genetic_bot import GeneticBot


def main():
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    config_path = str(current_dir / 'resources' / 'config' / 'basic_ui.ini')
    game = Game(config_path)
    dna = {
        'merges_weight': 10,
        'height_largest_weight': 0,
        'height_lowest_weight': 0,
        'height_average_weight': 0,
        'num_discontinuities_weight': -5,
        'num_discards_weight': 0
    }
    user = GeneticBot(config_path, game, dna_init=dna)
    user.run()


if __name__ == '__main__':
    main()
