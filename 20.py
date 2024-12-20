import sys
from collections import deque, defaultdict

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def read_maze():
    raw_data = sys.stdin.read().strip().split("\n")
    maze = [list(row) for row in raw_data]
    return maze

def positions(maze):
    start = end = None
    walls = set()
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'S':
                start = (i, j)
            elif cell == 'E':
                end = (i, j)
            elif cell == '#':
                walls.add((i, j))
    return start, end, walls

def bfs(maze, start, end=None, allow_walls=False, max_steps=float('inf')):
    queue = deque()
    queue.append((start[0], start[1], 0))
    visited = {}
    visited[(start[0], start[1])] = 0

    while queue:
        r, c, steps = queue.popleft()

        if end and (r, c) == end:
            return steps

        if steps >= max_steps:
            continue

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]):
                if allow_walls or maze[nr][nc] != '#':
                    if ((nr, nc) not in visited) or (steps + 1 < visited[(nr, nc)]):
                        visited[(nr, nc)] = steps + 1
                        queue.append((nr, nc, steps + 1))
    return visited

def reconstruct_path(maze, D_start, D_end, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (nr, nc) in D_start and D_start[(nr, nc)] == D_start[current] - 1:
                current = (nr, nc)
                break
    path.append(start)
    path.reverse()
    return path

def compute_all_distances(maze, start, end):
    D_start = bfs(maze, start) # how far to start from every point
    D_end = bfs(maze, end) # how far to end from every point
    return D_start, D_end

def find_cheats(maze, path, D_start, D_end, max_cheat_duration, min_saving):
    cheat_count = 0
    unique_cheats = set()

    path_set = set(path)

    for idx, (x, y) in enumerate(path): # check each point on the path
        queue = deque()
        queue.append((x, y, 0))
        visited = {}
        visited[(x, y)] = 0

        while queue:
            r, c, steps = queue.popleft()

            if steps > max_cheat_duration:
                continue

            if (r, c) in path_set and (r, c) != (x, y):
                original_segment_length = D_start[(r, c)] - D_start[(x, y)]
                saving = original_segment_length - steps
                if saving >= min_saving: # checks if cheat is "valid" (saves >=100)
                    unique_cheats.add(((x, y), (r, c)))
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]):
                    if (maze[nr][nc] != '#' or steps < max_cheat_duration):
                        if ((nr, nc) not in visited) or (steps + 1 < visited[(nr, nc)]):
                            visited[(nr, nc)] = steps + 1
                            queue.append((nr, nc, steps + 1))
    
    cheat_count = len(unique_cheats)
    return cheat_count

maze = read_maze()
start, end, walls = positions(maze)

# compute all distances
D_start, D_end = compute_all_distances(maze, start, end)

# get original path
path = reconstruct_path(maze, D_start, D_end, start, end)
original_time = D_start[end]
min_saving = 100

# part 1
max_cheat_duration = 2
cheat_saves = find_cheats(maze, path, D_start, D_end, max_cheat_duration, min_saving)
print("Part 1:", cheat_saves)

# part 2
max_cheat_duration = 20
cheat_saves = find_cheats(maze, path, D_start, D_end, max_cheat_duration, min_saving)
print("Part 2:", cheat_saves)