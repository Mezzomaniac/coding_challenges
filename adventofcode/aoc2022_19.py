from downloader import download
from dataclasses import dataclass, asdict, astuple
from functools import lru_cache
from math import ceil
from typing import Tuple, Dict
from queue import PriorityQueue, Queue
from time import time

download(2022, 19)
with open('aoc2022_19input.txt') as inputfile:
    data = inputfile.read()
test = '''Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'''
#data = test
print(data)

@dataclass(frozen=True)
class Blueprint:
    id: int
    ore_robot_cost: Dict[str, int]
    clay_robot_cost: Dict[str, int]
    obsidian_robot_cost: Dict[str, int]
    geode_robot_cost: Dict[str, int]
    
    max_ore_cost: int
    max_clay_cost: int
    max_obsidian_cost: int

@dataclass(frozen=True)
class State:
    geodes: int=0
    geode_robots: int=0
    obsidian: int=0
    obsidian_robots: int=0
    clay: int=0
    clay_robots: int=0
    ore: int=2
    ore_robots: int=1
    
    time_to_first_obsidian_robot: int=32
    enough_obsidian_robots: bool=False
    enough_clay_robots: bool=False
    enough_ore_robots: bool=False

    def __lt__(self, other):
        this = astuple(self)[:8]
        other = astuple(other)[:8]
        return strictly_lt(this, other)

blueprints = []
for line in data.splitlines():
    words = line.split()
    id = int(words[1][:-1])
    ore_robot_cost = {words[7].strip('.'): int(words[6])}
    clay_robot_cost = {words[13].strip('.'): int(words[12])}
    obsidian_robot_cost = {words[19]: int(words[18]), words[22].strip('.'): int(words[21])}
    geode_robot_cost = {words[28]: int(words[27]), words[31].strip('.'): int(words[30])}
    max_ore_cost = max(robot_cost['ore'] for robot_cost in (ore_robot_cost, clay_robot_cost, obsidian_robot_cost, geode_robot_cost))
    max_clay_cost = obsidian_robot_cost['clay']
    max_obsidian_cost = geode_robot_cost['obsidian']
    blueprint = Blueprint(id, ore_robot_cost, clay_robot_cost, obsidian_robot_cost, geode_robot_cost, max_ore_cost, max_clay_cost, max_obsidian_cost)
    blueprints.append(blueprint)

robots = ('geode', 'obsidian', 'clay', 'ore')

deadline = 24
deadline = 32

@lru_cache(maxsize=4194304)
def strictly_lt(a: tuple, b: tuple):
    return a < b and all(field1 <= field2 for field1, field2 in zip(a, b))

def triangle_number(n):
    return (n ** 2 + n) // 2

triangle_numbers = [triangle_number(n) for n in range(deadline)]

@lru_cache(maxsize=None)
def min_turns_to_produce(amount, rate):
    for turns in range(deadline):
        if triangle_numbers[max(turns - 1, 0)] + rate * turns >= amount:
            return turns

@lru_cache(maxsize=None)
def turns_to_produce(amount, rate):
    return ceil(amount / rate)

def calculate_next_state_dict(state, minutes=1):
    state_dict = asdict(state)
    state_dict['ore'] += state.ore_robots * minutes
    state_dict['clay'] += state.clay_robots * minutes
    state_dict['obsidian'] += state.obsidian_robots * minutes
    state_dict['geodes'] += state.geode_robots * minutes
    return state_dict

def turns_to_build_robot(blueprint, state, robot):
    return max((cost - getattr(state, resource)) / getattr(state, f'{resource}_robots') for resource, cost in getattr(blueprint, f'{robot}_robot_cost').items())

"""def turns_to_build_robot2(blueprint, state, robot, verbose=False):
    robot_cost = getattr(blueprint, f'{robot}_robot_cost')
    turns_required_until_enough_ore = min_turns_to_produce(robot_cost['ore'] - state.ore, state.ore_robots)
    if verbose:
        print('B', turns_required_until_enough_ore)
    if robot in ('ore', 'clay'):
        return turns_required_until_enough_ore
    other_required_resource = robots[robots.index(robot) + 1]
    turns_required_until_enough_other_resource = min_turns_to_produce(robot_cost[other_required_resource] - getattr(state, other_required_resource), getattr(state, f'{other_required_resource}_robots'))
    if verbose:
        print('C', turns_required_until_enough_other_resource)
    '''except ZeroDivisionError:
        turns_required_until_enough_other_resource = robot_cost[other_required_resource] + turns_to_build_robot2(blueprint, state, other_required_resource) + 1'''
    return max(turns_required_until_enough_ore, turns_required_until_enough_other_resource)"""

