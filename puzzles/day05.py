from collections import deque
from copy import deepcopy
import re
from typing import Dict

FN_INPUT = "puzzles/day05_input.txt"

# Load and split input (stacks + instructions)
with open(FN_INPUT) as f:
    lines = f.read()

stacks_txt, instructions_txt = lines.split("\n\n")
stacks_lines = [line.rstrip() for line in stacks_txt.split("\n") if line]
instructions_lines = [line.rstrip() for line in instructions_txt.split("\n") if line]

stacks: Dict[str, deque[str]] = {}
for i, char in enumerate(stacks_lines[-1]):
    if char.isnumeric():
        stacks[char] = deque()
        for j in range(len(stacks_lines) - 1, -1, -1):
            if stacks_lines[j][i].isalpha():
                stacks[char].append(stacks_lines[j][i])

# Follow the instructions
stacks_1 = deepcopy(stacks)
stacks_2 = deepcopy(stacks)
for instruction in instructions_lines:
    r = re.search(r"^move (\d+) from (\d+) to (\d+)$", instruction)
    assert r is not None
    num_txt, from_stack, to_stack = r.groups()
    num = int(num_txt)
    # Part 1
    for _ in range(num):
        stacks_1[to_stack].append(stacks_1[from_stack].pop())
    # Part 2
    crates: deque[str] = deque()
    for _ in range(num):
        crates.append(stacks_2[from_stack].pop())
    crates.reverse()
    stacks_2[to_stack] += crates
print("".join([v[-1] for v in stacks_1.values()]))
print("".join([v[-1] for v in stacks_2.values()]))
