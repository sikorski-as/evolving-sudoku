import random
from copy import copy

import numpy as np


def swap_rows(ind1, ind2):
    begin, end = 3, 6
    part1 = copy(ind1.sudoku[begin:end, :])
    part2 = copy(ind2.sudoku[begin:end, :])
    ind1.sudoku[begin:end, :], ind2.sudoku[begin:end, :] = part2, part1
    return ind1, ind2


ranges = [[0, 3], [3, 6], [6, 9]]
squares = [(x, y) for x in ranges for y in ranges]


def swap_squares(ind1, ind2, n=3):
    chosen_squares = random.sample(squares, k=n)
    for (xbegin, xend), (ybegin, yend) in chosen_squares:
        square1 = copy(ind1.sudoku[xbegin:xend, ybegin:yend])
        square2 = copy(ind2.sudoku[xbegin:xend, ybegin:yend])
        ind1.sudoku[xbegin:xend, ybegin:yend] = square2
        ind2.sudoku[xbegin:xend, ybegin:yend] = square1
    return ind1, ind2