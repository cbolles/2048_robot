from users.genetic_bot import GeneticBot
from game_objects import Game
from random import randint, randrange
from configparser import ConfigParser
import os
from pathlib import Path


class GeneticConfig:
    def __init__(self, config_path):
        config_parser = ConfigParser()
        config_parser.read(config_path)
        raw_config = config_parser['Genetic']
        self.population_size = int(raw_config['population_size'])
        self.num_parents = int(raw_config['num_parents'])
        self.mutation_rate = float(raw_config['mutation_rate'])
        self.mutation_step = float(raw_config['mutation_step'])
        self.target_score = int(raw_config['target_score'])


class Generation:
    def __init__(self, game_config_path, genetic_config, number, parents=None):
        self.game_config_path = game_config_path
        self.genetic_config = genetic_config
        self.bots = []
        self.number = number
        self.initialize_population(parents)

    def initialize_original_population(self):
        for i in range(0, self.genetic_config.population_size):
            game = Game(self.game_config_path)
            self.bots.append(GeneticBot(self.game_config_path, game))

    def get_parent(self, parents):
        if len(parents) == 1:
            return parents[0]
        prob = randint(0, 100)
        split_point = len(parents) // 2
        if prob < 75:
            return self.get_parent(parents[split_point:])
        return self.get_parent(parents[:split_point])

    def produce_offspring(self, parent_one, parent_two):
        dna_params = dict()
        parent_one_dna = parent_one.dna.__dict__
        parent_two_dna = parent_two.dna.__dict__

        # Generate from parents
        for key, value in parent_one_dna.items():
            prob = randint(0, 1)
            if prob == 0:
                dna_params[key] = value
            else:
                dna_params[key] = parent_two_dna[key]
        # Mutate
        for key in dna_params:
            prob = randint(0, 100)
            if prob <= self.genetic_config.mutation_rate:
                mutation_change = self.genetic_config.mutation_step * randrange(-1, 2, 2)
                dna_params[key] = dna_params[key] + mutation_change
        return GeneticBot(self.game_config_path, Game(self.game_config_path), dna_init=dna_params)

    def produce_generation(self, parents):
        parents = sorted(parents, key=lambda parent: parent.fitness)
        while len(self.bots) < self.genetic_config.population_size:
            parent_one = self.get_parent(parents)
            parent_two = self.get_parent(parents)
            while parent_two.fitness == parent_one.fitness:
                parent_two = self.get_parent(parents)
            self.bots.append(self.produce_offspring(parent_one, parent_two))

    def initialize_population(self, parents):
        if parents is None:
            self.initialize_original_population()
        else:
            self.produce_generation(parents)

    def evaluate_fitness(self):
        for bot in self.bots:
            bot.evaluate_fitness()

    def get_most_fit(self):
        return sorted(self.bots, key=lambda bot: bot.fitness)[-1]


def display_gen_details(population):
    most_fit = population.get_most_fit()
    print('Gen: ' + str(population.number))
    print('Score: ' + str(most_fit.fitness))
    print(population.get_most_fit().dna)


def training(params: dict) -> None:
    # Read in genetic configuration
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    genetic_config_path = str(current_dir / '..' / 'resources' / 'config' / 'genetic_training.ini')
    print(genetic_config_path)
    genetic_config = GeneticConfig(genetic_config_path)

    # Read in game configuration
    game_config_path = str(current_dir / '..' / 'resources' / 'config' / 'basic_ui.ini')

    # Establish first generation
    gen_number = 0
    population = Generation(game_config_path, genetic_config, gen_number)
    population.evaluate_fitness()

    display_gen_details(population)

    # Training loop
    while population.get_most_fit().fitness < genetic_config.target_score:
        gen_number += 1
        population = Generation(game_config_path, genetic_config, gen_number, parents=population.bots)
        population.evaluate_fitness()
        display_gen_details(population)
