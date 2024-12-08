import re
import sys

text = ""
for line in sys.stdin.read():
    text += line

mul_pattern = r"mul\((\d+),(\d+)\)"
do_pattern = r"do\(\)"
dont_pattern = r"don't\(\)"

valid = True
sum = 0

segments = re.split(f"({do_pattern}|{dont_pattern})", text)

for segment in segments:
    if segment == "do()":
        valid = True
    elif segment == "don't()":
        valid = False
    elif valid:
        matches = re.findall(mul_pattern, segment)
        for match in matches:
            sum += int(match[0]) * int(match[1])

print(sum)
