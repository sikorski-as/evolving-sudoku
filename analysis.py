import itertools
import json
import os
import statistics

import numpy as np
import yaml
import pathlib
from matplotlib import pyplot as plt

import jsonpickle

from evaluation import validate_sudoku

error_files = []


def load_json(path):
    try:
        with open(path) as f:
            return jsonpickle.loads(f.read())
    except json.decoder.JSONDecodeError:
        error_files.append(path)
        return None


def get_instances_ids_from_results_dir(rootdir: str, instances_filter=lambda x: True):
    root = pathlib.Path(rootdir)
    return sorted([int(instance_id) for instance_id in filter(instances_filter, os.listdir(root))])


def get_instances_ids_from_results_dir_for_difficulty_level(rootdir: str, difficulty_level_name: str):
    try:
        instances_filter = {
            '01_easy': lambda x: 0 <= int(x) < 50,
            '02_medium': lambda x: 50 <= int(x) < 100,
            '03_advanced': lambda x: 100 <= int(x) < 150,
            '04_hard': lambda x: 150 <= int(x) < 200,
        }[difficulty_level_name]
        return get_instances_ids_from_results_dir(rootdir, instances_filter=instances_filter)
    except KeyError:
        raise ValueError("unknown difficulty level")


def get_instances_results(rootdir: str, instances_filter=lambda x: True):
    root = pathlib.Path(rootdir)
    results = {}
    for instance_id in filter(instances_filter, os.listdir(root)):
        results[instance_id] = []
        for file in os.listdir(root / instance_id):
            results_one_attempt = load_json(root / instance_id / file)
            if results_one_attempt is not None:
                results[instance_id].append(results_one_attempt)
    return results


def get_results_for_difficulty_level(rootdir: str, difficulty_level_name: str):
    try:
        instances_filter = {
            '01_easy': lambda x: 0 <= int(x) < 50,
            '02_medium': lambda x: 50 <= int(x) < 100,
            '03_advanced': lambda x: 100 <= int(x) < 150,
            '04_hard': lambda x: 150 <= int(x) < 200,
        }[difficulty_level_name]
        return get_instances_results(rootdir, instances_filter=instances_filter)
    except KeyError:
        raise ValueError("unknown difficulty level")


def check_if_solved_correctly(solutions: list):
    return [validate_sudoku(solution) for solution in solutions]


def average_or_none(data: list):
    return None if len(data) == 0 else sum(data) / len(data)


def std_or_none(data: list):
    return None if len(data) < 2 else statistics.stdev(data)


def max_or_none(data: list):
    return None if len(data) == 0 else max(data)


def min_or_none(data: list):
    return None if len(data) == 0 else min(data)


def make_boxplot(title: str,
                 data: list,
                 xlabels: list, xlabel: str, ylabel: str, ylims: tuple,
                 output_filename: str):
    plt.clf()
    plt.boxplot(data)
    plt.title(title)
    plt.xticks(list(range(1, len(xlabels) + 1)), xlabels)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim(ylims)
    plt.savefig(output_filename)


def make_lineplot(title: str,
                  xdata_groups: list,
                  ydata_groups: list,
                  xlabel: str, ylabel: str,
                  xlims: tuple, ylims: tuple,
                  method,
                  output_filename: str):
    plt.clf()

    for x_points_group, y_points_group in zip(xdata_groups, ydata_groups):
        xs = list(np.array(one_xs) for one_xs in x_points_group)
        ys = list(np.array([score[0] for score in one_ys]) for one_ys in y_points_group)

        try:
            mean_x_axis = [i for i in range(max(len(_xs) for _xs in xs))]
            ys_interp = [np.interp(mean_x_axis, xs[i], ys[i]) for i in range(len(xs))]
            mean_y_axis = method(ys_interp, axis=0)
            plt.plot(mean_x_axis, mean_y_axis)
        except ValueError:
            pass  # xs is empty

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xlims is not None:
        plt.xlim(xlims)
    if ylims is not None:
        plt.ylim(ylims)
    plt.xscale('log')
    plt.savefig(output_filename)


