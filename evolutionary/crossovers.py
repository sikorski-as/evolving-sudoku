import random
from copy import copy

import numpy as np


def swap_columns(ind1, ind2):
    begin, end = random.choice(ranges)
    part1 = copy(ind1.sudoku[:, begin:end])
    part2 = copy(ind2.sudoku[:, begin:end])
    ind1.sudoku[:, begin:end], ind2.sudoku[:, begin:end] = part2, part1
    return ind1, ind2


def swap_rows(ind1, ind2):
    begin, end = random.choice(ranges)
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


def swap_using_score(ind1, ind2):
    """
    Child1 takes best rows, child2 takes best columns.
    Score -> number of unique number in column
    3x3 subblocks are taken into consideration
    :param ind1:
    :param ind2:
    :return:
    """
    child1, child2 = np.zeros((9, 9), dtype=int), np.zeros((9, 9), dtype=int)
    for sub_row in ranges:
        first_score, second_score = 0, 0
        for row in range(sub_row[0], sub_row[1]):
            first_score += calculate_score(ind1.sudoku[row, :])
            second_score += calculate_score(ind2.sudoku[row, :])
        child1[sub_row[0]:sub_row[1], :] = ind1.sudoku[sub_row[0]:sub_row[1], :] if first_score > second_score else ind2.sudoku[sub_row[0]:sub_row[1], :]

    for sub_col in ranges:
        first_score, second_score = 0, 0
        for col in range(sub_col[0], sub_col[1]):
            first_score += calculate_score(ind1.sudoku[:, col])
            second_score += calculate_score(ind2.sudoku[:, col])
        child2[:, sub_col[0]:sub_col[1]] = ind1.sudoku[:, sub_col[0]:sub_col[1]] if first_score > second_score else ind2.sudoku[:, sub_col[0]:sub_col[1]]

    ind1.sudoku = child1
    ind2.sudoku = child2


def calculate_score(number_list: np.array) -> int:
    return len(set(number_list))
