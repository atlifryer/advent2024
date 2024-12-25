import sys

content = sys.stdin.read()
values = content.strip().split("\n")

frequencies: dict = {}

for row, line in enumerate(values):
    for col, char in enumerate(line):
        if char != ".":
            if char not in frequencies:
                frequencies[char] = []
            frequencies[char].append((row, col))


def an_locs(point1, point2):
    r1, c1 = point1
    r2, c2 = point2

    delta_r = r2 - r1
    delta_c = c2 - c1

    point_before = (r1 - delta_r, c1 - delta_c)
    point_after = (r2 + delta_r, c2 + delta_c)

    return point_before, point_after


cols = len(values[0])
rows = len(values)

p1_locs: set = set()


# part 1
for char, locations in frequencies.items():
    for i in range(len(locations) - 1):
        point1 = locations[i]
        for j in range(i + 1, len(locations)):
            point2 = locations[j]
            before, after = an_locs(point1, point2)
            if all(0 <= coord <= rows - 1 for coord in before):
                p1_locs.add(before)
            if all(0 <= coord <= rows - 1 for coord in after):
                p1_locs.add(after)

print(len(p1_locs))
print(p1_locs)
print()

# part 2

p2_locs: set = set()

for char, locations in frequencies.items():
    queue = locations.copy()
    seen = set(queue)

    for i in range(len(locations) - 1):
        point1 = locations[i]
        r1, c1 = point1
        for j in range(i + 1, len(locations)):
            point2 = locations[j]
            r2, c2 = point2

            delta_r = r2 - r1
            delta_c = c2 - c1

            current_before = (r1 - delta_r, c1 - delta_c)
            current_after = (r2 + delta_r, c2 + delta_c)

            if 0 <= current_before[0] < rows and 0 <= current_before[1] < cols:
                p2_locs.add(current_before)
            if 0 <= current_after[0] < rows and 0 <= current_after[1] < cols:
                p2_locs.add(current_after)

            while True:
                next_before = (current_before[0] - delta_r, current_before[1] - delta_c)
                next_after = (current_after[0] + delta_r, current_after[1] + delta_c)

                extended = False

                if all(0 <= coord < rows for coord in next_before):
                    p2_locs.add(next_before)
                    print(next_before)
                    current_before = next_before
                    extended = True

                if all(0 <= coord < rows for coord in next_after):
                    p2_locs.add(next_after)
                    print(next_after)
                    current_after = next_after
                    extended = True

                if not extended:
                    break

print()
for ants in frequencies.values():
    for ant in ants:
        p2_locs.add(ant)
print(p2_locs)
print(len(p2_locs))
