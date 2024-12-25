import sys
from functools import lru_cache

content = sys.stdin.read()
lines = content.strip().splitlines()
matrix = [list(map(int, line.strip())) for line in lines]


# part 1
def find_number(matrix, number):
    return [
        (x, y)
        for x in range(len(matrix))
        for y in range(len(matrix[0]))
        if matrix[x][y] == number
    ]


def neighbors(matrix, row, col):
    directions = [1, -1, 1j, -1j]  # trying out imaginary numbers for 2d movement
    nbs = []

    at = row + col * 1j
    for drctn in directions:
        nb = at + drctn
        ni, nj = int(nb.real), int(nb.imag)
        if 0 <= ni < len(matrix) and 0 <= nj < len(matrix[0]):
            nbs.append((ni, nj, matrix[ni][nj]))
    return nbs


def dfs(matrix, row, col, visited, targets, step=1):
    stack = [(row, col, matrix[row][col])]

    while stack:
        curr_row, curr_col, curr_val = stack.pop()

        visited.add((curr_row, curr_col))

        if curr_val in targets:
            targets[curr_val].add((curr_row, curr_col))
            continue

        for ni, nj, nb_val in neighbors(matrix, curr_row, curr_col):
            if nb_val == curr_val + step and (ni, nj) not in visited:
                stack.append((ni, nj, nb_val))


def score(matrix):
    trailheads = find_number(matrix, 0)
    scores = {}

    for row, col in trailheads:
        visited = set()
        targets = {9: set()}
        dfs(matrix, row, col, visited, targets, step=1)
        scores[(row, col)] = len(targets[9])

    return scores


print("Part 1:")
scores = score(matrix)
score_sum = 0
for trailhead, score_num in scores.items():
    score_sum += score_num
print("Total score:", score_sum)


# part 2
@lru_cache(None)  # eh cache memoization shit sem gpt sagði mer að gera, veisla
def dfs_part2(row, col, curr_val):
    if curr_val == 9:
        return 1

    total_paths = 0

    for ni, nj, nb_val in neighbors(matrix, row, col):
        if nb_val == curr_val + 1:
            total_paths += dfs_part2(ni, nj, nb_val)

    return total_paths


def score_part2(matrix):
    trailheads = find_number(matrix, 0)
    total_paths = 0

    for row, col in trailheads:
        total_paths += dfs_part2(row, col, matrix[row][col])

    return total_paths


print("Part 2:")
total_paths = score_part2(matrix)
print("Total number of distinct paths:", total_paths)
