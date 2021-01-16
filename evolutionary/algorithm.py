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
    toolbox.register("select_t", tools.selTournament, tournsize=5)
    toolbox.register("select_b", tools.selBest)
    toolbox.register("mate_r", crossovers.swap_rows)
    toolbox.register("mate_c", crossovers.swap_columns)
    toolbox.register("mate_s", crossovers.swap_squares)
    toolbox.register("mate_score", crossovers.swap_using_score)
    toolbox.register("mutate", mutations.random_9_square)
    toolbox.register("mutate_swap_many", mutations.random_swap_in_squares)
    toolbox.register("mutate_swap_one", mutations.random_swap_in_square)
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
    child_per_parent = 3

    i = 0
    with Timer() as timer, SolutionTracer(filename=f"Evolutionary_CXPB_{CXPB}_MXPB_{MXPB}",
                                          max_repetitions=cfg.max_iterations) as solution_tracer:
        while cfg.max_iterations > i:
            i += 1
            # Select the next generation individuals
            offspring = toolbox.select_b(population, len(population))
            # Clone the selected individuals
            offspring = list(map(toolbox.clone, child_per_parent * offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random() < CXPB:
                    toolbox.mate_score(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random() < MXPB:
                    if random() < 0.8:
                        toolbox.mutate_swap_many(mutant)
                    else:
                        toolbox.mutate_swap_one(mutant)
                    del mutant.fitness.values

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            best_offspring = []
            for begin, end in zip(range(0, len(offspring) - child_per_parent, child_per_parent),
                                  range(child_per_parent, len(offspring), child_per_parent)):
                best_offspring.append(sorted(offspring[begin:end], key=lambda x: x.fitness.values[0])[0])

            population = offspring + population
            population = toolbox.select_t(population, cfg.population_size)
            # population = tools.selBest(population, k=cfg.population_size)
            best = tools.selBest(population, 1)[0]
            solution_tracer.update(best, timer.elapsed)
            print(i, best.fitness)
            if best.fitness.values[0] == 0:
                break
            if i % 100 == 0:
                print(best.sudoku)

    best = tools.selBest(population, 1)[0]
    print(best.fitness)
    print(best.sudoku)


if __name__ == '__main__':
    cfg = config.DefaultConfig
    run(cfg)
