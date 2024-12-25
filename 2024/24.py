import sys

lines = sys.stdin.read().strip().split("\n\n")
wires_part = lines[0].split("\n")
gates_part = lines[1].split("\n")

values = {}

for wire in wires_part:
    key, value = wire.split(": ")
    values[key] = int(value)

gates = []
for gate in gates_part:
    inputs, output = gate.split(" -> ")
    input1, operation, input2 = inputs.split(" ")
    gates.append((input1, operation, input2, output))


def evaluate(operation, a, b):
    if operation == "AND":
        return a & b
    elif operation == "OR":
        return a | b
    elif operation == "XOR":
        return a ^ b
    else:
        raise ValueError(f"Unknown operation: {operation}")


while gates:
    for gate in gates[:]:
        input1, operation, input2, output = gate
        if input1 in values and input2 in values:
            result = evaluate(operation, values[input1], values[input2])
            values[output] = result
            gates.remove(gate)

z_keys = sorted(key for key in values if key.startswith("z"))

binary_number = "".join(str(values[key]) for key in reversed(z_keys))
binary_integer = int(binary_number, 2)

# part 1
print(binary_integer)
