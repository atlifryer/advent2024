import sys


left_numbers = []
right_numbers = []

for line in sys.stdin.read().splitlines():
    number1, number2 = map(int, line.split())
    left_numbers.append(number1)
    right_numbers.append(number2)

similarity_total = 0
for left_number in left_numbers:
    similarity = 0
    for right_number in right_numbers:
        if left_number == right_number:
            similarity += 1
    similarity_total += left_number * similarity

print(similarity_total)
