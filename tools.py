import json
import math
import time
import types
from contextlib import contextmanager
from copy import deepcopy

import jsonpickle as jsonpickle
import numpy as np


def load_instances(filename):
    dataset = None
    with open(filename, 'r') as file:
        dataset = json.load(file)

    for difficulty, instances in dataset.items():
        for instance in instances:
            instance['puzzle'] = np.array(instance['puzzle'])
            try:
                instance['solution'] = np.array(instance['solution'])
            except:
                instance['solution'] = None

    return dataset


def load_sudoku_instances(filename):
    with open(filename, 'r') as file:
        instances = json.load(file, object_hook=lambda d: types.SimpleNamespace(**d))
        return instances


class Timer:
    DEFAULT_PRINT = False

    def __init__(self, name='It', print_on_exit: bool = DEFAULT_PRINT):
        self._name = name
        self.print_on_exit = print_on_exit
        self._start = None
        self._accumulator = 0.0

    def __enter__(self):
        self._start = time.time()
        return self

    def __exit__(self, *args):
        if self.print_on_exit:
            print('{} took {}s'.format(self._name, self.elapsed))

    @contextmanager
    def suspend(self):
        self._accumulator += self.elapsed
        yield
        self._start = time.time()

    @property
    def elapsed(self):
        if self._start is None:
            raise RuntimeError('Timer has to be started first, use with-statement')
        return time.time() - self._start + self._accumulator

    def print_elapsed(self):
        print('{} so far: {}s'.format(self._name, self.elapsed))


class SolutionTracer:
    def __init__(self, filename: str, id: int, clues: int, collect_partial: bool = True, max_repetitions: int = 1000):
        self.filename = filename
        self.collect_partial = collect_partial
        self.best = None
        self.best_time = math.inf
        self.times = []
        self.scores = []
        self.repetitions = 0
        self.max_repetitions = max_repetitions
        self.id = id
        self.clues = clues

    def update(self, solution, time):
        if self.collect_partial:
            if len(self.scores) != 0:
                self.repetitions = self.repetitions + 1 if self.scores[-1] == solution.fitness.values else 0
            self.scores.append(solution.fitness.values)
            self.times.append(time)
        if self.best is None or solution.fitness.values < self.best.fitness.values:
            self.best = deepcopy(solution)
            self.best_time = time

    @property
    def repetitions_exceeded(self):
        return self.repetitions > self.max_repetitions

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:
            result = {
                "Exit status": {
                    "Finished normally": exc_type is None,
                    'Exception type': str(exc_type),
                },
                "Partial times": self.times,
                "Partial scores": self.scores,
                "Solution": self.best.sudoku.tolist(),
                "Id": self.id,
                "Clues": self.clues
            }
        except AttributeError:
            result = {
                "Exit status": {
                    'Finished normally': exc_type is None,
                    'Exception type': str(exc_type)
                },
                'Error': 'No best chromosome set'
            }
        print(result)
        file_name = "{}_{}".format(self.filename, time.time())
        with open('results/{}/{}'.format(self.id, file_name), mode='w') as file:
            file.write(jsonpickle.encode(result))

    def __str__(self):
        return '<SolutionTracer' + '\n\tbest solution: {}'.format(self.best) + '\n\ttime: {:.3f}s'.format(
            self.best_time) + '\n\tcost: {:.3f}'.format(self.best.value) + '\n>'

    def print(self):
        print(str(self))
