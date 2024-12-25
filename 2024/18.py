import sys
from collections import deque
import copy

direction_map = {
    "^": (-1, 0),  # up
    ">": (0, 1),  # right
    "v": (1, 0),  # down
    "<": (0, -1),  # left
}

raw_data = sys.stdin.read().strip().split("\n")
byte_positions = [line.split(",") for line in raw_data]

GLOBAL_H = 71
GLOBAL_W = 71

start = (0, 0)
end = (GLOBAL_H - 1, GLOBAL_W - 1)


def bfs(start, end, walls):
    queue = deque([(start[0], start[1], 0)])
    visited = set()

    while queue:
        row, col, cost = queue.popleft()

        if (row, col) == end:
            return cost

        if (row, col) in visited:
            continue
        visited.add((row, col,))

        for dr, dc in direction_map.values():
        	next_row, next_col = row + dr, col + dc
        	if 0 <= next_row < GLOBAL_H and 0 <= next_col < GLOBAL_W and (next_row, next_col) not in walls:
        		queue.append((next_row, next_col, cost + 1))

    return -1


# part 1
formatted_data = {(int(y), int(x)) for x, y in byte_positions[:1024]}
print("Part 1:")
print(bfs(start, end, formatted_data))

# part 2
print("Part 2:")
for i in range(1025, len(byte_positions)):
	formatted_data = {(int(y), int(x)) for x, y in byte_positions[:i]}
	if bfs(start, end, formatted_data) == -1:
		print(i)
		break
print(byte_positions[:i][-1])
