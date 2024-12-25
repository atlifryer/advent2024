import sys
import itertools
from math import log2

# used hint from reddit otherwise i would have been cooked:
# https://www.reddit.com/r/adventofcode/comments/1hla5ql/2024_day_24_part_2_a_guide_on_the_idea_behind_the/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

lines = sys.stdin.read().strip().split("\n\n")
wires_part = lines[0].split("\n")
gates_part = lines[1].split("\n")

gates = []
for gate in gates_part:
    inputs, output = gate.split(" -> ")
    input1, operation, input2 = inputs.split(" ")
    gates.append((input1, operation, input2, output))

wires = {}
for wire in wires_part:
    key, value = wire.split(": ")
    wires[key] = int(value)

condition_1_violators = []
condition_2_violators = []

for input1, operation, input2, output in gates:
    if output.startswith("z"):
        if operation != "XOR" and output != "z45":
            condition_1_violators.append((input1, operation, input2, output))
    else:
        if (
            operation == "XOR"
            and not (input1.startswith("x") or input1.startswith("y"))
            and not (input2.startswith("x") or input2.startswith("y"))
        ):
            condition_2_violators.append((input1, operation, input2, output))


def simulate_gates(wires, gates):
    values = wires.copy()

    def evaluate(operation, a, b):
        if operation == "AND":
            return a & b
        elif operation == "OR":
            return a | b
        elif operation == "XOR":
            return a ^ b

    gates_copy = gates[:]
    unresolved_gates = set()
    while gates_copy:
        for gate in gates_copy[:]:
            input1, operation, input2, output = gate
            if input1 in values and input2 in values:
                values[output] = evaluate(operation, values[input1], values[input2])
                gates_copy.remove(gate)
            else:
                unresolved_gates.add((input1, input2, output))

    x_bits = [values.get(f"x{i:02d}", 0) for i in range(46)]
    y_bits = [values.get(f"y{i:02d}", 0) for i in range(46)]
    z_bits = [values.get(f"z{i:02d}", 0) for i in range(46)]

    x_value = int("".join(map(str, reversed(x_bits))), 2)
    y_value = int("".join(map(str, reversed(y_bits))), 2)
    actual_value = int("".join(map(str, reversed(z_bits))), 2)
    expected_value = x_value + y_value

    return x_bits, y_bits, expected_value, actual_value


# Function to apply swaps
def apply_specific_swaps(gates, swaps):
    for swap_from, swap_to in swaps:
        for i, (input1, operation, input2, output) in enumerate(gates):
            if output == swap_from:
                gates[i] = (input1, operation, input2, swap_to)
            elif output == swap_to:
                gates[i] = (input1, operation, input2, swap_from)


# uncomment to use on your own input:
# best_diff = float("inf")
# best_permutation = None
# best_gates = None

# for permutation in itertools.permutations(outputs_to_swap):
#     # Pair the rule 2 violators with the permutation
#     swaps = list(zip(outputs_to_swap, permutation))

#     # Make a copy of gates to apply swaps
#     gates_copy = gates[:]

#     # Apply the current permutation as swaps
#     apply_specific_swaps(gates_copy, swaps)

#     # Simulate the gates with the current swaps
#     x_bits, y_bits, expected_value, actual_value = simulate_gates(wires, gates_copy)

#     # Calculate the binary difference
#     diff = expected_value ^ actual_value
#     binary_diff = bin(diff)[2:].zfill(46)

#     # Check if this permutation is better
#     if diff < best_diff:
#         best_diff = diff
#         best_permutation = swaps
#         best_gates = gates_copy

best_permutation = [
    ("z11", "z23"),
    ("z23", "sps"),
    ("z05", "frt"),
    ("frt", "z11"),
    ("sps", "tst"),
    ("tst", "z05"),
]
best_diff = 1924145348608
# found using above brute force stuff

gates_copy = gates[:]
apply_specific_swaps(gates_copy, best_permutation)
x_bits, y_bits, expected_value, actual_value = simulate_gates(wires, gates_copy)

# check by what power of 2 the difference is off by
# (finding least significant incorrect bit after 6 correct swaps)
messed_up_bit = int(log2(abs(expected_value - actual_value)))


def find_full_adder_gates(bit_num, gates):
    x_name = f"x{bit_num:02d}"
    y_name = f"y{bit_num:02d}"

    and_gates = []
    xor_gates = []

    for gate in gates:
        input1, operation, input2, output = gate
        if (input1 == x_name and input2 == y_name) or (
            input1 == y_name and input2 == x_name
        ):
            if operation == "AND":
                and_gates.append(gate)
            elif operation == "XOR":
                xor_gates.append(gate)

    return and_gates, xor_gates


and_gates, xor_gates = find_full_adder_gates(38, gates_copy)

if len(and_gates) == 1 and len(xor_gates) == 1:
    and_gate = and_gates[0]
    xor_gate = xor_gates[0]
    new_swap = (and_gate[3], xor_gate[3])
    best_permutation.append(new_swap)

gates_final = gates[:]
apply_specific_swaps(gates_final, best_permutation)

x_bits, y_bits, expected_value, actual_value = simulate_gates(wires, gates_final)
final_diff = expected_value ^ actual_value

if expected_value != actual_value:
    print("You fucked up")


all_wires = set()
for wire1, wire2 in best_permutation:
    all_wires.add(wire1)
    all_wires.add(wire2)

print(",".join(sorted(all_wires)))
