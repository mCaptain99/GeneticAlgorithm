SELECTIONS = ["BEST", "ROULETTE", "TOURNAMENT"]
CROSS = ["ARITHMETIC", "BLEND_ALPHA", "BLEND_ALPHA_BETA", "LINEAR", "AVERAGE"]
MUTATION = ["UNIFORM", "GAUSS"]


def goldstein_prize(x1, x2):
    part1 = (1 + (x1 + x2 + 1) ** 2 * (19 - 14 * x1 + 3 * x1 * x1 - 14 * x2 + 6 * x1 * x2 + 3 * x2 * x2))
    part2 = (30 + (2 * x1 - 3 * x2) ** 2 * (18 - 32 * x1 + 12 * x1 * x1 + 48 * x2 - 36 * x1 * x2 + 27 * x2 * x2))
    return part1 * part2


class Singleton:
    def __init__(self, cls):
        self.cls = cls
        self.obj = None

    def __call__(self, *args, **kwargs):
        if not self.obj:
            self.obj = self.cls(*args, **kwargs)
        return self.obj

    def set(self, **kwargs):
        self.obj = self.cls(**kwargs)


@Singleton
class GlobalData:
    def __init__(self, begin_range, end_range, population_amount, function=goldstein_prize):
        self.begin_range = begin_range
        self.end_range = end_range
        self.function = function
        self.population_amount = population_amount
