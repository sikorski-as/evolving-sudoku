import random
import numpy as np
from evaluation import validate_chromosome
from evolutionary import chromosome, config, mutations, crossovers
from deap import creator, tools, base

from tools import Timer, SolutionTracer


def generate_chromosome(cls, sudoku, sudoku_generating_function):
    return cls(sudoku, sudoku_generating_function)


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", chromosome.Chromosome, fitness=creator.FitnessMin)
TOURNAMENT_SIZE = 2


def create_toolbox(cfg: config.EvolutionConfig):
    toolbox = base.Toolbox()
    toolbox.register("individual", generate_chromosome, creator.Individual, cfg.sudoku_instance,
                     chromosome.generate_random_sudoku_instance_with_square_constraints)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", validate_chromosome)
    toolbox.register("select_t", tools.selTournament, tournsize=TOURNAMENT_SIZE)
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
    toolbox = create_toolbox(cfg)

    population = toolbox.population(n=cfg.population_size)
    fitnesses = [toolbox.evaluate(el) for el in population]
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    CXPB, MXPB = 0.3, 0.3
    child_per_parent = 2

    i = 0
    with Timer() as timer, SolutionTracer(
            filename=f"Evolutionary_CXPB_{CXPB}_MXPB_TS_{TOURNAMENT_SIZE}_{MXPB}_CPP_{child_per_parent}_I_{cfg.max_iterations}_PS_{cfg.population_size}",
            max_repetitions=cfg.max_iterations,
            id=cfg.id,
            clues=cfg.clues
    ) as solution_tracer:
        while cfg.max_iterations > i:
            i += 1

            offspring = population
            # Clone the selected individuals
            offspring = list(map(toolbox.clone, child_per_parent * offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    # if random.random() < 0.5:
                    toolbox.mate_score(child1, child2)
                    # else:
                    #     toolbox.mate_r(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < MXPB:
                    if random.random() < 0.8:
                        toolbox.mutate_swap_many(mutant)
                    else:
                        toolbox.mutate_swap_one(mutant)
                    del mutant.fitness.values

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            best_offspring = []
            if child_per_parent > 1:
                for begin, end in zip(range(0, len(offspring) - child_per_parent + 1, child_per_parent),
                                      range(child_per_parent, len(offspring) + 1, child_per_parent)):
                    best_offspring.append(sorted(offspring[begin:end], key=lambda x: x.fitness.values[0])[0])
            else:
                best_offspring = offspring

            population = choose_unique(best_offspring)
            population = toolbox.select_t(population, cfg.population_size)

            # saving and checking stats
            best = tools.selBest(population, 1)[0]
            solution_tracer.update(best, timer.elapsed)
            if best.fitness.values[0] == 0:
                break
            if i % 100 == 0:
                print(i, best.fitness)
                print(best.sudoku)

    best = tools.selBest(population, 1)[0]
    print(best.fitness)
    print(best.sudoku)


def choose_unique(population: creator.Individual):
    population_set = []
    for el in population:
        duplicate = False
        for unique_el in population_set:
            if (unique_el.sudoku == el.sudoku).all():
                duplicate = True
                break
        if not duplicate:
            population_set.append(el)
    return population_set


if __name__ == '__main__':
    cfg = config.DefaultConfig
    run(cfg)
