FILE_INPUT = "puzzles/day02_input.txt"

result_matrix = {
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

points_for_outcome = {
    "Z": 6,
    "Y": 3,
    "X": 0,
}

points_for_selection = {
    "A": 1,
    "B": 2,
    "C": 3,
}

if __name__ == "__main__":
    with open(FILE_INPUT) as f:
        text = f.readlines()
        rounds = ["".join(line.rstrip().split(" ")) for line in text]

    total_points = 0
    for round in rounds:
        opponent_move, outcome = round[0], round[1]
        result = [r for r, o in result_matrix.items() if o == outcome and r[0] == opponent_move][0]
        my_move = result[1]
        total_points += points_for_outcome[outcome] + points_for_selection[my_move]

    print(f"Total points = {total_points}")
