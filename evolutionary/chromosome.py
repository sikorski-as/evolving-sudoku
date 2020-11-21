import sys
from typing import List, Tuple
import numpy as np


class Chromosome:

    def __init__(self, sudoku: np.ndarray, starting_points: List[Tuple]):
        if self.has_correct_dimensions(sudoku):
            self.starting_points: List[Tuple] = starting_points
            self.sudoku: np.ndarray = sudoku
            self.score: int = sys.maxsize
        else:
            raise Exception("Wrong data passed as sudoku instance!")

    @staticmethod
    def has_correct_dimensions(sudoku: np.ndarray) -> bool:
        return sudoku.shape == (9, 9)


def create_random(sudoku_instance: np.ndarray, amount: int = 1) -> List[Chromosome]:
    chromosomes: List[Chromosome] = []
    for _ in range(amount):
        chromosomes.append(Chromosome(*_generate_random_sudoku_instance(sudoku_instance)))
    return chromosomes


def _generate_random_sudoku_instance(sudoku: np.ndarray) -> (np.ndarray, List[Tuple]):
    points = np.where(sudoku > 0)
    static_points = [(x, y) for x, y in zip(points[0], points[1])]
    sudoku_instance = np.random.randint(1, 10, (9, 9))
    for x, y in static_points:
        sudoku_instance[x, y] = sudoku[x, y]
    return sudoku_instance, static_points


