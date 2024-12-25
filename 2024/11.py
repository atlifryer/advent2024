import sys

content = [872027, 227, 18, 9760, 0, 4, 67716, 9245696]

memo: dict = {}


def get_digit(num):
    if num < 10:
        return 1
    return get_digit(num / 10) + 1


def count_stones(num, steps):
    if steps == 0:
        return 1

    key = (num, steps)
    if key in memo:
        return memo[key]

    digits = get_digit(num)

    if num == 0:
        result = count_stones(1, steps - 1)
    elif digits % 2 == 0:
        mid = 10 ** (digits // 2)
        left = num // mid
        right = num % mid
        result = count_stones(left, steps - 1) + count_stones(right, steps - 1)
    else:
        result = count_stones(num * 2024, steps - 1)

    memo[key] = result
    return result


print("part 1:")
part1 = sum(count_stones(n, 25) for n in content)
print(part1)
print("\npart 2:")
part2 = sum(count_stones(n, 75) for n in content)
print(part2)
