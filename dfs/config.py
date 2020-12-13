from dataclasses import dataclass
import numpy as np

import tools


@dataclass
class DFSConfig:
    sudoku_instance: np.ndarray


_sample_sudoku_instances = tools.load_instances("../data/instances.json")

DefaultConfig: DFSConfig = DFSConfig(
    sudoku_instance=_sample_sudoku_instances['easy'][0]['puzzle']
)
