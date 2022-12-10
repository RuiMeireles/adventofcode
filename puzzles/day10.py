import doctest
from typing import Dict, List, Tuple

FILE_INPUT_EX = "puzzles/day10_input_ex.txt"
FILE_INPUT = "puzzles/day10_input.txt"

SPRITE_WIDTH = 3
CRT_WIDTH = 40
CRT_HEIGHT = 6


def sprite(X: int) -> List[int]:
    """
    >>> sprite(3)
    [2, 3, 4]
    """
    offset = (SPRITE_WIDTH - 1) // 2
    return [X - offset, X, X + offset]


def crt_pixel(cycle: int, X: int) -> str:
    """
    >>> crt_pixel(8, 5)
    '.'
    >>> crt_pixel(8, 6)
    '#'
    >>> crt_pixel(48, 6)
    '#'
    """
    return "#" if (cycle - 1) % CRT_WIDTH in sprite(X) else "."


def main(split_lines: List[List[str]]) -> Tuple[Dict[int, int], str]:
    cycle = 1
    X = 1
    history_X: Dict[int, int] = {}
    crt: str = ""
    for words in split_lines:
        if words[0] == "noop":
            crt += crt_pixel(cycle, X)
            # End cycle
            history_X[cycle] = X
            cycle += 1
        elif words[0] == "addx":
            V = int(words[1])
            for _ in range(2):
                crt += crt_pixel(cycle, X)
                # End cycle
                history_X[cycle] = X
                cycle += 1
            X += V
    return (history_X, crt)


def sum_of_signal_strengths(history: Dict[int, int]) -> int:
    return sum([k * v for k, v in history.items() if not (k - 20) % 40])


if __name__ == "__main__":
    assert not doctest.testmod().failed

    # with open(FILE_INPUT_EX) as f:
    with open(FILE_INPUT) as f:
        lines = f.read().split("\n")
        split_lines = [line.split(" ") for line in lines]

    history_X, crt = main(split_lines)
    # Part 1
    print(sum_of_signal_strengths(history_X))
    # Part 2
    for i in range(0, len(crt), CRT_WIDTH):
        print(crt[i : i + CRT_WIDTH])
    exit()
