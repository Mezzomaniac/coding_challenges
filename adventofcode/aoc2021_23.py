from downloader import download
from functools import lru_cache
from queue import PriorityQueue

download(2021, 23)
with open('aoc2021_23input.txt') as inputfile:
    data = inputfile.read()
print(data)

# part 1:
spaces = ('',) * 11 + tuple('BBCCADDA')
room_length = 2

# part 2:
spaces = ('',) * 11 + tuple('BDDBCCBCABADDACA')
room_length = 4

amphipod_rooms = dict(zip('ABCD', (range(i, i + room_length) for i in range(11, 11 + 5 * room_length, room_length))))
amphipod_doors = dict(zip('ABCD', range(2, 9, 2)))
room_doors = {room: (room - 11 + room_length) // room_length * 2 for room in range(11, 11 + 4 * room_length)}
exit_rooms = {room: (room - 11 + room_length) // room_length * room_length + 11 - room_length for room in range(11, 11 + 4 * room_length)}

GOAL = ''.join(amphipod * room_length for amphipod in 'ABCD')

costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

@lru_cache()
def find_path(start, target):
    if target > start:
        return set(range(target, start, -1))
    else:
        return set(range(target, start))

def available_spaces(spaces, current_index):
    amphipod = spaces[current_index]
    if not amphipod:
        return {}
    start = current_index
    room_exit_steps = 0
    if current_index > 10:
        start = room_doors[current_index]
        room_exit_indices = range(exit_rooms[current_index], current_index)
        if any(spaces[index] for index in room_exit_indices):
            # exit from current room is blocked
            return {}
        room_exit_steps = len(room_exit_indices) + 1
    # first try moving into a target room:
    target_room_indices = amphipod_rooms[amphipod]
    target_door_index = amphipod_doors[amphipod]
    path_indices = find_path(start, target_door_index)
    path_indices.add(target_room_indices[0])
    steps = len(path_indices) + room_exit_steps
    if any(spaces[index] for index in path_indices) or any(spaces[index] not in (amphipod, '') for index in target_room_indices[1:]):
        # path is blocked or target room has a foreigner
        pass
    else:
        for target_room_steps, room_index in reversed(tuple(enumerate(target_room_indices))):
            if not spaces[room_index]:
                return {room_index: (steps + target_room_steps) * costs[amphipod]}
    if current_index in range(11):
        # in hallway so can only move to room
        return {}
    # next try moving into the hallway:
    options = {}
    for target in range(11):
        if target in range(2, 9, 2):
            continue
        path_indices = find_path(start, target)
        if not any(spaces[index] for index in path_indices):
            steps = len(path_indices) + room_exit_steps
            options[target] = steps * costs[amphipod]
    return options

@lru_cache(maxsize=16384)
def rate_progress(spaces):
    return -sum(goal == room for goal, room in zip(GOAL, spaces[11:]))

frontier = PriorityQueue()
frontier.put((0, rate_progress(spaces), spaces))
visited = {spaces: 0}
best_progress = 0
while not frontier.empty():
    current_cost, current_progress, current_spaces = frontier.get()
    if current_progress < best_progress:
        best_progress = current_progress
        print(best_progress)
        #print(current_spaces)
        #print(current_cost)
        if current_progress == 11 - len(spaces):
            print(visited[current_spaces])
            break
    for current_index in range(len(spaces)):
        for new_index, cost in available_spaces(current_spaces, current_index).items():
            new_spaces = list(current_spaces)
            new_spaces[current_index] = ''
            new_spaces[new_index] = current_spaces[current_index]
            new_spaces = tuple(new_spaces)
            new_cost = current_cost + cost
            if new_spaces not in visited or new_cost < visited[new_spaces]:
                visited[new_spaces] = new_cost
                frontier.put((new_cost, rate_progress(new_spaces), new_spaces))

