import tools
from evaluation import validate
from evolutionary import chromosome, config


def run(cfg: config.EvolutionConfig) -> None:
    population = chromosome.create_random(cfg.sudoku_instance, 10)
    for el in population:
        el.score = validate(el.sudoku)


if __name__ == '__main__':
    sample_sudoku_instances = tools.load_instances("../data/instances.json")

    ecfg = config.EvolutionConfig(
        sudoku_instance=sample_sudoku_instances['easy'][0]['puzzle'],
        max_iterations=2
    )

    run(ecfg)
