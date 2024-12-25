from functools import cmp_to_key
import sys

all_text = sys.stdin.read().strip().split("\n")
split_index = all_text.index("")
ordering_rules = all_text[:split_index]
updates = all_text[split_index + 1 :]

updates_list = [list(map(int, item.split(","))) for item in updates]
incorrect_updates = []

middle_sum = 0
for update in updates_list:
    isValid = True
    for rule in ordering_rules:
        split_index = rule.index("|")
        rule1 = int(rule[:split_index])
        rule2 = int(rule[split_index + 1 :])
        if rule1 in update and rule2 in update:
            if update.index(rule1) > update.index(rule2):
                isValid = False
                incorrect_updates.append(update)
                break
    if isValid:
        middle_sum += update[len(update) // 2]

# print(middle_sum)
# print(incorrect_updates)

corrected_updates_sum = 0

for update in incorrect_updates:
    pages_in_update = set(update)
    relevant_rules = []
    for rule in ordering_rules:
        split_index = rule.index("|")
        rule1 = int(rule[:split_index])
        rule2 = int(rule[split_index + 1 :])
        if rule1 in pages_in_update and rule2 in pages_in_update:
            relevant_rules.append((rule1, rule2))

    def compare_pages(page1, page2):
        if (page1, page2) in relevant_rules:
            return -1
        elif (page2, page1) in relevant_rules:
            return 1
        else:
            return 0

    sorted_update = sorted(update, key=cmp_to_key(compare_pages))

    middle_page = sorted_update[len(sorted_update) // 2]
    corrected_updates_sum += middle_page

print(corrected_updates_sum)
