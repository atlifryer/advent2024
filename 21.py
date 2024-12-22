from collections import deque
import sys


class KeypadState:
    def __init__(self, robot1_pos="A", robot2_pos="A", robot3_pos="A", typed=""):
        self.robot1_pos = robot1_pos
        self.robot2_pos = robot2_pos
        self.robot3_pos = robot3_pos
        self.typed = typed

    def __eq__(self, other):
        return (
            self.robot1_pos == other.robot1_pos
            and self.robot2_pos == other.robot2_pos
            and self.robot3_pos == other.robot3_pos
            and self.typed == other.typed
        )

    def __hash__(self):
        return hash((self.robot1_pos, self.robot2_pos, self.robot3_pos, self.typed))

    def __str__(self):
        return f"R1:{self.robot1_pos} R2:{self.robot2_pos} R3:{self.robot3_pos} Typed:{self.typed}"


def find_shortest_sequence(target_code):
    start_state = KeypadState()
    queue = deque([(start_state, "")])
    visited = {start_state}

    dir_keypad = {
        "A": {"<": "^", ">": "A", "^": "A", "v": ">"},
        "^": {"<": None, ">": "A", "^": "^", "v": "v"},
        "v": {"<": "<", ">": ">", "^": "^", "v": "v"},
        "<": {"<": "<", ">": "v", "^": None, "v": "<"},
        ">": {"<": "v", ">": ">", "^": "A", "v": ">"},
    }

    num_keypad = {
        "A": {"<": "0", "^": "3"},
        "0": {"^": "2", ">": "A"},
        "1": {"^": "4", ">": "2"},
        "2": {"<": "1", "^": "5", ">": "3", "v": "0"},
        "3": {"<": "2", "^": "6", "v": "A"},
        "4": {"^": "7", "v": "1", ">": "5"},
        "5": {"<": "4", "^": "8", "v": "2", ">": "6"},
        "6": {"<": "5", "^": "9", "v": "3"},
        "7": {"v": "4", ">": "8"},
        "8": {"<": "7", "v": "5", ">": "9"},
        "9": {"<": "8", "v": "6"},
    }

    while queue:
        current_state, sequence = queue.popleft()

        if current_state.typed == target_code:
            return sequence

        if not target_code.startswith(current_state.typed):
            continue

        # Try moving robot1
        for move in ["^", "v", "<", ">", "A"]:
            if move == "A":
                # Case 1: robot1 is at A and robot2 is at A - we press on robot3
                if current_state.robot1_pos == "A" and current_state.robot2_pos == "A":
                    new_state = KeypadState(
                        current_state.robot1_pos,
                        current_state.robot2_pos,
                        current_state.robot3_pos,
                        current_state.typed + current_state.robot3_pos,
                    )
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_state, sequence + move))

                # Case 2: robot1 is at A but robot2 is not - move robot2
                elif current_state.robot1_pos == "A":
                    if (
                        current_state.robot3_pos in num_keypad
                        and current_state.robot2_pos
                        in num_keypad[current_state.robot3_pos]
                    ):
                        new_pos = num_keypad[current_state.robot3_pos][
                            current_state.robot2_pos
                        ]
                        new_state = KeypadState(
                            current_state.robot1_pos,
                            current_state.robot2_pos,
                            new_pos,
                            current_state.typed,
                        )
                        if new_state not in visited:
                            visited.add(new_state)
                            queue.append((new_state, sequence + move))

                # Case 3: robot1 is not at A - move robot2 based on robot1's position
                else:
                    if (
                        current_state.robot2_pos in dir_keypad
                        and current_state.robot1_pos
                        in dir_keypad[current_state.robot2_pos]
                    ):
                        new_pos = dir_keypad[current_state.robot2_pos][
                            current_state.robot1_pos
                        ]
                        if new_pos is not None:
                            new_state = KeypadState(
                                current_state.robot1_pos,
                                new_pos,
                                current_state.robot3_pos,
                                current_state.typed,
                            )
                            if new_state not in visited:
                                visited.add(new_state)
                                queue.append((new_state, sequence + move))

            # Move robot1 based on direction
            else:
                if (
                    current_state.robot1_pos in dir_keypad
                    and move in dir_keypad[current_state.robot1_pos]
                ):
                    new_pos = dir_keypad[current_state.robot1_pos][move]
                    if new_pos is not None:
                        new_state = KeypadState(
                            new_pos,
                            current_state.robot2_pos,
                            current_state.robot3_pos,
                            current_state.typed,
                        )
                        if new_state not in visited:
                            visited.add(new_state)
                            queue.append((new_state, sequence + move))

    return None


complexity = 0
lines = sys.stdin.read().strip().split("\n")
for line in lines:
    print(f"\nTrying to find sequence for code: {line}")
    sequence = find_shortest_sequence(line)
    if sequence:
        number = int(line[:-1])
        complexity += number * len(sequence)
        print(f"Found sequence: {sequence}")
        print(f"Length: {len(sequence)}")
    else:
        print("No sequence found!")
print(f"Total complexity: {complexity}")
