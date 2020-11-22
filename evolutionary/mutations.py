import random

import numpy as np

from evolutionary import chromosome

ranges = [[0, 3], [3, 6], [6, 9]]


def random_9_square(ind):
    """
    With given probability generates random 3x3 square with 1-9 numbers
    :param ind: individual to be mutated
    """
    prob = 75
    ranges = [[0, 3], [3, 6], [6, 9]]
    for xbegin, xend in ranges:
        for ybegin, yend in ranges:
            if prob > random.randint(1, 100):
                ind.sudoku[xbegin:xend, ybegin:yend] = np.random.permutation(range(1, 10)).reshape((3, 3))
    chromosome.set_back_starting_points(ind)
