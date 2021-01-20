import os
from pathlib import Path

import numpy as np

import tools
from multiprocessing import Pool
from evolutionary import config, algorithm


def test_sudoku_instance(sudoku_problem_instance, n=25):
    Path(f"results/{sudoku_problem_instance.id}").mkdir(parents=True, exist_ok=True)
    cfg = config.EvolutionConfig(
        clues=sudoku_problem_instance.clues,
        id=sudoku_problem_instance.id,
        sudoku_instance=np.array(sudoku_problem_instance.puzzle),
        max_iterations=700,
        population_size=150
    )
    with Pool(5) as p:
        p.map(algorithm.run, [cfg for _ in range(n)])
        algorithm.run(cfg)


def test_sudoku_instances(sudoku_instances, n=25):
    for sudoku_instance in sudoku_instances[:20]:
        test_sudoku_instance(sudoku_instance, n)


if __name__ == '__main__':
    instances_set = tools.load_sudoku_instances("data/new_instances_25_30_35.json")
    test_sudoku_instances(instances_set.easy)
    # test_sudoku_instances(instances_set.medium)
    # test_sudoku_instances(instances_set.hard)
