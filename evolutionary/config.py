from dataclasses import dataclass
import numpy as np


@dataclass
class EvolutionConfig:
    sudoku_instance: np.ndarray
    max_iterations: int
