import sys

content = sys.stdin.read().split(" ")
content[-1] = content[-1].rstrip("\n")

memo = {}

def count_stones(num_str, steps):
	if steps == 0:
		return 1

	key = (num_str, steps)
	if key in memo:
		return memo[key]

	integer = int(num_str)
	digits = len(num_str)

	if integer == 0:
		result = count_stones("1", steps - 1)
	elif digits % 2 == 0:
		mid = digits // 2
		left = str(int(num_str[:mid]))
		right = str(int(num_str[mid:]))
		result = count_stones(left, steps - 1) + count_stones(right, steps - 1)
	else:
		new_val = str(integer * 2024)
		result = count_stones(new_val, steps - 1)
	
	memo[key] = result
	return result

print("part 1:")
part1 = sum(count_stones(str(n), 25) for n in content)
print(part1)
print("\npart 2:")
part2 = sum(count_stones(str(n), 75) for n in content)
print(part2)








