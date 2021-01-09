from random import random
import numpy as np
from evaluation import validate_chromosome
from evolutionary import chromosome, config, mutations, crossovers
from deap import creator, tools, base

from tools import Timer, SolutionTracer


def generate_chromosome(cls, sudoku, sudoku_generating_function):
    return cls(sudoku, sudoku_generating_function)


def create_toolbox(cfg: config.EvolutionConfig):
    toolbox = base.Toolbox()
    toolbox.register("individual", generate_chromosome, creator.Individual, cfg.sudoku_instance,
                     chromosome.generate_random_sudoku_instance_with_square_constraints)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", validate_chromosome)
    toolbox.register("select_t", tools.selTournament, tournsize=3)
    toolbox.register("select_b", tools.selBest)
    toolbox.register("mate_r", crossovers.swap_rows)
    toolbox.register("mate_c", crossovers.swap_columns)
    toolbox.register("mate_s", crossovers.swap_squares)
    toolbox.register("mate_score", crossovers.swap_using_score)
    toolbox.register("mutate", mutations.random_9_square)
    toolbox.register("mutate_swap", mutations.random_swap_in_square)
    return toolbox


def run(cfg: config.EvolutionConfig) -> None:
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", chromosome.Chromosome, fitness=creator.FitnessMin)

    toolbox = create_toolbox(cfg)

    population = toolbox.population(n=cfg.population_size)
    fitnesses = [toolbox.evaluate(el) for el in population]
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    CXPB, MXPB = 0.3, 0.3

    i = 0
    with Timer() as timer, SolutionTracer(filename=f"Evolutionary_CXPB_{CXPB}_MXPB_{MXPB}", max_repetitions=cfg.max_iterations) as solution_tracer:
        while cfg.max_iterations > i:
            i += 1
            # Select the next generation individuals
            offspring = toolbox.select_b(population, len(population))
            # Clone the selected individuals
            offspring = list(map(toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random() < CXPB:
                    toolbox.mate_score(child1, child2)
                    # if random() < 0.99:
                    # if random() < 0.5:
                    #     toolbox.mate_c(child1, child2)
                    # else:
                    #     toolbox.mate_r(child1, child2)
                    # else:
                    #     toolbox.mate_s(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random() < MXPB:
                    # if random() < 0.1:
                    #     toolbox.mutate(mutant)
                    # else:
                    toolbox.mutate_swap(mutant)
                    del mutant.fitness.values

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            population = offspring + population
            population = toolbox.select_t(population, cfg.population_size)
            # population = tools.selBest(population, k=cfg.population_size)
            best = tools.selBest(population, 1)[0]
            solution_tracer.update(best, timer.elapsed)
            print(i, best.fitness)
            if best.fitness.values[0] == 0:
                break
            # if best.fitness.values[0] < currentBest:
            #     currentBest = (best.fitness.values[0])
            #     MXPB = MXPB * 0.9 if MXPB * 0.99 > 0.15 else 0.15
            # else:
            #     MXPB = MXPB * 1.5 if MXPB * 1.01 < 0.5 else 0.5
            # MXPB = MXPB * 0.999 if MXPB * 0.99 > 0.10 else 0.10

    best = tools.selBest(population, 1)[0]
    print(best.fitness)
    print(best.sudoku)


if __name__ == '__main__':
    cfg = config.DefaultConfig
    run(cfg)
