import copy
import logging
import random

import numpy as np

from oe.data import GlobalData
from oe.model.chromosome import Chromosome
from oe.model.chromosome_pair import ChromosomePair


def validate_value_in_range_after_crossing(f):
    def wrapper(*args, **kwargs):
        while True:
            results = f(*args, **kwargs)
            for value in results:
                if GlobalData().begin_range <= value <= GlobalData().end_range:
                    return results

    return wrapper


class Population:
    transformations = {
        'UNIFORM': ChromosomePair.uniform_mutation,
        'GAUSS': ChromosomePair.gauss_mutation,
    }

    def __init__(self, chromosome_pairs: list[ChromosomePair],
                 mutation_method='ONE_POINT_MUTATION',
                 cross_method='ONE_POINT',
                 selection_method='ROULETTE',
                 cross_probability=0.5,
                 mutation_probability=0.5,
                 inversion_probability=0.5,
                 selection_percent=50,
                 maximalization=False):
        self.chromosome_pairs = chromosome_pairs
        self.new_generation = []
        self.mutation_method = mutation_method
        self.cross_method = cross_method
        self.selection_method = selection_method
        self.cross_probability = cross_probability
        self.mutation_probability = mutation_probability
        self.selection_percent = selection_percent
        self.inversion_probability = inversion_probability
        self.maximalization = maximalization
        self.sort()
        self.elite = self.chromosome_pairs[:selection_percent // 100 * self.population_size]
        self.next_gen = []

    def mutation(self):
        self._execute_transformation_with_given_probability(self.mutation_probability, self.mutation_method)

    def cross(self):
        self.next_gen = []
        while len(self.next_gen) < self.population_size:
            if np.random.random_sample() <= self.cross_probability:
                children = self._cross()
                self.next_gen.extend(children)
        self.next_gen = self.next_gen[:self.population_size - 1]

    def selection(self):
        if self.selection_method == 'BEST':
            self.elite = self._best_selection()
        elif self.selection_method == 'ROULETTE':
            self.elite = self._roulette_selection()
        elif self.selection_method == 'TOURNAMENT':
            self.elite = self._tournament_selection()

    def epoch(self):
        self._store_best_chromosomes()
        self.selection()
        self.cross()
        self.mutation()
        self.chromosome_pairs = self.next_gen
        self.chromosome_pairs.append(self.best)

    @property
    def population_size(self):
        return len(self.chromosome_pairs)

    def _store_best_chromosomes(self):
        selector = max if self.maximalization else min
        best = selector(self.chromosome_pairs)
        best_copy = copy.deepcopy(best)
        self.best = best_copy

    def _execute_transformation_with_given_probability(self, probability, transformation):
        for chromosome_pair in self.next_gen:
            if np.random.random_sample() <= probability:
                logging.debug("{} chromosomes {}".format(transformation, chromosome_pair))
                self.transformations[transformation](chromosome_pair)

    def _get_random_pair_for_crossing(self, chromosome_index=0) -> tuple[Chromosome, Chromosome]:
        index1 = np.random.randint(0, len(self.elite))
        index2 = np.random.randint(0, len(self.elite))
        return self.elite[index1][chromosome_index], self.elite[index2][chromosome_index]

    def _cross(self):
        parent_11, parent_12 = self._get_random_pair_for_crossing(chromosome_index=0)
        parent_21, parent_22 = self._get_random_pair_for_crossing(chromosome_index=1)
        child_11, child_12, child_21, child_22 = None, None, None, None
        if self.cross_method == 'ARITHMETIC':
            child_11, child_12, child_21, child_22 = self._arithmetic_cross(parent_11, parent_12, parent_21, parent_22)
        elif self.cross_method == 'BLEND_ALPHA':
            child_11, child_12, child_21, child_22 = self._blend_cross_alpha(parent_11, parent_12, parent_21, parent_22)
        elif self.cross_method == 'BLEND_ALPHA_BETA':
            child_11, child_12, child_21, child_22 = self._blend_cross_alpha_beta(parent_11, parent_12, parent_21,
                                                                                  parent_22)
        elif self.cross_method == 'AVERAGE':
            child_11, child_12, child_21, child_22 = self._average_cross(parent_11, parent_12, parent_21, parent_22)
        elif self.cross_method == 'LINEAR':
            child_11, child_12, child_21, child_22 = self._linear_cross(parent_11, parent_12, parent_21, parent_22)
        return ChromosomePair(Chromosome(child_11), Chromosome(child_21)), \
               ChromosomePair(Chromosome(child_12), Chromosome(child_22))

    @validate_value_in_range_after_crossing
    def _arithmetic_cross(self, parent_11, parent_12, parent_21, parent_22):
        k = random.random()
        child_11 = k * parent_11.value + (1 - k) * parent_12.value
        child_12 = k * parent_12.value + (1 - k) * parent_11.value
        child_21 = k * parent_21.value + (1 - k) * parent_22.value
        child_22 = k * parent_22.value + (1 - k) * parent_21.value
        return child_11, child_12, child_21, child_22

    @validate_value_in_range_after_crossing
    def _blend_cross_alpha(self, parent_11, parent_12, parent_21, parent_22):
        d1, d2 = abs(parent_11.value - parent_12.value), abs(parent_21.value - parent_22.value)
        alpha = random.random()
        child_11 = random.uniform(min(parent_11.value, parent_12.value) - alpha * d1,
                                  max(parent_11.value, parent_12.value) + alpha * d1)
        child_12 = random.uniform(min(parent_11.value, parent_12.value) - alpha * d1,
                                  max(parent_11.value, parent_12.value) + alpha * d1)
        child_21 = random.uniform(min(parent_21.value, parent_22.value) - alpha * d2,
                                  max(parent_21.value, parent_22.value) + alpha * d2)
        child_22 = random.uniform(min(parent_21.value, parent_22.value) - alpha * d2,
                                  max(parent_21.value, parent_22.value) + alpha * d2)
        return child_11, child_12, child_21, child_22

    @validate_value_in_range_after_crossing
    def _blend_cross_alpha_beta(self, parent_11, parent_12, parent_21, parent_22):
        d1, d2 = abs(parent_11.value - parent_12.value), abs(parent_21.value - parent_22.value)
        alpha, beta = random.random(), random.random()
        child_11 = random.uniform(min(parent_11.value, parent_12.value) - alpha * d1,
                                  max(parent_11.value, parent_12.value) + beta * d1)
        child_12 = random.uniform(min(parent_11.value, parent_12.value) - alpha * d1,
                                  max(parent_11.value, parent_12.value) + beta * d1)
        child_21 = random.uniform(min(parent_21.value, parent_22.value) - alpha * d2,
                                  max(parent_21.value, parent_22.value) + beta * d2)
        child_22 = random.uniform(min(parent_21.value, parent_22.value) - alpha * d2,
                                  max(parent_21.value, parent_22.value) + beta * d2)
        return child_11, child_12, child_21, child_22

    @validate_value_in_range_after_crossing
    def _average_cross(self, parent_11, parent_12, parent_21, parent_22):
        child_11 = np.average((parent_11.value, parent_12.value))
        child_21 = np.average((parent_21.value, parent_22.value))
        child_12 = np.average((parent_11.value, parent_12.value))
        child_22 = np.average((parent_21.value, parent_22.value))
        return child_11, child_12, child_21, child_22

    @validate_value_in_range_after_crossing
    def _linear_cross(self, parent_11, parent_12, parent_21, parent_22):
        z_x, z_y = (1 / 2) * parent_11.value + (1 / 2) * parent_12.value, (1 / 2) * parent_21.value + (
                    1 / 2) * parent_22.value
        v_x, v_y = (3 / 2) * parent_11.value - (1 / 2) * parent_12.value, (3 / 2) * parent_21.value - (
                    1 / 2) * parent_22.value
        w_x, w_y = (-1 / 2) * parent_11.value + (3 / 2) * parent_12.value, (-1 / 2) * parent_21.value + (
                    3 / 2) * parent_22.value
        res = [z_x, z_y, v_x, v_y, w_x, w_y]
        eliminator = min if self.maximalization else max
        function = GlobalData().function
        weakest = eliminator(
            ((z_x, z_y), function(z_x, z_y)),
            ((v_x, v_y), function(v_x, v_y)),
            ((w_x, w_y), function(w_x, w_y)), key=lambda x: x[1])
        res.remove(weakest[0][0])
        res.remove(weakest[0][1])
        return tuple(res)

    def _get_pairs_and_function_values(self):
        return [(chromosome_pair, chromosome_pair.get_function_value())
                for chromosome_pair in self.chromosome_pairs]

    def _get_pairs_and_probabilities(self):
        pairs_and_values = self._get_pairs_and_function_values()
        if not self.maximalization:
            pairs_and_values = [(x[0], 1 / x[1]) for x in pairs_and_values]
        sum_of_function_values = sum([x[1] for x in pairs_and_values])
        return sorted([(x[0], x[1] / sum_of_function_values) for x in pairs_and_values], key=lambda x: x[1])

    def _get_pairs_and_distribuants(self):
        pairs_and_distribuants = []
        pairs_and_probabilities = self._get_pairs_and_probabilities()
        previous_prob = 0
        for pair, probability in pairs_and_probabilities:
            pairs_and_distribuants.append((pair, probability + previous_prob))
            previous_prob = probability
        return pairs_and_distribuants

    def _best_selection(self):
        sorted_results = sorted(self._get_pairs_and_function_values(), key=lambda x: x[1])
        sorted_population = [x[0] for x in sorted_results]
        if self.maximalization:
            return sorted_population[
                   self.population_size - self.population_size * self.selection_percent // 100:]
        else:
            return sorted_population[:self.population_size * self.selection_percent // 100]

    def _fit_in_interval(self, pairs_and_distribuants, value):
        previous = pairs_and_distribuants[0][0]
        for chromosome_pair, distribuant in pairs_and_distribuants:
            if value > distribuant:
                previous = chromosome_pair
            else:
                break
        return previous

    def _roulette_selection(self):
        new_population = []
        rand_numbers = np.random.rand(self.selection_percent * self.population_size // 100)
        pairs_and_distribuants = self._get_pairs_and_distribuants()
        for i in range(self.selection_percent * self.population_size // 100):
            new_population.append(self._fit_in_interval(pairs_and_distribuants, rand_numbers[i]))
        return new_population

    def _tournament_selection(self):
        tournament_number = self.population_size // (100 // self.selection_percent)
        tournament_size = self.population_size // tournament_number
        pairs_and_values = self._get_pairs_and_function_values()
        random.shuffle(pairs_and_values)
        winners = []
        for i in range(tournament_number):
            if self.maximalization:
                winners.append(
                    max(pairs_and_values[i * tournament_size: (i + 1) * tournament_size], key=lambda x: x[1]))
            else:
                winners.append(
                    min(pairs_and_values[i * tournament_size: (i + 1) * tournament_size], key=lambda x: x[1]))
        return [winner[0] for winner in winners]

    def __repr__(self):
        return str([repr(chp) for chp in self.chromosome_pairs])

    def __getitem__(self, index):
        return self.chromosome_pairs[index]

    def sort(self):
        self.chromosome_pairs.sort(key=lambda x: x.get_function_value())
        if self.maximalization:
            self.chromosome_pairs.reverse()

    def trim(self, max_size):
        self.sort()
        old_generation_size = max_size - len(self.next_gen) if max_size - len(self.next_gen) > 0 else 1
        self.chromosome_pairs = self.chromosome_pairs[:old_generation_size] + self.next_gen[:max_size]
