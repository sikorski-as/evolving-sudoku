from dataclasses import dataclass
import numpy as np

import tools


@dataclass
class EvolutionConfig:
    sudoku_instance: np.ndarray
    max_iterations: int
    population_size: int


sample_sudoku_instances = tools.load_instances("../data/instances.json")

DefaultConfig: EvolutionConfig = EvolutionConfig(
    sudoku_instance=sample_sudoku_instances['easy'][0]['puzzle'],
    max_iterations=500,
    population_size=200
)
