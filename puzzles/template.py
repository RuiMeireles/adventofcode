import doctest
from typing import List, Tuple

FILE_INPUT = "puzzles/dayXX_input.txt"
Instruction = Tuple[str, int]


def part1(instructions: List[Instruction]) -> int:
    """
    >>> instructions = [
    ...     ("R", 2),
    ... ]
    >>> part1(instructions)
    True
    """
    return True


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        lines = f.read().split("\n")
        split_lines = [line.split(" ") for line in lines]
        instructions = [(words[0], int(words[1])) for words in split_lines]

    print(part1(instructions))
    exit()
