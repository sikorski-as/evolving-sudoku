import random
from copy import copy, deepcopy


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

slices = [slice(0, 3), slice(3, 6), slice(6, 9)]
square_slices = [(x, y) for x in slices for y in slices]


def swap_squares(ind1, ind2, n=3):
    chosen_squares = random.sample(square_slices, k=n)
    for x_slice, y_slice in chosen_squares:
        ind1.sudoku[x_slice, y_slice], ind2.sudoku[x_slice, y_slice] = \
            ind2.sudoku[x_slice, y_slice], ind1.sudoku[x_slice, y_slice]
    return ind1, ind2


def swap_squares_uniform(ind1, ind2, prob_for_each_gene=0.5):
    for x_slice, y_slice in square_slices:
        if random.random() < prob_for_each_gene:
            ind1.sudoku[x_slice, y_slice], ind2.sudoku[x_slice, y_slice] = \
                ind2.sudoku[x_slice, y_slice], ind1.sudoku[x_slice, y_slice]
    return ind1, ind2

# def swap_squares(ind1, ind2, n=3):
#     chosen_squares = random.sample(squares, k=n)
#     for (xbegin, xend), (ybegin, yend) in chosen_squares:
#         square1 = deepcopy(ind1.sudoku[xbegin:xend, ybegin:yend])
#         square2 = deepcopy(ind2.sudoku[xbegin:xend, ybegin:yend])
#         ind1.sudoku[xbegin:xend, ybegin:yend] = square2
#         ind2.sudoku[xbegin:xend, ybegin:yend] = square1
#     return ind1, ind2
