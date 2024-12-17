import random
import sys
import copy


def combo_operand(operand, A, B, C):
	if operand in [0, 1, 2, 3]:
		return operand
	elif operand == 4:
		return A
	elif operand == 5:
		return B
	elif operand == 6:
		return C
	else:
		raise ValueError(f"Invalid combo operand: {operand}")

def adv(A, operand): # opcode 0
	return A // (2**operand)

def bxl(B, operand): # opcode 1
	return B ^ operand

def bst(operand): # opcode 2
	return operand % 8

def jnz(A, operand, instruction_pointer): # opcode 3
	if A != 0:
		return operand
	return instruction_pointer + 2

def bxc(B, C): # opcode 4
	return B ^ C

def out(operand): # opcode 5
	return operand % 8

def bdv(A, operand): # opcode 6
	return A // (2**operand)

def cdv(A, operand): # opcode 7
	return A // (2**operand)


def run_program(registers, program):
    A, B, C = registers
    instruction_pointer = 0
    output = []

    while instruction_pointer < len(program):
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1]
        
        if opcode == 0:  # adv
            A = adv(A, combo_operand(operand, A, B, C))
        elif opcode == 1:  # bxl
            B = bxl(B, operand)
        elif opcode == 2:  # bst
            B = bst(combo_operand(operand, A, B, C))
        elif opcode == 3:  # jnz
            new_pointer = jnz(A, operand, instruction_pointer)
            instruction_pointer = new_pointer
            continue
        elif opcode == 4:  # bxc
            B = bxc(B, C)
        elif opcode == 5:  # out
            output_value = out(combo_operand(operand, A, B, C))
            output.append(output_value)
        elif opcode == 6:  # bdv
            B = bdv(A, combo_operand(operand, A, B, C))
        elif opcode == 7:  # cdv
            C = cdv(A, combo_operand(operand, A, B, C))
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

        instruction_pointer += 2

    return output

# part 1
print("Part 1")
lines = sys.stdin.read().strip().split("\n")
registers = [int(line.split(":")[1].strip()) for line in lines[:3]]
program_part_1 = list(map(int, lines[4].split(":")[1].split(",")))
result_part_1 = run_program(registers, program_part_1)
print(f"Result: {result_part_1}")
print("***************")

def output_length_for_A(A, program):
    out = run_program([A,0,0], program)
    return len(out)

def find_bounds(program, target_len):
    base_A = 0
    base_len = output_length_for_A(base_A, program)
    
    if base_len == target_len:
        high = 1
        while output_length_for_A(high, program) == target_len and high < (1 << 60):
            high *= 2
        low = 0
        return low, high
    
    if base_len < target_len:
        high = 1
        while output_length_for_A(high, program) < target_len and high < (1 << 60):
            high *= 2
        
        low = 0
        
        lb = low
        ub = high
        while lb < ub:
            mid = (lb + ub) // 2
            length_mid = output_length_for_A(mid, program)
            if length_mid < target_len:
                lb = mid + 1
            else:
                ub = mid
        
        return lb, high * 6
    
    if base_len > target_len:
        high = 1
        while output_length_for_A(high, program) > target_len and high < (1 << 60):
            high *= 2
        low = 0
        lb = low
        ub = high
        while lb < ub:
            mid = (lb + ub) // 2
            length_mid = output_length_for_A(mid, program)
            if length_mid > target_len:
                lb = mid + 1
            else:
                ub = mid
        return lb, high * 6

def hamming_distance(output, target_output):
    return sum(o != t for o, t in zip(output, target_output))

def run_program_memoized(A, program, memo):
    if A in memo:
        return memo[A]
    output = run_program([A,0,0], program)
    memo[A] = output
    return output

def fitness(A, program, target, memo):
    out = run_program_memoized(A, program, memo)
    dist = hamming_distance(out, target)
    return dist

def crossover(a, b):
    A_bin = format(a, 'b').zfill(64)
    B_bin = format(b, 'b').zfill(64)
    point = random.randint(1, 63)
    child_bin = A_bin[:point] + B_bin[point:]
    return int(child_bin, 2)

def mutate(a, mutation_rate=0.02):
    A_bin = list(format(a, 'b').zfill(64))
    for i in range(len(A_bin)):
        if random.random() < mutation_rate:
            A_bin[i] = '1' if A_bin[i] == '0' else '0'
    return int(''.join(A_bin), 2)

def genetic_algorithm(program, target_output, 
                      pop_size=500, 
                      generations=10000, 
                      crossover_rate=0.7, 
                      mutation_rate=0.01, 
                      lower_bound=0, 
                      upper_bound=200000000000000):
    population = [random.randint(lower_bound, upper_bound) for _ in range(pop_size)]
    memo = {}

    best_perfect_A = None
    
    for gen in range(generations):
        scored = []
        for a in population:
            dist = fitness(a, program, target_output, memo)
            scored.append((dist, a))

        scored.sort(key=lambda x: (x[0], x[1]))
        best_dist, best_A = scored[0]

        if best_dist == 0:
            if best_perfect_A is None or best_A < best_perfect_A:
                best_perfect_A = best_A
        
        survivors = scored[:pop_size//2]
        
        new_pop = []
        new_pop.append(best_A)
        
        while len(new_pop) < pop_size:
            parent1 = random.choice(survivors)[1]
            parent2 = random.choice(survivors)[1]
            
            if random.random() < crossover_rate:
                child = crossover(parent1, parent2)
            else:
                child = parent1
            
            child = mutate(child, mutation_rate)
            
            if child < lower_bound or child > upper_bound:
                child = random.randint(lower_bound, upper_bound)
            
            new_pop.append(child)
        
        population = new_pop
    
    return best_perfect_A

program = program_part_1
target_output = program_part_1.copy()
target_len = len(target_output)

lower_bound, upper_bound = find_bounds(program, target_len)

print("\nPart 2:")
print("Estimated Bounds:", lower_bound, upper_bound)
found_A = genetic_algorithm(program, target_output, lower_bound=lower_bound, upper_bound=upper_bound)
print("Found A:", found_A)

print("Should see:")
print(f"Result: {program_part_1}")
print()
print("Testing A:")
registers = [found_A, 0, 0]
program = program_part_1
result = run_program(registers, program)
print(f"Result: {result}")
if result != program_part_1:
    print("Didn't find a working A value...")
else:
    print("It worked. But we're not 100% sure it's the lowest value...")



