from typing import List, Tuple, Callable
import numpy as np

from evolutionary.config import DefaultConfig


class Chromosome:

    def __init__(self, sudoku_instance: np.ndarray, sudoku_generating_func: Callable[[np.ndarray], Tuple[np.ndarray, List[Tuple]]]):
        sudoku, starting_points = sudoku_generating_func(sudoku_instance)
        if self.has_correct_dimensions(sudoku):
            self.sudoku_instance: np.ndarray = sudoku_instance
            self.starting_points: List[Tuple] = starting_points
            self.sudoku: np.ndarray = sudoku
        else:
            raise Exception("Wrong data passed as sudoku instance!")

    @staticmethod
    def has_correct_dimensions(sudoku: np.ndarray) -> bool:
        return sudoku.shape == (9, 9)


def create_random(sudoku_instance: np.ndarray, amount: int = 1) -> List[Chromosome]:
    chromosomes: List[Chromosome] = []
    for _ in range(amount):
        chromosomes.append(Chromosome(*generate_random_sudoku_instance(sudoku_instance)))
    return chromosomes


def generate_random_sudoku_instance(sudoku: np.ndarray) -> (np.ndarray, List[Tuple]):
    points = np.where(sudoku > 0)
    static_points = [(x, y) for x, y in zip(points[0], points[1])]
    sudoku_instance = np.random.randint(1, 10, (9, 9))
    for x, y in static_points:
        sudoku_instance[x, y] = sudoku[x, y]
    return sudoku_instance, static_points


def generate_random_sudoku_instance_with_constraints(sudoku: np.ndarray) -> (np.ndarray, List[Tuple]):
    """
    Uses every number only 9 times.
    Sudoku created by creating permutation in range 1-9 9 times.
    :param sudoku instance to be solved
    :return:
    """
    points = np.where(sudoku > 0)
    starting_points = [(x, y) for x, y in zip(points[0], points[1])]
    sudoku_instance = np.copy(sudoku)
    for i in range(0, 9):
        sudoku_instance[i, :] = np.random.permutation(range(1, 10))
    for x, y in starting_points:
        sudoku_instance[x, y] = sudoku[x, y]
    return sudoku_instance, starting_points


def set_back_starting_points(ind) -> None:
    for x, y in ind.starting_points:
        ind.sudoku[x, y] = ind.sudoku_instance[x, y]


if __name__ == '__main__':
    cfg: DefaultConfig = DefaultConfig
    generate_random_sudoku_instance_with_constraints(cfg.sudoku_instance)
