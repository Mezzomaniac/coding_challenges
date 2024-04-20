from downloader import download

download(2023, 21)
with open('aoc2023_21input.txt') as inputfile:
    data = inputfile.read()
test_data = '''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........'''
test_data1 = '''.....
.....
.#S..
.#.#.
.....'''
test_data2 = '''...
.S.
...'''
test_data3 = '''...
.S#
...'''
#data = test_data
print(data)

from collections import namedtuple
from queue import Queue

Coord = namedtuple('Coord', 'y x')

DIRS = (Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0))

def neighbours(coord):
    return (Coord(coord.y + dir.y, coord.x + dir.x) for dir in DIRS)

def total_plots_visited(steps_taken: dict, evenness: int):
    return len([plot for plot, steps in steps_taken.items() if steps % 2 == evenness])

grid = data.splitlines()
height = len(grid)
width = len(grid[0])
period = height + width

STEP_GOAL = 64
STEP_GOAL = 26501365
TEST_GOAL = 1200

evenness = STEP_GOAL % 2

start = Coord(*divmod(data.index('S'), width + 1))
frontier = Queue()
steps_taken = {start: 0}
frontier.put(start)
max_steps = 0
plot_counts = {0: 1}
plot_count_diffs = {0: 0}
plot_count_diff_diffs = {0: 0}
acceleration_factor = None
cyclic_speed_factors = {}
cyclic_constants = {}
while not frontier.empty():
    current = frontier.get()
    current_steps = steps_taken[current]
    if current_steps in (STEP_GOAL, TEST_GOAL):
        continue
    if current_steps > max_steps and current_steps % 2 == evenness:
        plot_count = total_plots_visited(steps_taken, evenness)
        plot_counts[current_steps] = plot_count
        plot_count_diff = plot_count - plot_counts.get(current_steps - period, 0)
        plot_count_diffs[current_steps] = plot_count_diff
        plot_count_diff_diff = plot_count_diff - plot_count_diffs.get(current_steps - period, 0)
        plot_count_diff_diffs[current_steps] = plot_count_diff_diff
        plot_count_diff_diff_diff = plot_count_diff_diff - plot_count_diff_diffs.get(current_steps - period, 0)
        if acceleration_factor is None and not plot_count_diff_diff_diff:
            acceleration_factor = plot_count_diff_diff / 2 / period ** 2
        plot_count_minus_acceleration_component = 0.
        plot_count_minus_acceleration_component_diff = 0.
        plot_count_minus_variable_components = 0.
        if acceleration_factor:
            acceleration_component = acceleration_factor * current_steps ** 2
            plot_count_minus_acceleration_component = plot_count - acceleration_component
            plot_count_minus_acceleration_component_diff = plot_count_minus_acceleration_component - (plot_counts[current_steps - period] - acceleration_factor * (current_steps - period) ** 2)
            cyclic_speed_factors[current_steps % period] = plot_count_minus_acceleration_component_diff / period
            plot_count_minus_variable_components = plot_count_minus_acceleration_component - cyclic_speed_factors[current_steps % period] * current_steps
            cyclic_constants[current_steps % period] = plot_count_minus_variable_components
        print(current_steps, plot_count, plot_count_diff, plot_count_diff_diff, f'{plot_count_minus_acceleration_component:.2f}', f'{plot_count_minus_acceleration_component_diff:.2f}', f'{plot_count_minus_variable_components:.2f}')
        max_steps = current_steps + 1
    for next in neighbours(current):
        if next in steps_taken or grid[next.y % height][next.x % width] == '#':
            continue
        frontier.put(next)
        steps_taken[next] = current_steps + 1

print(period, acceleration_factor, sorted({k: f'{v:.2f}' for k, v in cyclic_speed_factors.items()}.items()))

print(total_plots_visited(steps_taken, evenness))

def calculate_plots_visited(steps):
    return acceleration_factor * steps ** 2 + cyclic_speed_factors[steps % period] * steps + cyclic_constants[steps % period]

print(calculate_plots_visited(STEP_GOAL))
