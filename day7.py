import sys


def main():
    content = sys.stdin.read()
    values = content.strip().split("\n")

    result = []

    for entry in values:
        key, numbers = entry.split(": ")
        key = int(key)
        numbers = list(map(int, numbers.split(" ")))
        result.append((key, numbers))

    total_sum = 0

    def concatenate(a, b):
        ab = str(a) + str(b)
        return int(ab)

    def evaluate_combinations(numbers, target, current_index=1, current_value=None):
        if current_value is None:
            current_value = numbers[0]

        if current_index == len(numbers):
            if current_value == target:
                return True
            return False

        next_number = numbers[current_index]

        if evaluate_combinations(
            numbers, target, current_index + 1, current_value + next_number
        ):
            return True
        if evaluate_combinations(
            numbers, target, current_index + 1, current_value * next_number
        ):
            return True
        if evaluate_combinations(
            numbers, target, current_index + 1, concatenate(current_value, next_number)
        ):
            return True

        return False

    for target_result, numbers in result:
        if evaluate_combinations(numbers, target_result):
            total_sum += target_result

    print(total_sum)


main()
