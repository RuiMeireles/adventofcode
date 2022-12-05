from copy import deepcopy
import re

FN_INPUT = "puzzles/day05_input.txt"

with open(FN_INPUT) as f:
    lines = f.read()

stacks_txt, instructions_txt = lines.split('\n\n')
stacks_lines = [line.rstrip() for line in stacks_txt.split('\n')]
instructions_lines = [line.rstrip() for line in instructions_txt.split('\n')]

stacks = {}
for i, char in enumerate(stacks_lines[-1]):
    if char.isnumeric():
        stacks[char] = []
        for j in range(len(stacks_lines) - 1, -1, -1):
            if stacks_lines[j][i].isalpha():
                stacks[char].append(stacks_lines[j][i])

stacks_1 = deepcopy(stacks)
for instruction in instructions_lines:
    r = re.search(r"^move (\d+) from (\d+) to (\d+)$", instruction)
    num, from_stack, to_stack = r.groups()
    for _ in range(int(num)):
        stacks_1[to_stack].append(stacks_1[from_stack].pop())
print("".join([v[-1] for v in stacks_1.values()]))

stacks_2 = deepcopy(stacks)
for instruction in instructions_lines:
    r = re.search(r"^move (\d+) from (\d+) to (\d+)$", instruction)
    num_txt, from_stack, to_stack = r.groups()
    num = int(num_txt)
    crates = stacks_2[from_stack][-num:]
    stacks_2[from_stack] = stacks_2[from_stack][0:-num]
    stacks_2[to_stack] += crates
print("".join([v[-1] for v in stacks_2.values()]))
