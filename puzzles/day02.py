import doctest
from typing import List


FILE_INPUT = "puzzles/day02_input.txt"


result_matrix = {
    "AX": "DRAW",
    "AY": "WIN",
    "AZ": "LOSS",
    "BX": "LOSS",
    "BY": "DRAW",
    "BZ": "WIN",
    "CX": "WIN",
    "CY": "LOSS",
    "CZ": "DRAW",
}

points_for_outcome = {
    "WIN": 6,
    "DRAW": 3,
    "LOSS": 0,
}

points_for_selection = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}


def calculate_points_from_rounds(rounds: List[List[str]]) -> int:
    """
    >>> calculate_points_from_rounds([["A", "Y"], ["B", "X"], ["C", "Z"]])
    15
    """
    total_points = 0
    for round in rounds:
        result = result_matrix["".join(round)]
        total_points += points_for_outcome[result] + points_for_selection[round[1]]
    return total_points


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        text = f.readlines()

    rounds = [line.rstrip().split(" ") for line in text]
    total_points = calculate_points_from_rounds(rounds)
    print(f"Total points = {total_points}")
