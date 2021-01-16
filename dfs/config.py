from dataclasses import dataclass
import numpy as np

import tools


@dataclass
class DFSConfig:
    sudoku_instance: np.ndarray
    sudoku_solution: np.ndarray = None


_sample_sudoku_instances = tools.load_instances("../data/instances.json")

DefaultConfig: DFSConfig = DFSConfig(
    sudoku_instance=_sample_sudoku_instances['easy'][0]['puzzle'],
    sudoku_solution=_sample_sudoku_instances['easy'][0]['solution'],
)
