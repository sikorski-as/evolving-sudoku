from random import random, shuffle

from evaluation import validate_chromosome, validate_chromosome_extended
from evolutionary import chromosome, config, mutations, crossovers
from deap import creator, tools, base

import tools as project_tools
from evolutionary.config import EvolutionConfig


def generate_chromosome(cls, sudoku, sudoku_generating_function):
    return cls(sudoku, sudoku_generating_function)


def create_toolbox():
    toolbox = base.Toolbox()

    # basic operators
    toolbox.register("individual", generate_chromosome, creator.Individual, cfg.sudoku_instance,
                     chromosome.generate_random_sudoku_instance_with_square_constraints)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", validate_chromosome_extended)

    # selections
    toolbox.register("select", tools.selTournament, tournsize=4)
    # toolbox.register("select", tools.selBest)

    # crossovers
    toolbox.register("mate_r", crossovers.swap_rows)
    toolbox.register("mate_c", crossovers.swap_columns)
    toolbox.register("mate_s", crossovers.swap_squares)
    # toolbox.register("mate_s", crossovers.swap_squares_uniform)

    # mutations
    toolbox.register("mutate", mutations.random_9_square)
    toolbox.register("mutate_swap", mutations.random_swap_in_square)

    return toolbox


def run(cfg: config.EvolutionConfig) -> None:
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", chromosome.Chromosome, fitness=creator.FitnessMin)

    toolbox = create_toolbox()

    population = toolbox.population(n=cfg.population_size)
    fitnesses = [toolbox.evaluate(el) for el in population]
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    CXPB, MXPB = 0.2, 0.15

    i = 0
    while i < cfg.max_iterations:
        i += 1

        # Select the next generation individuals
        # offspring = toolbox.select(population, len(population))

        # Clone the selected individuals
        offspring = list(map(toolbox.clone, population))

        # crossover
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random() < CXPB:
                # if random() < 0.2:
                #     if random() < 0.5:
                #         toolbox.mate_c(child1, child2)
                #     else:
                #         toolbox.mate_r(child1, child2)
                # else:
                toolbox.mate_s(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # mutation
        for mutant in offspring:
            if random() < MXPB:
                if random() < 0.5:
                    toolbox.mutate(mutant)
                else:
                    toolbox.mutate_swap(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # select individuals for the next generation
        population = offspring + population
        population = toolbox.select(population, k=cfg.population_size)  # ; shuffle(population)
        # population = tools.selTournament(population, k=cfg.population_size, tournsize=4)

        # show the best in the generation
        best = tools.selBest(population, 1)[0]
        print('after iteration', i, 'best fitness is', best.fitness)

    best = tools.selBest(population, 1)[0]
    print(best.fitness)
    print(best.sudoku)


if __name__ == '__main__':
    # cfg = config.DefaultConfig
    sample_sudoku_instances = project_tools.load_instances("../data/instances.json")
    cfg = EvolutionConfig(
        sudoku_instance=sample_sudoku_instances['easy'][0]['puzzle'],
        max_iterations=7500,
        population_size=200
    )
    run(cfg)
