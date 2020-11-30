import random

import numpy as np

from evolutionary import chromosome

ranges = [[0, 3], [3, 6], [6, 9]]


def random_9_square(ind):
    """
    With given probability generates random 3x3 square with 1-9 numbers
    :param ind: individual to be mutated
    """
    prob = 10
    ranges = [[0, 3], [3, 6], [6, 9]]
    for xbegin, xend in ranges:
        for ybegin, yend in ranges:
            if prob > random.randint(1, 100):
                available_numbers = set(range(1, 10))
                static_points = []
                for x, y in ind.starting_points:
                    if xbegin <= x < xend and ybegin <= y < yend:
                        static_points.append((x, y))
                        available_numbers.remove(ind.sudoku_instance[x, y])
                random_numbers = list(np.random.permutation(list(available_numbers)))
                for x in range(xbegin, xend):
                    for y in range(ybegin, yend):
                        if (x, y) not in static_points:
                            ind.sudoku[x, y] = random_numbers.pop()
                        else:
                            ind.sudoku[x, y] = ind.sudoku_instance[x, y]
