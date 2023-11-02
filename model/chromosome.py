import random

import numpy as np

from oe.data import GlobalData


class Chromosome:
    _value = None

    def __init__(self, value):
        self.value = value

    def uniform_mutation(self):
        self.value = random.uniform(GlobalData().begin_range, GlobalData().end_range)

    def gauss_mutation(self):
        while True:
            self.value = self.value + np.random.normal()
            if GlobalData().begin_range <= self.value <= GlobalData().end_range:
                break

    def __repr__(self):
        return ''.join([str(i) for i in self.value])
