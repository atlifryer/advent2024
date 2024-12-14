import sys
import time
import os

content = sys.stdin.read()
eqns = content.strip().split("\n")

robots: list = []

GLOBAL_W = 101
GLOBAL_H = 103

for robot in eqns:
    parts = robot.split(" ")
    px = int(parts[0].split("=")[1].split(",")[0])
    py = int(parts[0].split("=")[1].split(",")[1])
    vx = int(parts[1].split("=")[1].split(",")[0])
    vy = int(parts[1].split("=")[1].split(",")[1])
    robot_data = {
        "p": (px, py),
        "v": (vx, vy),
    }
    robots.append(robot_data)


def calc_pos(p, v, w, h, seconds):
    px, py = p
    vx, vy = v

    new_x = (px + vx * seconds) % w
    new_y = (py + vy * seconds) % h

    new_x = new_x if new_x >= 0 else new_x + w
    new_y = new_y if new_y >= 0 else new_y + h

    return new_x, new_y


w = GLOBAL_W
h = GLOBAL_H

# part 1
# quadrant calculations
mid_x = (w - 1) // 2
mid_y = (h - 1) // 2
quadrants = {
    "1": lambda x, y: 0 <= x < mid_x and 0 <= y < mid_y,
    "2": lambda x, y: mid_x < x < w and 0 <= y < mid_y,
    "3": lambda x, y: 0 <= x < mid_x and mid_y < y < h,
    "4": lambda x, y: mid_x < x < w and mid_y < y < h,
}

q_counts = {"1": 0, "2": 0, "3": 0, "4": 0}

seconds = 100
final_positions = []

for robot in robots:
    final_position = calc_pos(robot["p"], robot["v"], w, h, seconds)
    final_positions.append(final_position)
    fposx, fposy = final_position

    for name, cond in quadrants.items():
        if cond(fposx, fposy):
            q_counts[name] += 1
            break

print("Part 1:")
safety_factor = 1
for value in q_counts.values():
    safety_factor *= value

print(safety_factor)


# part 2
def print_grid(positions, w, h):
    grid = [["." for _ in range(w)] for _ in range(h)]
    for x, y in positions:
        grid[y][x] = "1"
    for row in grid:
        print("".join(row))
    print()


threshold = 20
seconds = 0
found = False

print()
print("Part 2:")
while not found:
    positions = [calc_pos(robot["p"], robot["v"], w, h, seconds) for robot in robots]

    rows: dict = {}
    cols: dict = {}

    for x, y in positions:
        rows.setdefault(y, []).append(x)
        cols.setdefault(x, []).append(y)

    # only checking rows because the tree is inside a square anyway
    for y, xs in rows.items():
        xs_sorted = sorted(xs)
        consecutive_count = 1
        for i in range(1, len(xs_sorted)):
            if xs_sorted[i] == xs_sorted[i - 1] + 1:
                consecutive_count += 1
                if consecutive_count >= threshold:
                    print(f"Suspicious row found after {seconds} seconds")
                    print_grid(positions, w, h)
                    found = True
                    break
            else:
                consecutive_count = 1
        if found:
            break

    seconds += 1
