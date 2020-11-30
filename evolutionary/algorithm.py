from random import random

from evaluation import validate_chromosome
from evolutionary import chromosome, config, mutations, crossovers
from deap import creator, tools, base


def generate_chromosome(cls, sudoku, sudoku_generating_function):
    return cls(sudoku, sudoku_generating_function)


def create_toolbox():
    toolbox = base.Toolbox()
    toolbox.register("individual", generate_chromosome, creator.Individual, cfg.sudoku_instance,
                     chromosome.generate_random_sudoku_instance_with_square_constraints)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", validate_chromosome)
    toolbox.register("select", tools.selTournament, tournsize=2)
    toolbox.register("select", tools.selBest)
    toolbox.register("mate_r", crossovers.swap_rows)
    toolbox.register("mate_c", crossovers.swap_columns)
    toolbox.register("mate_s", crossovers.swap_squares)
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
    while cfg.max_iterations > i:
        i += 1
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random() < CXPB:
                if random() < 0.6:
                    if random() < 0.5:
                        toolbox.mate_c(child1, child2)
                    else:
                        toolbox.mate_r(child1, child2)
                else:
                    toolbox.mate_s(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random() < MXPB:
                if random() < 0.1:
                    toolbox.mutate(mutant)
                else:
                    toolbox.mutate_swap(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        population = offspring + population
        population = tools.selTournament(population, k=cfg.population_size, tournsize=4)
        # population = tools.selBest(population, k=cfg.population_size)
        best = tools.selBest(population, 1)[0]
        print(best.fitness)

    best = tools.selBest(population, 1)[0]
    print(best.fitness)
    print(best.sudoku)


if __name__ == '__main__':
    cfg = config.DefaultConfig
    run(cfg)
