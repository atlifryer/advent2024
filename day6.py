import sys

guard_map = sys.stdin.read().strip().split("\n")

# identify starting position of guard
for i, line in enumerate(guard_map):
    if "^" in line:
        start_row = i
        start_col = line.index("^")
        break

# dimensions of the map
row_amount = len(guard_map) - 1
col_amount = len(guard_map[0]) - 1

# initial guard direction
guard_direction = guard_map[start_row][start_col]

direction_map = {
    "^": (-1, 0),  # up
    ">": (0, 1),  # right
    "v": (1, 0),  # down
    "<": (0, -1),  # left
}


def guard_cannot_leave(row, col, guard_direction):
    if (
        (row == 0 and guard_direction == "^")
        or (row == row_amount and guard_direction == "v")
        or (col == 0 and guard_direction == "<")
        or (col == col_amount and guard_direction == ">")
    ):
        return False
    return True


def turn_right(guard_direction):
    right_turn_map = {
        "^": ">",
        ">": "v",
        "v": "<",
        "<": "^",
    }
    return right_turn_map.get(guard_direction)


row, col = start_row, start_col


def in_loop(row, col, guard_direction):
    positions = set()
    _, loop, _ = make_path(row, col, guard_direction, positions)
    return loop


def make_path(row, col, guard_direction, positions):
    original_path = set()
    loop = False
    next_square = guard_map[row][col]
    i = 0  # dumnb ass fuck way to ignore start position
    while guard_cannot_leave(row, col, guard_direction):
        i += 1
        if (row, col, guard_direction) in positions:
            loop = True
            break
        positions.add((row, col, guard_direction))
        if i != 1:
            original_path.add((row, col))

        move_row, move_col = direction_map.get(guard_direction)
        if next_square != "#":
            next_square = guard_map[row + move_row][col + move_col]
            while next_square == "#":
                guard_direction = turn_right(guard_direction)
                move_row, move_col = direction_map.get(guard_direction)
                next_square = guard_map[row + move_row][col + move_col]

            row += move_row
            col += move_col

    original_path.add((row, col))

    return guard_map, loop, original_path


positions: set = set()
path, loop, original_path = make_path(row, col, guard_direction, positions)


def how_many_loops(guard_map, row, col):
    loop_positions = 0
    for r in range(len(guard_map)):
        row_list = list(guard_map[r])
        for c in range(len(row_list)):
            if (r, c) in original_path:
                if row_list[c] != "#":
                    original_char = row_list[c]
                    row_list[c] = "#"
                    guard_map[r] = "".join(row_list)

                    loop = in_loop(row, col, guard_direction)
                    if loop:
                        loop_positions += 1

                    row_list[c] = original_char
                    guard_map[r] = "".join(row_list)
    return loop_positions


loop_amount = how_many_loops(guard_map, start_row, start_col)
print(loop_amount)