def calculate_statistics(difficulty_results: dict, attach_all=False):
    instance_stats = {}
    all_times = []
    all_times_correctly_solved = []
    n_all_attempts_correctly_solved = 0
    n_all_attempts = 0
    all_numbers_of_generations = []
    all_numbers_of_generations_correctly_solved = []
    for instance_id, instance_results in difficulty_results.items():
        # solved percentage
        solutions = [one_result['Solution'] for one_result in instance_results]
        list_of_correctly_solved = check_if_solved_correctly(solutions)
        n_correctly_solved = sum(list_of_correctly_solved)
        correctly_solved_percentage = n_correctly_solved / len(solutions) * 100

        n_all_attempts_correctly_solved += n_correctly_solved
        n_all_attempts += len(solutions)

        # average time
        times = [one_result['Partial times'][-1] for one_result in instance_results]
        all_times.extend(times)

        times_correctly_solved = list(itertools.compress(times, list_of_correctly_solved))
        all_times_correctly_solved.extend(times_correctly_solved)

        # number of generations for all attempts of current instance
        numbers_of_generations = [len(one_result['Partial scores']) for one_result in instance_results]
        numbers_of_generations_for_correctly_solved = list(
            itertools.compress(numbers_of_generations, list_of_correctly_solved))

        all_numbers_of_generations.extend(numbers_of_generations)
        all_numbers_of_generations_correctly_solved.extend(numbers_of_generations_for_correctly_solved)

        # report for current instance
        instance_stats[int(instance_id)] = {
            'number_of_attempts': len(solutions),
            'number_of_attempts_solved': n_correctly_solved,
            'correctly_solved_attempts_percentage': correctly_solved_percentage,

            'statistics': {
                'for_all_attempts': {
                    'time_average': average_or_none(times),
                    'time_std': std_or_none(times),
                    'time_min': min_or_none(times),
                    'time_max': max_or_none(times),
                    'number_of_generations_average': average_or_none(numbers_of_generations),
                    'number_of_generations_std': std_or_none(numbers_of_generations),
                    'number_of_generations_min': min_or_none(numbers_of_generations),
                    'number_of_generations_max': max_or_none(numbers_of_generations),
                },
                'for_correctly_solved_attempts': {
                    'time_average': average_or_none(times_correctly_solved),
                    'time_std': std_or_none(times_correctly_solved),
                    'time_min': min_or_none(times_correctly_solved),
                    'time_max': max_or_none(times_correctly_solved),
                    'number_of_generations_average': average_or_none(numbers_of_generations_for_correctly_solved),
                    'number_of_generations_std': std_or_none(numbers_of_generations_for_correctly_solved),
                    'number_of_generations_min': min_or_none(numbers_of_generations_for_correctly_solved),
                    'number_of_generations_max': max_or_none(numbers_of_generations_for_correctly_solved),
                }
            }

        }

        if attach_all:
            statistics = instance_stats[int(instance_id)]['statistics']
            statistics['for_all_attempts']['number_of_generations_raw_data'] = numbers_of_generations
            statistics['for_correctly_solved_attempts'][
                'number_of_generations_raw_data'] = numbers_of_generations_for_correctly_solved
            statistics['for_all_attempts']['time_raw_data'] = times
            statistics['for_correctly_solved_attempts']['time_raw_data'] = times_correctly_solved

    overall_stats = {
        'number_of_attempts': n_all_attempts,
        'number_of_attempts_solved': n_all_attempts_correctly_solved,
        'correctly_solved_attempts_percent': None if n_all_attempts == 0 else n_all_attempts_correctly_solved / n_all_attempts * 100,
        'statistics': {
            'for_all_attempts': {
                'time_average': average_or_none(all_times),
                'time_std': std_or_none(all_times),
                'time_min': min_or_none(all_times),
                'time_max': max_or_none(all_times),
                'number_of_generations_average': average_or_none(all_numbers_of_generations),
                'number_of_generations_std': std_or_none(all_numbers_of_generations),
                'number_of_generations_min': min_or_none(all_numbers_of_generations),
                'number_of_generations_max': max_or_none(all_numbers_of_generations),
            },
            'for_correctly_solved_attempts': {
                'time_average': average_or_none(all_times_correctly_solved),
                'time_std': std_or_none(all_times_correctly_solved),
                'time_min': min_or_none(all_times_correctly_solved),
                'time_max': max_or_none(all_times_correctly_solved),
                'number_of_generations_average': average_or_none(all_numbers_of_generations_correctly_solved),
                'number_of_generations_std': std_or_none(all_numbers_of_generations_correctly_solved),
                'number_of_generations_min': min_or_none(all_numbers_of_generations_correctly_solved),
                'number_of_generations_max': max_or_none(all_numbers_of_generations_correctly_solved),
            }
        }
    }

    if attach_all:
        statistics = overall_stats['statistics']
        statistics['for_all_attempts']['number_of_generations_raw_data'] = all_numbers_of_generations
        statistics['for_correctly_solved_attempts'][
            'number_of_generations_raw_data'] = all_numbers_of_generations_correctly_solved
        statistics['for_all_attempts']['time_raw_data'] = all_times
        statistics['for_correctly_solved_attempts']['time_raw_data'] = all_times_correctly_solved

    return {
        'overall_stats': overall_stats,
        'per_instance_stats': instance_stats
    }


