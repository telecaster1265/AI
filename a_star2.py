import heapq
from collections import deque

# Goal state
GOAL = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

# Moves: (dy, dx)
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def heuristic(state):
    # Manhattan distance
    dist = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val == 0:
                continue
            goal_y = (val - 1) // 3
            goal_x = (val - 1) % 3
            dist += abs(i - goal_y) + abs(j - goal_x)
    return dist


def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j


def state_to_tuple(state):
    return tuple(tuple(row) for row in state)


def generate_successors(state):
    y, x = find_blank(state)
    successors = []
    for dy, dx in MOVES:
        ny, nx = y + dy, x + dx
        if 0 <= ny < 3 and 0 <= nx < 3:
            new_state = [list(row) for row in state]
            new_state[y][x], new_state[ny][nx] = new_state[ny][nx], new_state[y][x]
            successors.append(state_to_tuple(new_state))
    return successors


def a_star(start):
    open_set = []
    heapq.heappush(open_set, (heuristic(start), 0, start, []))
    visited = set()

    while open_set:
        f, g, current, path = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.add(current)

        if current == GOAL:
            return path + [current]

        for neighbor in generate_successors(current):
            if neighbor not in visited:
                heapq.heappush(open_set, (g + 1 + heuristic(neighbor), g + 1, neighbor, path + [current]))
    return None


# Example: initial state from your image
start_state = (
    (4, 1, 3),
    (0, 2, 6),
    (7, 5, 8)
)

solution = a_star(start_state)

if solution:
    for i, state in enumerate(solution):
        print(f"Step {i}:")
        for row in state:
            print(row)
        print()
else:
    print("No solution found.")
