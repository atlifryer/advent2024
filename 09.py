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


# þettta shit er svona 70% chatgpt addled cringe code
# eg var bara kominn með nóg af þessu rusli
def initialize_blocks(content):
    files, spaces = [], []
    pos = 0

    for i, char in enumerate(content):
        if char == "\n":
            continue
        block_size = int(char)
        if i % 2 == 0:
            files.append(list(range(pos, pos + block_size)))
            pos += block_size
        else:
            spaces.append(list(range(pos, pos + block_size)))
            pos += block_size

    return files, spaces


def defragment_memory(files, spaces):
    for i in reversed(range(len(files))):
        file_block = files[i]
        file_size = len(file_block)

        for j, space_block in enumerate(spaces):
            if len(space_block) >= file_size and file_block[0] > space_block[0]:
                files[i] = space_block[:file_size]
                spaces[j] = space_block[file_size:]
                break

    return files, spaces


def calculate_checksum(files):
    checksum = 0
    for file_index, file_block in enumerate(files):
        for position in file_block:
            checksum += file_index * position
    return checksum


files, spaces = initialize_blocks(content)
files, spaces = defragment_memory(files, spaces)

check_sum = calculate_checksum(files)
print("Part 2:")
print("Checksum:", check_sum)
