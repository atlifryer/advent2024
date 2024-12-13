import sys
from collections import deque
from collections import defaultdict

content = sys.stdin.read()
lines = content.strip().splitlines()

plants = set(char for line in lines for char in line)


# part 1
def neighbors(matrix, row, col):  # function from day 10
    directions = [1, -1, 1j, -1j]
    nbs = []

    at = row + col * 1j
    for drctn in directions:
        nb = at + drctn
        ni, nj = int(nb.real), int(nb.imag)
        if 0 <= ni < len(matrix) and 0 <= nj < len(matrix[0]):
            nbs.append((ni, nj, matrix[ni][nj], drctn))
        else:  # add-on to count sides that look at out of bounds
            nbs.append((ni, nj, "x", drctn))
    return nbs


def find_regions(matrix, plant):
    visited = set()
    regions = []

    def bfs(start):
        queue = deque([start])
        region = []
        while queue:
            x, y = queue.popleft()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            region.append((x, y))
            for ni, nj, char, _ in neighbors(matrix, x, y):
                if char == plant and (ni, nj) not in visited:
                    queue.append((ni, nj))
        return region

    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            if matrix[x][y] == plant and (x, y) not in visited:
                regions.append(bfs((x, y)))
    return regions


print("Part 1:")
total_price = 0
for plant in plants:
    total_perimeter = 0
    regions = find_regions(lines, plant)
    total_area = sum(len(region) for region in regions)

    for region in regions:
        perimeter = 0
        for loc in region:
            neighboring_plants = neighbors(lines, *loc)
            for _, _, char, _ in neighboring_plants:
                if char != plant:
                    perimeter += 1

        area = len(region)
        total_perimeter += perimeter
        region_cost = perimeter * area
        total_price += region_cost

print("Total price of fencing:", total_price)

# part 2
print("\nPart 2:")

def find_boundary_edges(region, matrix, plant):
    boundary_edges = []
    direction_map = {
        -1: "N",    # Up
        1: "S",     # Down
        -1j: "W",   # Left
        1j: "E"     # Right
    }
    
    for r, c in region:
        for _, _, char, direction in neighbors(matrix, r, c):
            if char != plant:
                boundary_edges.append(((r, c), direction_map[direction]))
    return boundary_edges

def group_boundary_edges(edges):
    grouped_edges = {
        "N": [],
        "E": [],
        "S": [],
        "W": []
    }

    for (r, c), direction in edges:
        grouped_edges[direction].append((r, c))

    # Sort edges for each direction to prepare for finding continuous segments
    for direction in grouped_edges:
        if direction in ["N", "S"]:
            grouped_edges[direction].sort(key=lambda coord: (coord[0], coord[1]))
        else:
            grouped_edges[direction].sort(key=lambda coord: (coord[1], coord[0]))

    return grouped_edges

def find_continuous_segments(sorted_edges, direction):
    segments = []
    checked = set()

    for i, (r, c) in enumerate(sorted_edges):
        if (r, c) in checked:
            continue
        
        segment = [(r, c)]
        checked.add((r, c))

        # Define how to check neighbors based on direction
        if direction == "N" or direction == "S":
            for nr, nc in sorted_edges[i + 1:]:
                if nr == r and nc == c + 1:
                    segment.append((nr, nc))
                    checked.add((nr, nc))
                    c = nc
                else:
                    break

        elif direction == "E" or direction == "W":
            for nr, nc in sorted_edges[i + 1:]:
                if nc == c and nr == r + 1:
                    segment.append((nr, nc))
                    checked.add((nr, nc))
                    r = nr
                else:
                    break

        segments.append(segment)

    return segments


total_price_part2 = 0
for plant in plants:
    regions = find_regions(lines, plant)
    for region in regions:
        print("\nPlant", plant)
        boundary_edges = find_boundary_edges(region, lines, plant)
        grouped_edges = group_boundary_edges(boundary_edges)

        # Find continuous segments for each direction
        N_segments = find_continuous_segments(grouped_edges["N"], "N")
        E_segments = find_continuous_segments(grouped_edges["E"], "E")
        S_segments = find_continuous_segments(grouped_edges["S"], "S")
        W_segments = find_continuous_segments(grouped_edges["W"], "W")

        # Count the total number of fence segments
        total_segments = len(N_segments) + len(E_segments) + len(S_segments) + len(W_segments)
        
        # Calculate cost for the region
        region_cost = total_segments * len(region)
        total_price_part2 += region_cost

        print("Boundary edges:", boundary_edges)
        print("Grouped edges:", grouped_edges)
        print(f"Plant {plant} region with area {len(region)} has {total_segments} segments (cost: {region_cost}).")

print("Total price of fencing (Part 2):", total_price_part2)

# part 2
# ab price = 368
# abcde price = 80
# ex price = 236
# large price = 1206
# xo price = 436
