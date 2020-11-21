import tools
from evolutionary import algorithm, config

if __name__ == '__main__':
    sample_sudoku_instances = tools.load_instances("../data/instances.json")

    ecfg = config.EvolutionConfig(
        sudoku_instance=sample_sudoku_instances['easy'][0]['puzzle'],
        max_iterations=2
    )

    algorithm.run(ecfg)
