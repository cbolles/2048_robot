from users.genetic_bot import GeneticBot
from game_objects import Game
from random import randint


class GeneticConfig:
    def __init__(self, population_size, num_parents, mutation_rate, mutation_step):
        self.population_size = population_size
        self.num_parents = num_parents
        self.mutation_rate = mutation_rate
        self.mutation_step = mutation_step


class Generation:
    def __init__(self, size, config_path, genetic_config, parents=None):
        self.config_path = config_path
        self.genetic_config = genetic_config
        self.bots = []
        self.initialize_population(parents)

    def initialize_original_population(self):
        for i in range(0, self.genetic_config.population_size):
            game = Game(self.config_path)
            self.bots.append(GeneticBot(self.config_path, game))

    def get_parent(self, parents):
        if len(parents) == 1:
            return parents[0]
        prob = randint(0, 99)
        split_point = len(parents) // 2
        if prob < 65:
            return self.get_parent(parents[:split_point])
        return self.get_parent(parents[split_point:])

    def produce_offspring(self, parent_one, parent_two):
        pass

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
    
