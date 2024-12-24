from functools import lru_cache
import sys

lines = sys.stdin.read().strip().split("\n")

numeric_keypad = {
    # 	7  8  9
    #   4  5  6
    #   1  2  3
    #      0 [A]
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}

direction_keypad = {
    # 	   ^ [A]
    #  	<  v  >
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}

dir_map = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}


# Generate all possible combinations of count_a a's and count_b b's
def generate_combinations(a, b, count_a, count_b):
    def backtrack(combination, remaining_a, remaining_b):
        if remaining_a == 0 and remaining_b == 0:
            results.append("".join(combination))
            return
        if remaining_a > 0:
            combination.append(a)
            backtrack(combination, remaining_a - 1, remaining_b)
            combination.pop()
        if remaining_b > 0:
            combination.append(b)
            backtrack(combination, remaining_a, remaining_b - 1)
            combination.pop()

    results = []
    backtrack([], count_a, count_b)
    return results


# Generate all valid move sequences from start to target on respective keypad
@lru_cache(None)
def valid_move_sequences(start, target):
    if start in direction_keypad and target in direction_keypad:
        keypad = direction_keypad
    else:
        keypad = numeric_keypad

    start_pos = keypad[start]
    dest_pos = keypad[target]

    diff_x = dest_pos[0] - start_pos[0]
    diff_y = dest_pos[1] - start_pos[1]

    x_moves = ("^" if diff_x < 0 else "v", abs(diff_x))
    y_moves = ("<" if diff_y < 0 else ">", abs(diff_y))

    move_combinations = generate_combinations(
        x_moves[0], y_moves[0], x_moves[1], y_moves[1]
    )

    # Check if the sequence is valid based on the keypad
    def is_valid(sequence):
        current_pos = start_pos
        for move in sequence:
            if move in dir_map:
                dx, dy = dir_map[move]
                current_pos = (current_pos[0] + dx, current_pos[1] + dy)
                if current_pos not in keypad.values():
                    return False
        return True

    valid_sequences = ["".join(seq) + "A" for seq in move_combinations if is_valid(seq)]
    return valid_sequences


# Get the shortest sequence length from start to target recursively
@lru_cache(None)
def shortest_sequence_length(start, target, depth=0):
    if depth == 0:
        ways = valid_move_sequences(start, target)
        return min(len(way) for way in ways)

    ways = valid_move_sequences(start, target)
    shortest_length = float("inf")

    for way in ways:
        total_length = 0
        way = "A" + way
        for i in range(len(way) - 1):
            sub_start, sub_target = way[i], way[i + 1]
            total_length += shortest_sequence_length(sub_start, sub_target, depth - 1)

        shortest_length = min(shortest_length, total_length)

    return shortest_length


def code_sequence_length(code, depth):
    code = "A" + code
    length = 0
    for i in range(len(code) - 1):
        a, b = code[i], code[i + 1]
        length += shortest_sequence_length(a, b, depth)
    return length


# part 1
complexity = 0
for line in lines:
    complexity += code_sequence_length(line, 2) * int(line[:-1])

print(complexity)

# part 2
complexity = 0
for line in lines:
    complexity += code_sequence_length(line, 25) * int(line[:-1])

print(complexity)
