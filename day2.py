def main():
    def is_line_safe(line):
        increasing = False
        decreasing = False

        for j in range(len(line) - 1):
            if line[j] < line[j + 1]:
                increasing = True
            else:
                decreasing = True
            if increasing and decreasing:
                return False
            diff = abs(line[j] - line[j + 1])
            if diff > 3 or diff < 1:
                return False
        return True

    lines = []

    with open("day2_input.txt", "r") as file:
        for line in file:
            numbers = list(map(int, line.split()))
            lines.append(numbers)

    unsafe_lines = [line[:] for line in lines]

    safe_reports = 0

    for line in lines:
        if is_line_safe(line):
            print(line)
            unsafe_lines.remove(line)
            safe_reports += 1

    for line in unsafe_lines:
        for i in range(len(line)):
            temp_line = line[:i] + line[i + 1 :]

            if is_line_safe(temp_line):
                safe_reports += 1
                break

    print(safe_reports)


main()