"""def decide_action(blueprint, state, minutes_left, verbose=False):
    if minutes_left == 1:
        return []
    #turns_required = {}
    #turns_required2 = {}
    robots_to_build = []
    for robot in robots:
        if getattr(state, f'enough_{robot}_robots', False):
            continue
        # Don't build a robot if it's too late to benefit
        if minutes_left <= 3 and robot in ('ore', 'obsidian') or minutes_left <= 5 and robot == 'clay':
            setattr(state, f'enough_{robot}_robots', True)
            continue
        # Don't build a type of robot if there're enough already
        if robot != 'geode' and getattr(state, f'{robot}_robots') >= max(cost for robot_cost in (getattr(blueprint, f'{each_robot}_robot_cost') for each_robot in robots) for resource, cost in robot_cost.items() if resource == robot):
            setattr(state, f'enough_{robot}_robots', True)
            if robot == 'obsidian':
                state.enough_clay_robots = True
            #if verbose and robot != 'ore':
                #print(robot)
            continue
        # Don't build a type of robot if there's already enough if its resource
        #if robot == 'clay' and 
        try:
            turns = turns_to_build_robot(blueprint, state, robot)
            #print(robot, turns)
        except ZeroDivisionError:
            #turns_required2[robot] = turns_to_build_robot2(blueprint, state, robot)
            continue
        if turns == 0:
            #if not turns_required:
                #return robot
            robots_to_build.append(robot)
            '''test_state = next_state(state)
            for resource, cost in getattr(blueprint, f'{robot}_robot_cost').items():
                setattr(test_state, resource, getattr(test_state, resource) - cost)
            setattr(test_state, f'{robot}_robots', getattr(test_state, f'{robot}_robots') + 1)
            test = [turns_to_build_robot2(blueprint, test_state, goal) <= goal_turns for goal, goal_turns in turns_required2.items()]
            #print(test)
            if True:#any(test):
            #if all(turns_to_build_robot2(blueprint, test_state, goal) + 1 <= goal_turns for goal, goal_turns in turns_required2.items()):
                return [robot]
                robots_to_build.append(robot)'''
                #if verbose:
                    #print('b')
                #return robot
        #turns_required[robot] = turns
        #turns_required2[robot] = turns_to_build_robot2(blueprint, state, robot)
    return robots_to_build"""

@lru_cache(maxsize=None)
def heuristic1(state_tuple):
    return  tuple(-field for field in state_tuple)[:8]

@lru_cache(maxsize=None)
def best_case_scenario(minutes_left, geodes, geode_robots, turns_to_build_geode_robot, verbose=False):
    minutes_available_for_new_geode_robots_to_produce_geodes = max(minutes_left - 1 - turns_to_build_geode_robot, 0)
    if verbose:
        print('A', minutes_available_for_new_geode_robots_to_produce_geodes)
    return geodes + geode_robots * minutes_left + triangle_numbers[minutes_available_for_new_geode_robots_to_produce_geodes]

def heuristic2(blueprint, state, minutes_left, verbose=False):
    turns_to_build_geode_robot = turns_to_build_robot2(blueprint, state, 'geode', verbose)
    if not state.obsidian_robots:
        turns_to_build_geode_robot += turns_to_build_robot2(blueprint, state, 'obsidian', verbose)
        if not state.clay_robots:
            turns_to_build_geode_robot += turns_to_build_robot2(blueprint, state, 'clay', verbose)
    return best_case_scenario(minutes_left, state.geodes, state.geode_robots, turns_to_build_geode_robot, verbose)

