import heapq
from graphviz import Digraph
import hashlib
import os

os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"


# 목표 상태
GOAL = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def heuristic(state):
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


def generate_successors_extended(state):
    y, x = find_blank(state)
    successors = []
    
    # 1칸 이동
    for dy, dx in MOVES:
        ny, nx = y + dy, x + dx
        if 0 <= ny < 3 and 0 <= nx < 3:
            new_state = [list(row) for row in state]
            new_state[y][x], new_state[ny][nx] = new_state[ny][nx], new_state[y][x]
            successors.append(state_to_tuple(new_state))

    # 2칸 이동
    for dy, dx in MOVES:
        ny1, nx1 = y + dy, x + dx       # 중간 타일
        ny2, nx2 = y + 2*dy, x + 2*dx   # 끝 타일
        # 중간과 끝 타일이 모두 보드 내에 있는지 확인
        if 0 <= ny1 < 3 and 0 <= nx1 < 3 and 0 <= ny2 < 3 and 0 <= nx2 < 3:
            new_state = [list(row) for row in state]
            # 빈칸과 끝 타일 교환, 중간 타일과 교환된 빈칸(원래 끝 타일 값) 교환
            new_state[y][x], new_state[ny2][nx2] = new_state[ny2][nx2], new_state[y][x] # 0 <-> val2
            new_state[ny1][nx1], new_state[y][x] = new_state[y][x], new_state[ny1][nx1] # val1 <-> val2 (원래 val2가 있던 자리에 val1이 감)
            successors.append(state_to_tuple(new_state))
            
    return successors


def a_star(start):
    open_set = []
    heapq.heappush(open_set, (heuristic(start), 0, start, []))

    visited = set()
    visited_order = []
    tree = {}  # parent -> [children]
    fn_values = {}  # state -> (g, h)

    while open_set:
        f, g, current, path = heapq.heappop(open_set)

        if current in visited:
            continue

        visited.add(current)
        visited_order.append(current)
        fn_values[current] = (g, heuristic(current))

        if current == GOAL:
            return path + [current], visited_order, tree, fn_values

        for neighbor in generate_successors_extended(current):
            if neighbor not in visited:
                heapq.heappush(
                    open_set,
                    (g + 1 + heuristic(neighbor), g + 1, neighbor, path + [current]),
                )
                tree.setdefault(current, []).append(neighbor)

    return None, visited_order, tree, fn_values


# ---------- 시각화 ----------


def format_state(state):
    return "\n".join(
        [" ".join(str(c) if c != 0 else "_" for c in row) for row in state]
    )


def state_to_id(state):
    return hashlib.md5(str(state).encode()).hexdigest()


def visualize_tree(tree, fn_values, visited_order, goal, filename="a_star_tree"):
    dot = Digraph(comment="A* Search Tree")
    dot.attr(rankdir="TB", size="10")

    # 모든 노드를 수집 (tree의 키와 값들 포함)
    all_states = set(fn_values.keys())
    for parent, children in tree.items():
        all_states.add(parent)
        all_states.update(children)

    for state in all_states:
        node_id = state_to_id(state)
        if state in fn_values:
            g, h = fn_values[state]
            label = format_state(state) + f"\n{g} + {h} = {g + h}"
        else:
        # 부모 노드를 통해 g 값을 계산
            parent_state = next(
                (parent for parent, children in tree.items() if state in children), None
            )
            if parent_state and parent_state in fn_values:
                parent_g, _ = fn_values[parent_state]
                g = parent_g + 1  # 부모 g값 + 1
            else:
                g = 0  # 루트 노드에 가까운 경우 기본값
            h = heuristic(state)
            label = format_state(state) + f"\n{g} + {h} = {g + h}"
        shape = "box"
        style = "solid" if state in visited_order else "dashed"
        fillcolor = "#a0ffa0" if state == goal else "#ffffff"
        dot.node(node_id, label=label, shape=shape, style=style, fillcolor=fillcolor, fontname="Arial" )

    for parent, children in tree.items():
        for child in children:
            dot.edge(state_to_id(parent), state_to_id(child))

    output_path = dot.render(filename, format="png", cleanup=False)
    print(f"[✅] 탐색 트리 저장됨: {output_path}")


# ---------- 실행 ----------

if __name__ == "__main__":
    start_state = ((4, 1, 3), (0, 2, 6), (7, 5, 8))

    solution, visited_order, tree, fn_values = a_star(start_state)

    if solution:
        for i, state in enumerate(solution):
            print(f"Step {i}:")
            for row in state:
                print(row)
            print()
    else:
        print("해결 불가")

    visualize_tree(tree, fn_values, visited_order, GOAL)
