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
        'merges_weight': 0.1539,
        'height_largest_weight': -0.327,
        'height_lowest_weight': -0.40303,
        'height_average_weight': -0.5604,
        'num_discontinuities_weight': -.57822,
        'num_discards_weight': -0.5994,
        'fill_ratio_weight': -1.0833
    }
    params['game_display'] = True
    # params['dna_init'] = dna
    user = BasicBot(config_path, params)
    # user = Human(config_path)
    # user = GeneticBot(config_path, params)
    user.run()
    print(user.user_stats.user_score)
    # training(params)


if __name__ == '__main__':
    main()
