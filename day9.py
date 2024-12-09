import sys

content = sys.stdin.read()


def initialize_memory(content):
    memory = []
    file_id = 0

    for i, char in enumerate(content):
        if char == "\n":
            continue
        block_size = int(char)

        if i % 2 == 1:
            memory.extend(["."] * block_size)
        else:
            memory.extend([file_id] * block_size)
            file_id += 1
    return memory


memory_part1 = initialize_memory(content)
print("Part 1:")


def move_memory(mem):
    first_dot = None
    for i in range(len(mem)):
        if mem[i] == ".":
            first_dot = i
            break

    if first_dot is None:
        return mem

    for i in range(len(mem) - 1, first_dot, -1):
        if mem[i] != "." and first_dot < i:
            mem[first_dot], mem[i] = mem[i], mem[first_dot]

            while first_dot < len(mem) and mem[first_dot] != ".":
                first_dot += 1

            if first_dot >= len(mem):
                break

    if len(mem) > 1 and mem[1] == ".":
        mem.pop(1)
        mem.append(".")

    return mem


def checksum(item):
    sum = 0
    for i in range(len(item)):
        if isinstance(item[i], int):
            sum += item[i] * i
    return sum


moved_memory = move_memory(memory_part1.copy())
check_sum = checksum(moved_memory)
print("Checksum:", check_sum)
print()


# part 2
def group_memory(mem2):
    grouped = []
    i = 0
    while i < len(mem2):
        if mem2[i] == ".":
            start = i
            while i < len(mem2) and mem2[i] == ".":
                i += 1
            grouped.append(["."] * (i - start))
        else:
            start = i
            file_id = mem2[i]
            while i < len(mem2) and mem2[i] == file_id:
                i += 1
            grouped.append([file_id] * (i - start))
    return grouped


def defragment_memory(grouped):
    for i in range(len(grouped) - 1, -1, -1):
        if not isinstance(grouped[i][0], int):
            continue

        file_group = grouped[i][:]
        file_size = len(file_group)

        for j in range(i):
            if grouped[j][0] == ".":
                free_size = len(grouped[j])

                if free_size == file_size:
                    grouped[j] = file_group[:]
                    grouped[i] = ["." for _ in range(file_size)]

                    break

                elif free_size > file_size:
                    grouped[j] = file_group[:]
                    grouped[i] = ["." for _ in range(file_size)]

                    leftover = free_size - file_size
                    grouped.insert(j + 1, ["." for _ in range(leftover)])

                    break

    return grouped


memory = initialize_memory(content)
print("\nPart 2:")
grouped_memory = group_memory(memory.copy())
moved_memory2 = defragment_memory(grouped_memory.copy())
flat_result = [item for group in moved_memory2 for item in group]
# print("".join(map(str, flat_result)))
check_sum = checksum(flat_result)
print("Checksum:", check_sum)
