from dataclasses import dataclass
import numpy as np

import tools


@dataclass
class EvolutionConfig:
    sudoku_instance: np.ndarray
    id: int
    clues: int
    max_iterations: int
    population_size: int


s = np.array(
    [[0, 0, 8, 0, 6, 0, 9, 0, 0],
    [0, 0, 0, 2, 0, 3, 6, 7, 8],
    [7, 0, 6, 0, 5, 1, 0, 0, 4],
    [9, 7, 3, 0, 4, 8, 1, 0, 0],
    [6, 2, 0, 0, 3, 9, 0, 5, 0],
    [0, 0, 1, 7, 0, 0, 0, 0, 0],
    [5, 8, 0, 9, 0, 0, 3, 0, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 0, 0, 0, 5, 7, 2, 1]]
)

# sample_sudoku_instances = tools.load_instances("data/instances.json")
instances_set = tools.load_sudoku_instances("data/new_instances_25_30_35.json")

DefaultConfig: EvolutionConfig = EvolutionConfig(
    # sudoku_instance=sample_sudoku_instances['easy'][0]['puzzle'],
    id=0,
    clues=25,
    sudoku_instance=np.array(instances_set.easy[0].puzzle),
    max_iterations=20000,
    population_size=150
)