if __name__ == '__main__':
    difficulty_levels_names = level_1, level_2, level_3, level_4 = ['01_easy', '02_medium', '03_advanced', '04_hard']
    report, report_big = None, None

    # load or generate big report
    try:
        with open('report_big.json') as report_big_file:
            report_big = json.load(report_big_file)
    except FileNotFoundError:
        report_big = {
            level_1:
                calculate_statistics(get_results_for_difficulty_level('output/results', '01_easy'), attach_all=True),
            level_2:
                calculate_statistics(get_results_for_difficulty_level('output/results', '02_medium'), attach_all=True),
            level_3:
                calculate_statistics(get_results_for_difficulty_level('output/results', '03_advanced'),
                                     attach_all=True),
            level_4:
                calculate_statistics(get_results_for_difficulty_level('output/results', '04_hard'), attach_all=True),
        }
        with open('report_big.json', 'w') as report_big_file:
            json.dump(report_big, report_big_file)

    # generate nice report file if not exists already
    try:
        with open('report.yaml') as report_file:
            report = yaml.safe_load(report_file)
    except FileNotFoundError:
        report = {
            level_1: calculate_statistics(get_results_for_difficulty_level('output/results', '01_easy')),
            level_2: calculate_statistics(get_results_for_difficulty_level('output/results', '02_medium')),
            level_3: calculate_statistics(get_results_for_difficulty_level('output/results', '03_advanced')),
            level_4: calculate_statistics(get_results_for_difficulty_level('output/results', '04_hard'))
        }
        with open('report.yaml', 'w') as report_file:
            yaml.dump(report, report_file)

    #
    # BOXPLOTS
    #

    TIME_LABEL = 'czas [sekundy]'
    SCORE_LABEL = 'wartość funkcji celu'
    INSTANCE_LABEL = 'ID instancji'
    DIFFICULTY_LABEL = 'poziom trudności'
    GENERATIONS_LABEL = 'liczba pokoleń'

    TIME_YLIMS = (-10, 510)
    GENERATIONS_YLIMS = (-100, 4100)
    SCORE_YLIMS = (-1, 25)

    # per difficulty level: number of generations (all attempts)
    make_boxplot('Liczba pokoleń (wszystkie próby)',
                 [level_stats['overall_stats']['statistics']['for_all_attempts']['number_of_generations_raw_data']
                  for level_stats in [report_big[level] for level in difficulty_levels_names]],
                 difficulty_levels_names,
                 DIFFICULTY_LABEL,
                 GENERATIONS_LABEL,
                 GENERATIONS_YLIMS,
                 'output/plots/n_generations_all.png')

    # per difficulty level: number of generations (correct only)
    make_boxplot('Liczba pokoleń (tylko rozwiązane)',
                 [level_stats['overall_stats']['statistics']['for_correctly_solved_attempts'][
                      'number_of_generations_raw_data']
                  for level_stats in [report_big[level] for level in difficulty_levels_names]],
                 difficulty_levels_names,
                 DIFFICULTY_LABEL,
                 GENERATIONS_LABEL,
                 GENERATIONS_YLIMS,
                 'output/plots/n_generations_correct.png')

    # per instance: number of generations (all attempts)
    for level_name in difficulty_levels_names:
        data = [pair for pair in report_big[level_name]['per_instance_stats'].items()]
        data.sort(key=lambda x: int(x[0]))

        make_boxplot(f'Liczba pokoleń (wszystkie próby) - poziom {level_name}',
                     [instance_data[1]['statistics']['for_all_attempts']['number_of_generations_raw_data'] for
                      instance_data in data],
                     [instance_data[0] for instance_data in data],
                     INSTANCE_LABEL,
                     GENERATIONS_LABEL,
                     GENERATIONS_YLIMS,
                     f'output/plots/n_generations_all_{level_name}.png')

    # per instance: number of generations (correct only)
    for level_name in difficulty_levels_names:
        data = [pair for pair in report_big[level_name]['per_instance_stats'].items()]
        data.sort(key=lambda x: int(x[0]))

        make_boxplot(f'Liczba pokoleń (tylko rozwiązane) - poziom {level_name}',
                     [instance_data[1]['statistics']['for_correctly_solved_attempts']['number_of_generations_raw_data']
                      for instance_data in data],
                     [instance_data[0] for instance_data in data],
                     INSTANCE_LABEL,
                     GENERATIONS_LABEL,
                     GENERATIONS_YLIMS,
                     f'output/plots/n_generations_correct_{level_name}.png')

    # per difficulty level: time (all attempts)
    make_boxplot('Czas (wszystkie próby)',
                 [level_stats['overall_stats']['statistics']['for_all_attempts']['time_raw_data']
                  for level_stats in [report_big[level] for level in difficulty_levels_names]],
                 difficulty_levels_names,
                 DIFFICULTY_LABEL,
                 TIME_LABEL,
                 TIME_YLIMS,
                 'output/plots/time_all.png')

    # per difficulty level: time (correct only)
    make_boxplot('Czas (tylko rozwiązane)',
                 [level_stats['overall_stats']['statistics']['for_correctly_solved_attempts']['time_raw_data']
                  for level_stats in [report_big[level] for level in difficulty_levels_names]],
                 difficulty_levels_names,
                 DIFFICULTY_LABEL,
                 TIME_LABEL,
                 TIME_YLIMS,
                 'output/plots/time_correct.png')

    # per instance: time (all attempts)
    for level_name in difficulty_levels_names:
        data = [pair for pair in report_big[level_name]['per_instance_stats'].items()]
        data.sort(key=lambda x: int(x[0]))

        make_boxplot(f'Czas (wszystkie próby) - poziom {level_name}',
                     [instance_data[1]['statistics']['for_all_attempts']['time_raw_data'] for
                      instance_data in data],
                     [instance_data[0] for instance_data in data],
                     INSTANCE_LABEL,
                     TIME_LABEL,
                     TIME_YLIMS,
                     f'output/plots/time_all_{level_name}.png')

    # per instance: time (correct only)
    for level_name in difficulty_levels_names:
        data = [pair for pair in report_big[level_name]['per_instance_stats'].items()]
        data.sort(key=lambda x: int(x[0]))

        make_boxplot(f'Czas (tylko rozwiązane) - poziom {level_name}',
                     [instance_data[1]['statistics']['for_correctly_solved_attempts']['time_raw_data']
                      for instance_data in data],
                     [instance_data[0] for instance_data in data],
                     INSTANCE_LABEL,
                     TIME_LABEL,
                     TIME_YLIMS,
                     f'output/plots/time_correct_{level_name}.png')

    #
    # LINE PLOTS
    #

    # per instance: average time lines (all attempts)
    for level_name in difficulty_levels_names:
        xdata = []
        ydata = []
        results = get_results_for_difficulty_level('output/results', level_name)
        for instance_id, instance_results in results.items():
            solutions = [one_result['Solution'] for one_result in instance_results]
            list_of_correctly_solved = check_if_solved_correctly(solutions)

            xdata.append([one_result['Partial times'] for one_result in instance_results])
            ydata.append([one_result['Partial scores'] for one_result in instance_results])

        make_lineplot(f'Uśrednione przebiegi czasowe (wszystkie próby) - poziom {level_name}',
                      xdata,
                      ydata,
                      TIME_LABEL,
                      SCORE_LABEL,
                      None, SCORE_YLIMS,
                      np.mean,
                      f'output/plots/time_all_mean_scores_{level_name}.png')

        make_lineplot(f'Maksymalne przebiegi czasowe (wszystkie próby) - poziom {level_name}',
                      xdata,
                      ydata,
                      TIME_LABEL,
                      SCORE_LABEL,
                      None, SCORE_YLIMS,
                      np.max,
                      f'output/plots/time_all_max_scores_{level_name}.png')

        make_lineplot(f'Minimalne przebiegi czasowe (wszystkie próby) - poziom {level_name}',
                      xdata,
                      ydata,
                      TIME_LABEL,
                      SCORE_LABEL,
                      None, SCORE_YLIMS,
                      np.min,
                      f'output/plots/time_all_min_scores_{level_name}.png')

    # per instance: average time lines (correct only)
    for level_name in difficulty_levels_names:
        xdata = []
        ydata = []
        results = get_results_for_difficulty_level('output/results', level_name)
        for instance_id, instance_results in results.items():
            solutions = [one_result['Solution'] for one_result in instance_results]
            list_of_correctly_solved = check_if_solved_correctly(solutions)

            xdata.append(list(itertools.compress([one_result['Partial times'] for one_result in instance_results],
                                                 list_of_correctly_solved)))
            ydata.append(list(itertools.compress([one_result['Partial scores'] for one_result in instance_results],
                                                 list_of_correctly_solved)))

        make_lineplot(f'Uśrednione przebiegi czasowe (tylko rozwiązane) - poziom {level_name}',
                      xdata,
                      ydata,
                      TIME_LABEL,
                      SCORE_LABEL,
                      None, SCORE_YLIMS,
                      np.mean,
                      f'output/plots/time_correct_mean_scores_{level_name}.png')

        make_lineplot(f'Maksymalne przebiegi czasowe (tylko rozwiązane) - poziom {level_name}',
                      xdata,
                      ydata,
                      TIME_LABEL,
                      SCORE_LABEL,
                      None, SCORE_YLIMS,
                      np.max,
                      f'output/plots/time_correct_max_scores_{level_name}.png')

        make_lineplot(f'Minimalne przebiegi czasowe (tylko rozwiązane) - poziom {level_name}',
                      xdata,
                      ydata,
                      TIME_LABEL,
                      SCORE_LABEL,
                      None, SCORE_YLIMS,
                      np.min,
                      f'output/plots/time_correct_min_scores_{level_name}.png')
