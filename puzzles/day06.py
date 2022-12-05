import doctest
from typing import List

FILE_INPUT = "puzzles/dayXX_input.txt"


def main(lines: List[str]) -> int:
    """
    >>> lines = [
    ...     '2-4,6-8',
    ... ]
    >>> main(lines)
    4
    """
    return 4


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        lines = [line.rstrip() for line in f.readlines() if line]

    print(main(lines))
    exit()
