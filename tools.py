import json
import numpy as np


def load_instances(filename):
    dataset = None
    with open(filename, 'r') as file:
        dataset = json.load(file)

    for difficulty, instances in dataset.items():
        for instance in instances:
            instance['puzzle'] = np.array(instance['puzzle'])
            instance['solution'] = np.array(instance['solution'])

    return dataset
