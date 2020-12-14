import time

from evaluation import is_row_valid, is_column_valid, is_square_valid, _validate
from dfs import config


def _precompute_possibilities(grid):
    full_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    possibilities = {}

    square_cache = {}
    row_cache = {}
    column_cache = {}

    # Create Possible values of 1..9 for each Cell
    for row in range(0, 9):
        for col in range(0, 9):
            if grid[row][col] == 0:
                # Create possible values in row and subtract from full set
                in_row = row_cache[row] if row in row_cache else set(grid[row])
                r = full_set - in_row

                # Create possible values in column and subtract
                in_column = column_cache[col] if col in column_cache else set(grid[:, col])
                c = r - in_column

                # Create possible values in square and subtract
                square_id = square_vertical_id, square_horizontal_id = row // 3, col // 3

                row_start = square_vertical_id * 3
                col_start = square_horizontal_id * 3

                in_square = square_cache[square_id] if square_id in square_cache else \
                    set(grid[row_start:row_start + 3, col_start:col_start + 3].flatten())

                possibilities[(row, col)] = list(c - in_square)

    return possibilities


def run(cfg: config.DFSConfig) -> None:
    sudoku = cfg.sudoku_instance
    possibilities = _precompute_possibilities(sudoku)

    start = time.time()
    solution = _dfs(sudoku, possibilities)
    end = time.time()

    print('solution found by DFS in {} seconds:'.format(end - start))
    print(solution)
    print('repetitions:', _validate(solution))
    print('solution from dataset:')
    print(cfg.sudoku_solution)
    print('are they the same?', solution == cfg.sudoku_solution)


def sudoku_iterator(current_row, current_column):
    nrow = current_row + 1
    ncol = current_column
    if nrow >= 9:
        nrow = 0
        ncol = current_column + 1
    return nrow, ncol


def _dfs(sudoku, possibilities, row=0, col=0):
    if col == 9:
        return sudoku

    if sudoku[row, col] != 0:  # if already filled
        nrow, ncol = sudoku_iterator(row, col)
        return _dfs(sudoku, possibilities, nrow, ncol)
    else:
        for possible_number in possibilities[(row, col)]:
            sudoku[row, col] = possible_number
            valid = is_row_valid(sudoku, row, col) and is_column_valid(sudoku, row, col) and is_square_valid(sudoku, row, col)
            if valid:
                nrow, ncol = sudoku_iterator(row, col)
                solution = _dfs(sudoku, possibilities, nrow, ncol)
                if solution is not None:
                    return solution
                else:
                    continue

        sudoku[row, col] = 0
        print('failed, backtracking ({}, {})'.format(row, col))
        return None


if __name__ == '__main__':
    cfg = config.DefaultConfig
    run(cfg)
