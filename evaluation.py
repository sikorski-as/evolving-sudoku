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