quality_level_total = 0
result = 1
for blueprint in blueprints[:3]:
    t = time()
    print(blueprint)
    
    @lru_cache(maxsize=None)
    def enough_obsidian(minutes_left, obsidian, obsidian_robots):
        return obsidian + obsidian_robots * (minutes_left - 2) >= blueprint.max_obsidian_cost * (minutes_left - 1)
    
    @lru_cache(maxsize=None)
    def enough_clay(minutes_left, clay, clay_robots):
        return clay + clay_robots * (minutes_left - 4) >= blueprint.max_clay_cost * (minutes_left - 3)
    
    @lru_cache(maxsize=None)
    def enough_ore(minutes_left, ore, ore_robots):
        part1needs = blueprint.max_ore_cost * (minutes_left - 5)
        part2needs = max(getattr(blueprint, f'{each_robot}_robot_cost')['ore'] for each_robot in robots if each_robot != 'clay') * 2
        part3needs = blueprint.geode_robot_cost['ore'] * 2
        return ore + ore_robots * (minutes_left - 2) >= part1needs + part2needs + part3needs
    
    best_geodes = 0
    elapsed = 2
    start = State()
    minutes = {start: elapsed}
    frontier = Queue()
    frontier.put((start, elapsed))
    #frontier = PriorityQueue()
    #priority = heuristic1(astuple(start))#, -heuristic2(blueprint, start, deadline - 1))
    #frontier.put((priority, start, elapsed))
    reached_obsidian_stage = False
    reached_geode_stage = False
    reached_second_geode_robot = False
    #rejected = set()
    while not frontier.empty():
        current_state, current_minute = frontier.get()
        #if current_state in rejected:
            #continue
        if current_minute > elapsed:
            print(current_minute, frontier.qsize(), len(minutes), time() - t)
            elapsed = current_minute
            #if current_minute > 28:
                #minutes = {state: minute for state, minute in minutes.items() if minute > current_minute - 5}
        if current_minute == deadline:
            if current_state.geodes > best_geodes:
                best_geodes = current_state.geodes
                print(best_geodes, frontier.qsize(), len(minutes), time() - t)
                minutes.clear()
            continue
        minutes_left = deadline - current_minute
        #if best_geodes == 9:
            #print(current_state, current_minute)
        next_state_dict = calculate_next_state_dict(current_state)
        next_states = set()
        for robot in robots:
            if minutes_left == 1:
                break
            if getattr(current_state, f'enough_{robot}_robots', False):
                #print('a')
                continue
            # Don't build a robot if it's too late to benefit
            if minutes_left <= 3 and robot in ('ore', 'obsidian') or minutes_left <= 5 and robot == 'clay':
                next_state_dict[f'enough_{robot}_robots'] = True
                #print('b', robot)
                continue
            # Don't build a type of robot if there're enough already
            if robot != 'geode' and getattr(current_state, f'{robot}_robots') >= getattr(blueprint, f'max_{robot}_cost'):
                next_state_dict[f'enough_{robot}_robots'] = True
                #print('c')
                if robot == 'obsidian':
                    next_state_dict['enough_clay_robots'] = True
                    #print('d')
                continue
            # Can we afford it?
            if not all(getattr(current_state, resource) >= cost for resource, cost in getattr(blueprint, f'{robot}_robot_cost').items()):
                continue
            # Don't build a type of robot if there's already enough of its resource
            if robot == 'obsidian' and enough_obsidian(minutes_left, current_state.obsidian, current_state.obsidian_robots):
                next_state_dict['enough_obsidian_robots'] = True
                #print('e', current_minute, current_state, enough_obsidian.cache_info())
                continue
            if robot == 'clay' and enough_clay(minutes_left, current_state.clay, current_state.clay_robots):
                next_state_dict['enough_clay_robots'] = True
                #print('f')
                continue
            if robot == 'ore' and enough_ore(minutes_left, current_state.ore, current_state.ore_robots):
                next_state_dict['enough_ore_robots'] = True
                #print('g')
                continue
            test_state_dict = next_state_dict.copy()
            for resource, cost in getattr(blueprint, f'{robot}_robot_cost').items():
                test_state_dict[resource] -= cost
            test_state_dict[f'{robot}_robots'] += 1
            if not current_state.obsidian_robots and robot == 'obsidian':
                next_state_dict['time_to_first_obsidian_robot'] = current_minute
            next_states.add(State(**test_state_dict))
        next_states.add(State(**next_state_dict))
        next_minute = current_minute + 1
        minutes_left = deadline - next_minute
        #count = 0
        for next_state in next_states:
            #print(next_state)
            if not reached_obsidian_stage and next_state.obsidian_robots:
                reached_obsidian_stage = current_minute
                #minutes.clear()
            elif reached_obsidian_stage and next_minute == reached_obsidian_stage + 2 + 1 and not next_state.obsidian_robots:
                continue
            if not reached_geode_stage and next_state.geode_robots:
                reached_geode_stage = current_minute
                #minutes.clear()
            elif reached_geode_stage and next_minute == reached_geode_stage + 1 and not next_state.geode_robots:
                continue
            if not reached_second_geode_robot and next_state.geode_robots == 2:
                reached_second_geode_robot = current_minute
                print('a')
            elif reached_second_geode_robot and  next_minute == reached_second_geode_robot + 3 and next_state.geode_robots < 2:
                continue
            '''put = True
            if reached_geode_stage:
                for state, minute in minutes.copy().items():
                    if next_state < state and next_minute >= minute:
                        put = False
                        break
                    elif state < next_state and minute >= next_minute:
                        del minutes[state]
                        rejected.add(state)'''
            if next_state not in minutes or minutes[next_state] > next_minute:
                #verbose = False#best_geodes == 8
                #best_possible = heuristic2(blueprint, next_state, minutes_left, verbose)
                #print(next_minute, next_state, turns_to_build_geode_robot, best_possible)
                #if verbose:
                    #print(next_state, next_minute, best_possible)
                #if best_possible <= best_geodes:
                    #continue
                minutes[next_state] = next_minute
                #priority = heuristic1(astuple(next_state))#, -best_possible)
                #frontier.put((priority, next_state, next_minute))
                frontier.put((next_state, next_minute))
                #count += 1
        #print(f'{count}/{len(next_states)}')
        #print()
    quality_level_total += best_geodes * blueprint.id
    result *= best_geodes
