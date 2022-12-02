FILE_INPUT = "puzzles/day02_input.txt"

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

if __name__ == "__main__":
    with open(FILE_INPUT) as f:
        text = f.readlines()
        rounds = [line.rstrip().split(" ") for line in text]

    total_points = 0
    for round in rounds:
        opponent_move, outcome = round
        my_move = SELECTIONS_FOR_PLAYER[(opponent_move, outcome)]
        total_points += POINTS_FOR_OUTCOME[outcome] + POINTS_FOR_SELECTION[my_move]

    print(f"Total points = {total_points}")
