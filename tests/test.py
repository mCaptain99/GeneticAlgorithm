import numpy as np

from oe.data import GlobalData
from oe.model.population import Population
from oe.tests import test_config
from oe.utils.generator import Generator


def execute_genetic_algorithm(begin_range=-10, end_range=10, population_amount=100,
                              epochs=20, **parameters):
    population_generator = Generator(population_amount, begin_range, end_range)
    chromosome_pairs = population_generator.get_population()
    population = Population(chromosome_pairs, **parameters)
    for i in range(epochs):
        population.epoch()
    return population.best.get_function_value()


def make_test(comment='', begin_range=-10, end_range=10, population_amount=100,
              test_number=20, epochs=70, **parameters):
    print(f'  {comment}')
    GlobalData.set(begin_range=begin_range, end_range=end_range, population_amount=population_amount)
    results = []
    for i in range(test_number):
        results.append(execute_genetic_algorithm(begin_range=begin_range, end_range=end_range,
                                                 population_amount=population_amount, epochs=epochs, **parameters))
    print(f'    Srednia: {np.mean(results)}, Mediana: {np.median(results)}\n')


if __name__ == '__main__':
    print('Porównanie prawdopo  doobieństwa selekcji:')
    make_test(comment='Wysoki procent selekcji (90):', **test_config.high_cross)
    make_test(comment='Niski procent selekcji (20):', **test_config.low_cross)

    print('Porównanie procentu mutacji:')
    make_test(comment='Wysokie prawdopodobienstwo mutacji: (0.8)', **test_config.high_mutation)
    make_test(comment='Niskie prawdopodobienstwo mutacji: (0.1)', **test_config.low_mutation)

    print('Porównanie metod krzyzowania:')
    make_test(comment='Krzyzowanie arytmetyczne', **test_config.arithmetic_cross)
    make_test(comment='Krzyzowanie mieszajace alfa', **test_config.blend_alpha_cross)
    make_test(comment='Krzyzowanie mieszajace alfa beta', **test_config.blend_alpha_beta_cross)
    make_test(comment='Krzyzowanie usredniajace', **test_config.average_cross)
    make_test(comment='Krzyzowanie linearne', **test_config.linear_cross)

    print('Porównanie metod seleckji:')
    make_test(comment='Seleckja najlepszych', **test_config.best_selection)
    make_test(comment='Selekcja turniejowa', **test_config.tournament_selection)
    make_test(comment='Seleckja ruletki', **test_config.roulette_selection)

    print('Porównanie metod mutacji:')
    make_test(comment='Mutacja jednorodna', **test_config.uniform_mutation)
    make_test(comment='Mutacja gaussa', **test_config.gauss_mutation)

    print('Wpływ liczby epok:')
    make_test(comment='Liczba epok: 200', epochs=200, **test_config.default)
    make_test(comment='Liczba epok: 20', epochs=20, **test_config.default)

    print('Wpływ wielkości populacji:')
    make_test(comment='Liczba osobnikow: 400', population_amount=400, **test_config.default)
    make_test(comment='Liczba osobnikow: 40', population_amount=40, **test_config.default)

