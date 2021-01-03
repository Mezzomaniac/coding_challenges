import queue

def neighbors(point):
    return {(point[0] - 1, point[1]), (point[0], point[1] - 1), (point[0] + 1, point[1]), (point[0], point[1] + 1)}

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def wall(point):
    x, y = point
    number = x*x + 3*x + 2*x*y + y + y*y + 1352
    return bin(number).count('1') % 2

goal = (31, 39)
start = (1, 1)
costs = {start: 0}
frontier = queue.PriorityQueue()
frontier.put((0, start))
while not frontier.empty():
    current = frontier.get()[1]
    if current == goal:
        print(costs[current])
        break
    for next in neighbors(current):
        if -1 in next or wall(next):
            continue
        cost = costs[current] + 1
        if cost < costs.get(next, cost + 1):
            costs[next] = cost
            priority = cost + distance(next, goal)
            frontier.put((priority, next))

start = (1, 1)
costs = {start: 0}
frontier = queue.Queue()
frontier.put(start)
while not frontier.empty():
    current = frontier.get()
    for next in neighbors(current):
        if -1 in next or wall(next):
            continue
        cost = costs[current] + 1
        if 51 > cost < costs.get(next, cost + 1):
            costs[next] = cost
            frontier.put(next)
print(len(costs))
