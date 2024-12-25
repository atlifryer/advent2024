import sys
from functools import lru_cache

content = sys.stdin.read()
test = content.strip().split("\n\n")
towels = test[0].split(", ")
designs = test[1].split("\n")

@lru_cache(None)
def can_form_design(design):
	if not design:
		return True
	for towel in towels:
		if design.startswith(towel):
			if can_form_design(design[len(towel):]):
				return True
	return False

# part 1
count = sum(can_form_design(design) for design in designs)
print(count)

# part 2
@lru_cache(None)
def count_ways(design):
    if not design:
        return 1
    ways = 0
    for towel in towels:
        if design.startswith(towel):
            ways += count_ways(design[len(towel):])
    return ways

total_ways = sum(count_ways(design) for design in designs)
print(total_ways)

#well that was easy