print(quality_level_total)
print(result)


'''quality_level_total = 0
for blueprint in blueprints:
    print(blueprint)
    frontier = Queue()
    frontier.put((State(), 0))
    best_quality = 0
    while not frontier.empty():
        state, elapsed = frontier.get()
        #print('a')
        for minute in range(elapsed, deadline):
            #print(minute)
            #print(state, '\n')
            verbose = True
            to_build = decide_action(blueprint, state, deadline - minute, verbose)
            state = calculate_next_state(state)
            if isinstance(to_build, str):
                for resource, cost in getattr(blueprint, f'{to_build}_robot_cost').items():
                    setattr(state, resource, getattr(state, resource) - cost)
                setattr(state, f'{to_build}_robots', getattr(state, f'{to_build}_robots') + 1)
            elif to_build:
                #print('b', to_build)
                for robot in to_build:
                    test_state = State(**asdict(state))
                    for resource, cost in getattr(blueprint, f'{robot}_robot_cost').items():
                        setattr(test_state, resource, getattr(test_state, resource) - cost)
                    setattr(test_state, f'{robot}_robots', getattr(test_state, f'{robot}_robots') + 1)
                    frontier.put((test_state, minute + 1))
        #print(state.geodes)
        #print('\n\n')
        if minute == deadline - 1:
            quality_level = state.geodes * blueprint.id
            best_quality = max(best_quality, quality_level)
    print(best_quality)
    quality_level_total += best_quality
print(quality_level_total)'''


