import numpy as np


class Singleton:
    def __init__(self, cls):
        self.cls = cls
        self.obj = None

    def __call__(self, *args, **kwargs):
        if not self.obj:
            self.obj = self.cls(*args, **kwargs)
        return self.obj

    def set(self, begin_range, end_range, amount, precision):
        self.obj = self.cls(begin_range, end_range, amount, precision)


@Singleton
class Converter:
    def __init__(self, begin_range, end_range, amount, precision=6):
        self.begin_range = begin_range
        self.end_range = end_range
        self.amount = amount
        self.length = np.ceil(np.log2((end_range - begin_range) * (10 ** precision)))

    def to_bin(self, num):
        num = int((num - self.begin_range) * (2**self.length - 1) / (self.end_range - self.begin_range))
        return self._to_bin(num, self.length)

    def to_dec(self, bin_representation):
        num = self._to_dec(bin_representation)
        return num * (self.end_range - self.begin_range) / (2**self.length - 1) + self.begin_range

    def _to_bin(self, num, m):
        bin_representation = []
        while num != 0:
            bit = int(num % 2)
            bin_representation.append(bit)
            num = num // 2
        bin_representation.reverse()
        while len(bin_representation) != m:
            bin_representation.insert(0, 0)
        return bin_representation

    def _to_dec(self, bin_representation):
        dec = 0
        for bit in bin_representation[1:]:
            dec = (dec << 1) | bit
        return dec
