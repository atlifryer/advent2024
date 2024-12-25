import sys


text = [
    list(line.strip()) for line in sys.stdin.read().strip().split("\n") if line.strip()
]


def check_pattern(grid, pattern):
    rows = len(grid)
    cols = len(grid[0])
    pattern_len = len(pattern)
    count = 0

    def count_matches(start_row, start_col, d_row, d_col):
        for i in range(pattern_len):
            r = start_row + i * d_row
            c = start_col + i * d_col
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return 0
            if grid[r][c] != pattern[i]:
                return 0
        return 1

    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
    ]

    for row in range(rows):
        for col in range(cols):
            for d_row, d_col in directions:
                count += count_matches(row, col, d_row, d_col)

    return count


def count_x_pattern(grid, pattern):
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    reverse_pattern = pattern[::-1]
    patterns = [pattern, reverse_pattern]

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != "A":
                continue

            for pat_diagonal1 in patterns:
                for pat_diagonal2 in patterns:
                    match = True

                    positions_diag1 = [
                        (row - 1, col - 1, pat_diagonal1[0]),
                        (row + 1, col + 1, pat_diagonal1[2]),
                    ]

                    positions_diag2 = [
                        (row - 1, col + 1, pat_diagonal2[0]),
                        (row + 1, col - 1, pat_diagonal2[2]),
                    ]

                    for r, c, expected_char in positions_diag1:
                        if 0 <= r < rows and 0 <= c < cols:
                            if grid[r][c] != expected_char:
                                match = False
                                break
                        else:
                            match = False
                            break

                    if not match:
                        continue

                    for r, c, expected_char in positions_diag2:
                        if 0 <= r < rows and 0 <= c < cols:
                            if grid[r][c] != expected_char:
                                match = False
                                break
                        else:
                            match = False
                            break

                    if match:
                        count += 1
                        break

    return count


pattern = "MAS"

print(count_x_pattern(text, pattern))
