import sys
import re
from sympy import Matrix, solve_linear_system, symbols  # type: ignore

content = sys.stdin.read()
machines_raw = content.strip().split("\n\n")

machines = []

for machine in machines_raw:
    lines = machine.split("\n")
    machine_data = {
        "A": lines[0].split(": ")[1],
        "B": lines[1].split(": ")[1],
        "Prize": lines[2].split(": ")[1],
    }
    machines.append(machine_data)

cost_a = 3
cost_b = 1
max_button_presses = 100


def parse_button(button_str):
    x_move, y_move = map(int, re.findall(r"[+-]\d+", button_str))
    return x_move, y_move


def calc_button_presses(machine, part2=False):
    ax, ay = parse_button(machine["A"])
    bx, by = parse_button(machine["B"])

    target_x, target_y = map(int, re.findall(r"\d+", machine["Prize"]))

    if part2:
        target_x += 10000000000000
        target_y += 10000000000000

    a, b = symbols("a b")

    system = Matrix([[ax, bx, target_x], [ay, by, target_y]])

    solution = solve_linear_system(system, a, b)

    if solution and all(val >= 0 for val in solution.values()):
        return solution[a], solution[b]

    return None


total_a_presses = 0
total_b_presses = 0
for i, machine in enumerate(machines, start=1):
    result = calc_button_presses(machine)
    if result:
        ap, bp = result
        if "/" in str(ap) or "/" in str(bp):
            continue
        total_a_presses += ap
        total_b_presses += bp

print("Part 1:")

total_a_presses = 0
total_b_presses = 0
for i, machine in enumerate(machines, start=1):
    result = calc_button_presses(machine)
    if result:
        ap, bp = result
        if "/" in str(ap) or "/" in str(bp):
            continue
        total_a_presses += ap
        total_b_presses += bp

total_cost = total_a_presses * cost_a + total_b_presses * cost_b
print(f"You must spend {total_cost} tokens.")

print()
print("Part 2:")

total_a_presses = 0
total_b_presses = 0
for i, machine in enumerate(machines, start=1):
    result = calc_button_presses(machine, part2=True)
    if result:
        ap, bp = result
        if "/" in str(ap) or "/" in str(bp):
            continue
        total_a_presses += ap
        total_b_presses += bp

total_cost = total_a_presses * cost_a + total_b_presses * cost_b
print(f"You must spend {total_cost} tokens.")
