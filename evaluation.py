from typing import Tuple

import numpy as np

from evolutionary.chromosome import Chromosome


def check_repetitions(row) -> int:
    """
    :param row to be checked
    :return: amount of number repetitions in row
    """
    numbers = set()
    for el in row:
        numbers.add(el)
    # it can be slightly optimised by replacing the above with np.unique

    return 9 - len(numbers)


def validate_chromosome(chromosome: Chromosome) -> Tuple[int]:
    return _validate(chromosome.sudoku),


def _validate(sudoku: np.ndarray) -> int:
    """
        Checks if sudoku is correctly solved
        :param sudoku instance
        :return: Number of collisions if any
    """

    xlen, ylen = sudoku.shape

    total_repetitions: int = 0
    for i in range(xlen):
        total_repetitions += check_repetitions(sudoku[i, :])

    for j in range(ylen):
        total_repetitions += check_repetitions(sudoku[:, j])

    ranges = [[0, 3], [3, 6], [6, 9]]
    for xbegin, xend in ranges:
        for ybegin, yend in ranges:
            square: np.ndarray = sudoku[xbegin:xend, ybegin:yend]
            total_repetitions += check_repetitions(square.flatten())

    return total_repetitions


_NINE_FACTORIAL = 9 * 8 * 7 * 6 * 5 * 4 * 3 * 2 * 1


def validate_chromosome_extended(chromosome: Chromosome) -> Tuple[int]:
    sudoku = chromosome.sudoku

    cols_sum = np.sum(np.abs(np.sum(sudoku, axis=0) - 45))
    rows_sum = np.sum(np.abs(np.sum(sudoku, axis=1) - 45))
    cols_prod = np.sum(np.sqrt(np.abs(np.product(sudoku, axis=0) - _NINE_FACTORIAL)))
    rows_prod = np.sum(np.sqrt(np.abs(np.product(sudoku, axis=1) - _NINE_FACTORIAL)))
    cols_miss = 9 - len(np.unique(sudoku, axis=0))
    rows_miss = 9 - len(np.unique(sudoku, axis=1))

    return 10 * (cols_sum + rows_sum) + cols_prod + rows_prod + 50 * (cols_miss + rows_miss),
