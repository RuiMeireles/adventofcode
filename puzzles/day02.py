from commonlib import read_file_with_blocks_of_int

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

if __name__ == "__main__":
    with open(FILE_INPUT) as f:
        text = f.readlines()
        rounds = ["".join(line.rstrip().split(" ")) for line in text]

    total_points = 0
    for round in rounds:
        result = result_matrix[round]
        total_points += points_for_outcome[result] + points_for_selection[round[1]]

    print(f"Total points = {total_points}")
