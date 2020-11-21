import unittest
from evaluation import validate
import numpy as np


class EvaluationTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.sudoku_with_bad_columns = np.array([
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9]
        ])
        self.sudoku_with_bad_rows = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2, 2, 2, 2],
            [3, 3, 3, 3, 3, 3, 3, 3, 3],
            [4, 4, 4, 4, 4, 4, 4, 4, 4],
            [5, 5, 5, 5, 5, 5, 5, 5, 5],
            [6, 6, 6, 6, 6, 6, 6, 6, 6],
            [7, 7, 7, 7, 7, 7, 7, 7, 7],
            [8, 8, 8, 8, 8, 8, 8, 8, 8],
            [9, 9, 9, 9, 9, 9, 9, 9, 9],
        ])
        self.correct_sudoku = np.array([
            [2, 3, 4, 6, 1, 8, 9, 7, 5],
            [5, 1, 7, 9, 3, 4, 2, 6, 8],
            [8, 6, 9, 2, 7, 5, 3, 4, 1],
            [6, 9, 5, 4, 2, 1, 7, 8, 3],
            [4, 7, 3, 8, 5, 9, 6, 1, 2],
            [1, 2, 8, 3, 6, 7, 4, 5, 9],
            [7, 5, 6, 1, 9, 3, 8, 2, 4],
            [9, 8, 2, 5, 4, 6, 1, 3, 7],
            [3, 4, 1, 7, 8, 2, 5, 9, 6]
        ])
        self.square_error = 6
        self.row_error = 8

    def test_evaluation_bad_rows(self):
        self.assertEqual(validate(self.sudoku_with_bad_rows), 9 * self.row_error + 9 * self.square_error)

    def test_evaluation_bad_columns(self):
        self.assertEqual(validate(self.sudoku_with_bad_columns), 9 * self.row_error + 9 * self.square_error)

    def test_evaluation_correct(self):
        self.assertEqual(validate(self.correct_sudoku), 0)


if __name__ == '__main__':
    unittest.main()
