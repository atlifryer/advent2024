import sys

lines = sys.stdin.read().strip().split("\n\n")

matrices = []
for block in lines:
    matrix = [list(row) for row in block.split("\n")]
    matrices.append(matrix)


def compute_heights(matrix, reverse=False):
    if reverse:
        matrix = matrix[::-1]
    return [
        max((i for i, row in enumerate(matrix) if row[j] == "#"), default=-1)
        for j in range(len(matrix[0]))
    ]


keys_heights = []
locks_heights = []

for matrix in matrices:
    if all(cell == "#" for cell in matrix[0]):
        locks_heights.append(compute_heights(matrix))
    else:
        keys_heights.append(compute_heights(matrix, reverse=True))

valid_pairs = 0
for lock in locks_heights:
    for key in keys_heights:
        if all(l + k <= 5 for l, k in zip(lock, key)):
            valid_pairs += 1

print("Number of valid lock/key pairs:", valid_pairs)
