import sys
from collections import deque

raw_data = sys.stdin.read().strip().split("\n")
robot_map = [list(row) for row in raw_data[: raw_data.index("")]]
moves = list("".join(raw_data[raw_data.index("") + 1 :]))


def positions(matrix, two=False):
    # identify starting position of robot
    for i, line in enumerate(matrix):
        if "@" in line:
            robot_pos = (i, line.index("@"))
            continue

    # identify box positions
    if two:
        box_positions = {
            (i, j, char)
            for i, line in enumerate(matrix)
            for j, char in enumerate(line)
            if char == "[" or char == "]"
        }
    else:
        box_positions = {
            (i, j)
            for i, line in enumerate(matrix)
            for j, char in enumerate(line)
            if char == "O"
        }

    # identify wall positions
    wall_positions = {
        (i, j)
        for i, line in enumerate(matrix)
        for j, char in enumerate(line)
        if char == "#"
    }

    return robot_pos, box_positions, wall_positions


robot_pos, box_positions, wall_positions = positions(robot_map)


direction_map = {
    "^": (-1, 0),  # up
    ">": (0, 1),  # right
    "v": (1, 0),  # down
    "<": (0, -1),  # left
}


def move_robot(robot_pos, box_positions, direction):
    dr, dc = direction_map[direction]
    next_pos = (robot_pos[0] + dr, robot_pos[1] + dc)

    if next_pos in wall_positions:
        return robot_pos, box_positions

    if next_pos in box_positions:
        box_row, box_col = next_pos
        boxes_to_move = []

        while (box_row, box_col) in box_positions:
            boxes_to_move.append((box_row, box_col))
            box_row += dr
            box_col += dc

        if (box_row, box_col) in wall_positions or (box_row, box_col) in box_positions:
            return robot_pos, box_positions

        for br, bc in reversed(boxes_to_move):
            box_positions.remove((br, bc))
            box_positions.add((br + dr, bc + dc))

    robot_pos = next_pos
    return robot_pos, box_positions


def calculate_gps_sum(box_positions, two=False):
    if two:
        bpos = []
        for r, c, char in box_positions:
            if char == "[":
                bpos.append((r, c))
    else:
        return sum(100 * row + col for row, col in box_positions)

    return sum(100 * row + col for row, col in bpos)


for move in moves:
    robot_pos, box_positions = move_robot(robot_pos, box_positions, move)

# part 1
print("GPS sum:", calculate_gps_sum(box_positions))

# part 2


def make_larger(grid):
    larger_grid = []

    for row in grid:
        new_row = []
        for char in row:
            if char == "#":
                new_row.extend(["#", "#"])
            elif char == "O":
                new_row.extend(["[", "]"])
            elif char == ".":
                new_row.extend([".", "."])
            elif char == "@":
                new_row.extend(["@", "."])
        larger_grid.append("".join(new_row))

    return larger_grid


def get_vertical_cluster(start_positions, box_positions, dr):
    cluster = set(start_positions)

    for r, c, s in list(cluster):
        if s == "[" and (r, c + 1, "]") in box_positions:
            cluster.add((r, c + 1, "]"))
        elif s == "]" and (r, c - 1, "[") in box_positions:
            cluster.add((r, c - 1, "["))

    while True:
        new_found = False
        current_layer = list(cluster)
        for r, c, s in current_layer:
            nr = r + dr
            for ns in ["[", "]"]:
                if (nr, c, ns) in box_positions and (nr, c, ns) not in cluster:
                    cluster.add((nr, c, ns))
                    new_found = True
                    if ns == "[" and (nr, c + 1, "]") in box_positions:
                        cluster.add((nr, c + 1, "]"))
                    elif ns == "]" and (nr, c - 1, "[") in box_positions:
                        cluster.add((nr, c - 1, "["))
        if not new_found:
            break

    return cluster


def can_move_cluster(cluster, dr, dc, wall_positions):
    for row, col, _ in cluster:
        if (row + dr, col + dc) in wall_positions:
            return False
    return True


def move_cluster(cluster, dr, dc, box_positions):
    new_positions = set((row + dr, col + dc, side) for row, col, side in cluster)

    for pos in cluster:
        box_positions.discard(pos)

    box_positions.update(new_positions)


def move_robot_2(robot_pos, box_positions, direction):
    dr, dc = direction_map[direction]
    next_pos = (robot_pos[0] + dr, robot_pos[1] + dc)
    sides = ["[", "]"]

    next_pos_boxes = [(robot_pos[0] + dr, robot_pos[1] + dc, side) for side in sides]

    if next_pos in wall_positions:
        return robot_pos, box_positions

    if any(box in box_positions for box in next_pos_boxes):
        if direction in ["<", ">"]:
            box_row, box_col = next_pos
            boxes_to_move = []

            while any((box_row, box_col, side) in box_positions for side in sides):
                box_side = "[" if (box_row, box_col, "[") in box_positions else "]"
                boxes_to_move.append((box_row, box_col, box_side))
                box_row += dr
                box_col += dc

            if (box_row, box_col) in wall_positions:
                return robot_pos, box_positions

            for br, bc, side in reversed(boxes_to_move):
                box_positions.remove((br, bc, side))
                box_positions.add((br + dr, bc + dc, side))

        elif direction in ["^", "v"]:
            next_box = (
                next_pos_boxes[0]
                if next_pos_boxes[0] in box_positions
                else next_pos_boxes[1]
            )
            cluster = get_vertical_cluster([next_box], box_positions, dr)
            if can_move_cluster(cluster, dr, dc, wall_positions):
                move_cluster(cluster, dr, dc, box_positions)
            else:
                return robot_pos, box_positions

    robot_pos = next_pos
    return robot_pos, box_positions


larger_grid = make_larger(robot_map)

robot_pos, box_positions, wall_positions = positions(larger_grid, two=True)

for move in moves:
    robot_pos, box_positions = move_robot_2(robot_pos, box_positions, move)

print("Part 2 GPS:", calculate_gps_sum(box_positions, two=True))
