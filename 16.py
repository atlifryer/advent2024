import sys
import heapq

direction_map = {
    "^": (-1, 0),  # up
    ">": (0, 1),  # right
    "v": (1, 0),  # down
    "<": (0, -1),  # left
}

directions = ["^", ">", "v", "<"]

raw_data = sys.stdin.read().strip().split("\n")
maze = [list(row) for row in raw_data]


def positions(matrix, two=False):
    for i, line in enumerate(matrix):
        if "S" in line:
            start = (i, line.index("S"))
            continue

    for i, line in enumerate(matrix):
        if "E" in line:
            end = (i, line.index("E"))
            continue

    wall_positions = {
        (i, j)
        for i, line in enumerate(matrix)
        for j, char in enumerate(line)
        if char == "#"
    }

    return start, end, wall_positions


def bfs(start, end, walls):
    pq = [(0, start[0], start[1], ">")]
    visited = set()

    while pq:
        cost, row, col, direction = heapq.heappop(pq)

        if (row, col) == end:
            return cost

        if (row, col, direction) in visited:
            continue
        visited.add((row, col, direction))

        dr, dc = direction_map[direction]
        next_row, next_col = row + dr, col + dc
        if (next_row, next_col) not in walls:
            heapq.heappush(pq, (cost + 1, next_row, next_col, direction))

        new_direction_cw = directions[(directions.index(direction) + 1) % 4]
        heapq.heappush(pq, (cost + 1000, row, col, new_direction_cw))

        new_direction_ccw = directions[(directions.index(direction) - 1) % 4]
        heapq.heappush(pq, (cost + 1000, row, col, new_direction_ccw))

    return -1


# part 1
start, end, walls = positions(maze)
GLOBAL_MIN_COST = bfs(start, end, walls)
print("Part 1:", GLOBAL_MIN_COST)


# part 2
def bfs2(start, end, walls):
    pq = [(0, start[0], start[1], ">", [(start[0], start[1])])]
    visited = {}
    paths = []

    while pq:
        cost, row, col, direction, path = heapq.heappop(pq)

        if cost > GLOBAL_MIN_COST:
            continue

        if (row, col) == end:
            if cost == GLOBAL_MIN_COST:
                paths.append(path)
            continue

        if (row, col, direction) in visited:
            prev_cost = visited[(row, col, direction)]
            if cost > prev_cost:
                continue
        else:
            visited[(row, col, direction)] = cost

        dr, dc = direction_map[direction]
        next_row, next_col = row + dr, col + dc
        if (next_row, next_col) not in walls:
            heapq.heappush(
                pq,
                (
                    cost + 1,
                    next_row,
                    next_col,
                    direction,
                    path + [(next_row, next_col)],
                ),
            )

        new_direction_cw = directions[(directions.index(direction) + 1) % 4]
        heapq.heappush(pq, (cost + 1000, row, col, new_direction_cw, path))

        new_direction_ccw = directions[(directions.index(direction) - 1) % 4]
        heapq.heappush(pq, (cost + 1000, row, col, new_direction_ccw, path))

    return paths


start, end, walls = positions(maze)
optimal_paths = bfs2(start, end, walls)
unique_tiles = set()
for path in optimal_paths:
    unique_tiles.update(path)

print("Part 2:", len(unique_tiles))
