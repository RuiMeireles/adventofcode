from collections import deque
from copy import deepcopy
import doctest
import re
from typing import Dict, List

FN_INPUT = "puzzles/day05_input.txt"

Stacks = Dict[str, deque[str]]


def read_stacks(stacks_lines: List[str]) -> Stacks:
    """
    >>> stack_lines = [
    ...     '    [D]    ',
    ...     '[N] [C]    ',
    ...     '[Z] [M] [P]',
    ...     ' 1   2   3 ',
    ... ]
    >>> read_stacks(stack_lines)
    {'1': deque(['Z', 'N']), '2': deque(['M', 'C', 'D']), '3': deque(['P'])}
    """
    stacks: Dict[str, deque[str]] = {}
    for i, char in enumerate(stacks_lines[-1]):
        if char.isnumeric():
            stacks[char] = deque()
            for j in range(len(stacks_lines) - 1, -1, -1):
                if stacks_lines[j][i].isalpha():
                    stacks[char].append(stacks_lines[j][i])
    return stacks


def move_crates(stacks: Stacks, instructions_lines: List[str], all_at_once: bool = False) -> Stacks:
    """
    >>> stacks = {'1': deque(['Z', 'N']), '2': deque(['M', 'C', 'D']), '3': deque(['P'])}
    >>> instruction_lines = [
    ...     'move 1 from 2 to 1',
    ...     'move 3 from 1 to 3',
    ...     'move 2 from 2 to 1',
    ...     'move 1 from 1 to 2',
    ... ]
    >>> move_crates(stacks, instruction_lines)
    {'1': deque(['C']), '2': deque(['M']), '3': deque(['P', 'D', 'N', 'Z'])}
    >>> move_crates(stacks, instruction_lines, all_at_once=True)
    {'1': deque(['M']), '2': deque(['C']), '3': deque(['P', 'Z', 'N', 'D'])}
    """
    stacks_out = deepcopy(stacks)
    for instruction in instructions_lines:
        r = re.search(r"^move (\d+) from (\d+) to (\d+)$", instruction)
        assert r is not None
        num_txt, from_stack, to_stack = r.groups()
        num = int(num_txt)
        crates: deque[str] = deque()
        for _ in range(num):
            crates.append(stacks_out[from_stack].pop())
        if all_at_once:
            crates.reverse()
        stacks_out[to_stack] += crates
    return stacks_out


if __name__ == "__main__":
    assert not doctest.testmod().failed
    with open(FN_INPUT) as f:
        lines = f.read()

    # Load and split input (stacks + instructions)
    stacks_txt, instructions_txt = lines.split("\n\n")
    stacks_lines = [line.rstrip() for line in stacks_txt.split("\n") if line]
    instructions_lines = [line.rstrip() for line in instructions_txt.split("\n") if line]

    # Read the stacks and follow the instructions
    stacks = read_stacks(stacks_lines)
    stacks_1 = move_crates(stacks, instructions_lines)
    stacks_2 = move_crates(stacks, instructions_lines, all_at_once=True)

    print("".join([v[-1] for v in stacks_1.values()]))
    print("".join([v[-1] for v in stacks_2.values()]))
