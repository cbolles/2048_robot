import os
from pathlib import Path
from users.genetic_bot import GeneticBot
from users.basic_bot import BasicBot
from users.human import Human
from users.genetic_bot import GeneticBot
from ai_training.genetic_training import training


def main():
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    config_path = str(current_dir / 'resources' / 'config' / 'base_config.ini')
    params = dict()
    dna = {
        'merges_weight': 20,
        'height_largest_weight': 0,
        'height_lowest_weight': 0,
        'height_average_weight': 0,
        'num_discontinuities_weight': -5,
        'num_discards_weight': 0,
        'fill_ratio_weight': 5
    }
    params['game_display'] = True
    # params['dna_init'] = dna
    # user = BasicBot(config_path, params)
    # user = Human(config_path)
    # user = GeneticBot(config_path, params)
    # user.run()
    # print(user.user_stats.user_score)
    training(params)

if __name__ == '__main__':
    main()
