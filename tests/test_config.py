from oe.data import goldstein_prize

default = {'mutation_method': 'GAUSS',
           'cross_method': 'ARITHMETIC',
           'selection_method': 'BEST',
           'cross_probability': 0.5,
           'mutation_probability': 0.4,
           'selection_percent': 50,
           'maximalization': False}

high_cross = default.copy()
high_cross['selection_percent'] = 90
high_cross['cross_probability'] = 0.9

low_cross = default.copy()
low_cross['selection_percent'] = 20
low_cross['cross_probability'] = 0.2

high_mutation = default.copy()
high_mutation['mutation_probability'] = 0.8

low_mutation = default.copy()
low_mutation['mutation_probability'] = 0.1

arithmetic_cross = default.copy()

blend_alpha_cross = default.copy()
blend_alpha_cross['cross_method'] = 'BLEND_ALPHA'

blend_alpha_beta_cross = default.copy()
blend_alpha_beta_cross['cross_method'] = 'BLEND_ALPHA_BETA'

average_cross = default.copy()
average_cross['cross_method'] = 'AVERAGE'

linear_cross = default.copy()
linear_cross['cross_method'] = 'LINEAR'

best_selection = default.copy()
tournament_selection = default.copy()
tournament_selection['selection_method'] = 'TOURNAMENT'
roulette_selection = default.copy()
roulette_selection['selection_method'] = 'ROULETTE'

gauss_mutation = default.copy()
uniform_mutation = default.copy()
uniform_mutation['mutation_method'] = 'UNIFORM'

