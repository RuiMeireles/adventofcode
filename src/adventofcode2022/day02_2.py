import doctest
from typing import List

FILE_INPUT = "src/adventofcode2022/day02_input.txt"

POINTS_FOR_OUTCOME = {
    "Z": 6,  # Win
    "Y": 3,  # Draw
    "X": 0,  # Loss
}

POINTS_FOR_SELECTION = {
    "A": 1,  # Rock
    "B": 2,  # Paper
    "C": 3,  # Scissor
}

SELECTIONS_OUTCOME = {
    # Player1_selection, Player2_selection: Outcome_for_Player2
    "AA": "Y",
    "AB": "Z",
    "AC": "X",
    "BA": "X",
    "BB": "Y",
    "BC": "Z",
    "CA": "Z",
    "CB": "X",
    "CC": "Y",
}

SELECTIONS_FOR_PLAYER = {
    # (Player1_selection, Outcome_for_Player2): Player2_selection
    (s[0], o): s[1]
    for s, o in SELECTIONS_OUTCOME.items()
}


def calculate_points_from_rounds(rounds: List[List[str]]) -> int:
    """
    >>> calculate_points_from_rounds([["A", "Y"], ["B", "X"], ["C", "Z"]])
    12
    """
    total_points = 0
    for round in rounds:
        opponent_move, outcome = round
        my_move = SELECTIONS_FOR_PLAYER[(opponent_move, outcome)]
        total_points += POINTS_FOR_OUTCOME[outcome] + POINTS_FOR_SELECTION[my_move]
    return total_points


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        lines = f.readlines()

    rounds = [line.rstrip().split(" ") for line in lines]
    total_points = calculate_points_from_rounds(rounds)
    print(f"Total points = {total_points}")
