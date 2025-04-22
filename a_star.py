''' 

콘솔창으로만 출력됨.

'''

import heapq

# 목표 상태
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# 초기 상태
INITIAL_STATE = [[4, 1, 3], [0, 2, 6], [7, 5, 8]]

# 맨해튼 거리 계산 함수 (휴리스틱)
def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:  # 빈칸 제외
                goal_x = (value - 1) // 3
                goal_y = (value - 1) % 3
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

# 퍼즐 상태를 문자열로 변환 (중복 상태 확인용)
def state_to_string(state):
    return ''.join(str(cell) for row in state for cell in row)

# 빈 칸의 위치 찾기
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# 빈 칸 이동 함수
def move_blank(state, direction):
    x, y = find_blank(state)
    new_state = [row[:] for row in state]
    if direction == "up" and x > 0:
        new_state[x][y], new_state[x-1][y] = new_state[x-1][y], new_state[x][y]
    elif direction == "down" and x < 2:
        new_state[x][y], new_state[x+1][y] = new_state[x+1][y], new_state[x][y]
    elif direction == "left" and y > 0:
        new_state[x][y], new_state[x][y-1] = new_state[x][y-1], new_state[x][y]
    elif direction == "right" and y < 2:
        new_state[x][y], new_state[x][y+1] = new_state[x][y+1], new_state[x][y]
    return new_state

# A* 알고리즘 구현 + 탐색 트리 저장
def a_star_with_tree(initial_state):
    priority_queue = []
    visited_states = set()
    
    # 탐색 트리 저장용 리스트
    search_tree = []
    
    # 초기 상태 추가
    heapq.heappush(priority_queue, (manhattan_distance(initial_state), initial_state, [], 0))
    
    while priority_queue:
        _, current_state, path, g_cost = heapq.heappop(priority_queue)
        
        # 현재 상태를 탐색 트리에 추가
        search_tree.append((current_state, path))
        
        # 목표 상태 도달 시 경로 반환 및 트리 출력
        if current_state == GOAL_STATE:
            return path, search_tree
        
        # 현재 상태를 문자열로 변환하여 방문 확인
        state_str = state_to_string(current_state)
        if state_str in visited_states:
            continue
        visited_states.add(state_str)
        
        # 빈 칸 이동 방향
        for direction in ["up", "down", "left", "right"]:
            next_state = move_blank(current_state, direction)
            next_path = path + [direction]
            next_g_cost = g_cost + 1
            next_h_cost = manhattan_distance(next_state)
            heapq.heappush(priority_queue, (next_g_cost + next_h_cost, next_state, next_path, next_g_cost))

# 실행 및 탐색 트리 출력
solution_path, search_tree = a_star_with_tree(INITIAL_STATE)

print("해결 경로:", solution_path)
print("\n탐색 트리:")
for idx, (state, path) in enumerate(search_tree):
    print(f"노드 {idx}:")
    for row in state:
        print(row)
    print(f"경로: {path}\n")
