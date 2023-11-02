import random

from oe.model.chromosome import Chromosome
from oe.model.chromosome_pair import ChromosomePair


class Generator:
    def __init__(self, amount, x1, x2):
        self.amount = amount
        self.x1 = x1
        self.x2 = x2

    @staticmethod
    def get_random_tuple(x1, x2):
        return random.uniform(x1, x2), random.uniform(x1, x2)

    def get_population(self):
        population = []
        for item in range(self.amount):
            ch1, ch2 = self.get_random_tuple(self.x1, self.x2)
            population.append(ChromosomePair(Chromosome(ch1),
                                             Chromosome(ch2)))

        return population