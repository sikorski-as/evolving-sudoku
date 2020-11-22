from copy import copy


def swap_rows(ind1, ind2):
    begin, end = 3, 6
    part1 = copy(ind1.sudoku[begin:end, :])
    part2 = copy(ind2.sudoku[begin:end, :])
    ind1.sudoku[begin:end, :], ind2.sudoku[begin:end, :] = part2, part1
    return ind1, ind2

