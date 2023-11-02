from oe.data import GlobalData
from oe.model.chromosome import Chromosome


class ChromosomePair:
    def __init__(self, chromosome1: Chromosome, chromosome2: Chromosome):
        self.chromosome1 = chromosome1
        self.chromosome2 = chromosome2

    def uniform_mutation(self):
        self.chromosome1.uniform_mutation()
        self.chromosome2.uniform_mutation()

    def gauss_mutation(self):
        self.chromosome1.gauss_mutation()
        self.chromosome2.gauss_mutation()

    def get_function_value(self):
        return GlobalData().function(self.chromosome1.value, self.chromosome2.value)

    def __getitem__(self, index):
        if index == 0:
            return self.chromosome1
        elif index == 1:
            return self.chromosome2

    def __repr__(self):
        function = GlobalData().function
        return " [" + repr(self.chromosome1.value) + " ; " + repr(self.chromosome2.value) + "] --> " + \
               str(self.get_function_value())

    def __le__(self, other):
        return self.get_function_value() <= other.get_function_value()

    def __ge__(self, other):
        return self.get_function_value() >= other.get_function_value()

    def __lt__(self, other):
        return self.get_function_value() < other.get_function_value()

    def __gt__(self, other):
        return self.get_function_value() > other.get_function_value()