'''from itertools import chain, product

blueprint_parameters = [(11, 9), (11, 10), (14, 10), (14, 8), (10, 10), (9, 8), (8, 7), (11, 8), (11, 9), (10, 8), (11, 10), (10, 8), (9, 12), (8, 7), (8, 7), (12, 9), (14, 8), (10, 7), (9, 8), (11, 11), (12, 8), (10, 7), (9, 8), (12, 9), (6, 7), (13, 9), (9, 7), (9, 9), (13, 9), (8, 7)]
test_data_blueprint_parameters = [(8, 7), (8, 7)]
#blueprint_parameters = test_data_blueprint_parameters

quality_level_total = 0
result = 1
for blueprint, parameters in list(zip(blueprints, blueprint_parameters))[0:1]:
    t = time()
    print(blueprint, parameters)
    ore_robot_cost = blueprint.ore_robot_cost['ore']
    clay_robot_cost = blueprint.clay_robot_cost['ore']
    obsidian_robot_cost_ore = blueprint.obsidian_robot_cost['ore']
    obsidian_robot_cost_clay = blueprint.obsidian_robot_cost['clay']
    geode_robot_cost_ore = blueprint.geode_robot_cost['ore']
    geode_robot_cost_obsidian = blueprint.geode_robot_cost['obsidian']
    
    #minutes_to_obsidian_robot = deadline
    clay_states = {}
    for course in product((None, 'ore', 'clay'), repeat=parameters[0] + 2):
        if 'clay' not in course:
            continue
        ore = 2
        ore_robots = 1
        clay = 0
        clay_robots = 0
        for minute, choice in enumerate(course, 1):
            if (choice == 'ore' and ore < ore_robot_cost) or (choice == 'clay' and ore < clay_robot_cost):
                break
            ore += ore_robots
            clay += clay_robots
            if choice == 'ore':
                ore_robots += 1
                ore -= ore_robot_cost
            elif choice == 'clay':
                clay_robots += 1
                ore -= clay_robot_cost
            if clay >= obsidian_robot_cost_clay and ore >= obsidian_robot_cost_ore:
                new_state = (ore, ore_robots, clay, clay_robots)
                if clay_states.get(new_state, deadline) > minute:
                    for state, minutes_required in clay_states.copy().items():
                        if strictly_lt(state, new_state) and minutes_required >= minute:
                            del clay_states[state]
                        elif strictly_lt(new_state, state) and minute >= minutes_required:
                            break
                    else:
                        clay_states[new_state] = minute
                break
    print(len(clay_states), set(clay_states.values()))
    
    #minutes_to_geode_robot = deadline
    obsidian_states = {}
    for i, (clay_state, minutes_to_obsidian_robot) in enumerate(clay_states.items()):
        #if not i % 2:
        print(i, len(obsidian_states), strictly_lt.cache_info())
        #print(clay_state, minutes_to_obsidian_robot)
        for i, course in enumerate(product((None, 'ore', 'clay', 'obsidian'), repeat=min(parameters[1] + 0, deadline - 2 - minutes_to_obsidian_robot - 1))):
            #if not i % 100000:
                #print(i)
            if 'obsidian' not in course:
                continue
            ore = clay_state[0]
            ore_robots = clay_state[1]
            clay = clay_state[2]
            clay_robots = clay_state[3]
            obsidian = 0
            obsidian_robots = 0
            for minute, choice in enumerate(course, 1):
                if (choice == 'ore' and ore < ore_robot_cost) or (choice == 'clay' and ore < clay_robot_cost) or (choice == 'obsidian' and (ore < obsidian_robot_cost_ore or clay < obsidian_robot_cost_clay)):
                    break
                ore += ore_robots
                clay += clay_robots
                obsidian += obsidian_robots
                if choice == 'ore':
                    ore_robots += 1
                    ore -= ore_robot_cost
                elif choice == 'clay':
                    clay_robots += 1
                    ore -= clay_robot_cost
                elif choice == 'obsidian':
                    obsidian_robots += 1
                    ore -= obsidian_robot_cost_ore
                    clay -= obsidian_robot_cost_clay
                if obsidian >= geode_robot_cost_obsidian and ore >= geode_robot_cost_ore:
                    new_state = (ore, ore_robots, clay, clay_robots, obsidian, obsidian_robots)
                    minute += minutes_to_obsidian_robot + 2
                    if obsidian_states.get(new_state, deadline - 1) > minute:
                        for state, minutes_required in obsidian_states.copy().items():
                            if strictly_lt(state, new_state) and minutes_required >= minute:
                                del obsidian_states[state]
                            elif strictly_lt(new_state, state) and minute >= minutes_required:
                                break
                        else:
                            obsidian_states[new_state] = minute
                        #print(strictly_lt.cache_info())
                    break
    print(len(obsidian_states), set(obsidian_states.values()))
    
    best_geodes = 0
    for i, (obsidian_state, minutes_to_geode_robot) in enumerate(obsidian_states.items()):
        minutes_per_phase = [deadline - 5, 2, 2, 1]
        phase = 0
        minutes_used = minutes_to_geode_robot
        if minutes_used >= deadline - 1:
            continue
        while minutes_used:
            if minutes_per_phase[phase] <= 0:
                phase += 1
                continue
            minutes_per_phase[phase] -= 1
            minutes_used -= 1
        #print(i, minutes_per_phase, best_geodes)
        if not i % 100:
            print(i)
        for i, course in enumerate(chain.from_iterable(permutation) for permutation in product(product((None, 'ore', 'clay', 'obsidian', 'geode'), repeat=minutes_per_phase[0]), product((None, 'ore', 'obsidian', 'geode'), repeat=minutes_per_phase[1]), product((None, 'geode'), repeat=minutes_per_phase[2]), product((None,), repeat=minutes_per_phase[3]))):
            course = list(course)
            #if not i % 100000:
                #print(i)
            #if 'geode' not in course:
            if course.count('geode') < minutes_per_phase[0] - 4:
                continue
            #print(i)
            ore = obsidian_state[0]
            ore_robots = obsidian_state[1]
            clay = obsidian_state[2]
            clay_robots = obsidian_state[3]
            obsidian = obsidian_state[4]
            obsidian_robots = obsidian_state[5]
            geodes = 0
            geode_robots = 0
            for minute, choice in enumerate(course, minutes_to_geode_robot + 1):
                if minute + min_turns_to_produce(best_geodes - geodes + 1, geode_robots) > deadline:
                    break
                if (choice == 'ore' and ore < ore_robot_cost) or (choice == 'clay' and ore < clay_robot_cost) or (choice == 'obsidian' and (ore < obsidian_robot_cost_ore or clay < obsidian_robot_cost_clay)) or (choice == 'geode' and (ore < geode_robot_cost_ore or obsidian < geode_robot_cost_obsidian)):
                    break
                ore += ore_robots
                clay += clay_robots
                obsidian += obsidian_robots
                geodes += geode_robots
                if choice == 'ore':
                    ore_robots += 1
                    ore -= ore_robot_cost
                elif choice == 'clay':
                    clay_robots += 1
                    ore -= clay_robot_cost
                elif choice == 'obsidian':
                    obsidian_robots += 1
                    ore -= obsidian_robot_cost_ore
                    clay -= obsidian_robot_cost_clay
                elif choice == 'geode':
                    geode_robots += 1
                    ore -= geode_robot_cost_ore
                    obsidian -= geode_robot_cost_obsidian
            if geodes > best_geodes:
                best_geodes = geodes
                print(best_geodes)
    print(best_geodes)
    quality_level_total += best_geodes * blueprint.id
    result *= best_geodes
    print(time() - t)
#print(quality_level_total)
print(result)

# 24-min results:
geode_results = [1, 0, 0, 0, 1, 5, 9, 2, 1, 3, 0, 3, 0, 8, 8, 0, 0, 5, 4, 0, 1, 5, 4, 0, 15, 0, 7, 3, 0, 8]  # 1699 is too low
# the 2 depth numbers refer to itertools.product repeats at the first 2 stages
geode_results_1_0_deeper = [1, 1, 0, 0, 1, 5, 9, 2, 1, 4, 0, 4, 0, 12, 8, 0, 0, 5, 5, 0, 1, 5, 5, 0, 15, 0, 7, 3, 0, 8]
geode_results_1_1_deeper = [1, 1, 0, 0, 1, 5, 9, 2, 1, 4, 0, 4, 0, 12, 8, 0, 0, 5, 5, 0, 1, 5, 5, 0, 15, 0, 7, 3, 0, 8]  # 1821 is too low
geode_results_2_0_deeper = [1, 1, 0, 0, 1, 5, 9, 2, 1, 4, 0, 4, 1, 12, 8, 0, 0, 5, 5, 0, 1, 5, 5, 0, 15, 0, 7, 3, 0, 8]  # 1834
geode_result_2_1_deeper = [1, 1, 0, 0]
geode_result_2_2_deeper = [1, 1, 0, 0]

# 32-min results:
# 1_0 depth:
[15, 15, 7]  # 1575 is too low
# 2_0 depth:
[15]'''
