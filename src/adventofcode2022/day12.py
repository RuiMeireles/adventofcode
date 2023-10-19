import doctest
from typing import List, Tuple

FILE_INPUT = "src/adventofcode2022/day12_input.txt"
DIRECTIONS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]
START = "S"
END = "E"
END_PART_2 = "a"
HEIGHTS = "SabcdefghijklmnopqrstuvwxyzE"

Point = Tuple[int, int]
Path = List[Point]
Matrix = List[List[str]]
Matrix_b = List[List[bool]]


def get_neighbors(p: Point, matrix: Matrix, reversed_path: bool = False) -> List[Point]:
    neighbors: List[Point] = []
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    for dir in DIRECTIONS:
        n = (p[0] + dir[0], p[1] + dir[1])
        # Ensure neighbor is inside the matrix
        if not (0 <= n[0] < num_rows and 0 <= n[1] < num_cols):
            continue
        # Ensure transition to neighbor isn't too steep
        diff = HEIGHTS.index(matrix[n[0]][n[1]]) - HEIGHTS.index(matrix[p[0]][p[1]])
        if not reversed_path:
            if diff > 1:
                continue
        else:
            if diff < -1:
                continue
        neighbors.append(n)
    return neighbors


def get_next_possible_paths(path: Path, matrix: Matrix, visited: Matrix_b, part_1: bool) -> List[Path]:
    """This function updates the 'visited' input argument"""
    new_paths: List[Path] = []
    point = path[-1]
    for n in get_neighbors(point, matrix, reversed_path=not part_1):
        # Ignore the neighbor if it has been already visited by another path
        if visited[n[0]][n[1]]:
            continue
        # Create a new possible path
        visited[n[0]][n[1]] = True
        new_paths.append(path + [n])
    return new_paths


def best_path_length(lines: List[str], part_1: bool) -> int:
    """
    >>> lines = [
    ...     "Sabqponm",
    ...     "abcryxxl",
    ...     "accszExk",
    ...     "acctuvwj",
    ...     "abdefghi",
    ... ]
    >>> best_path_length(lines, part_1=True)
    31
    >>> best_path_length(lines, part_1=False)
    29
    """
    matrix: Matrix = [list(line) for line in lines]
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    visited: Matrix_b = [[False] * num_cols for _ in range(num_rows)]

    # Find start
    start = (0, 0)
    for r in range(num_rows):
        for c in range(num_cols):
            if matrix[r][c] == (START if part_1 else END):
                start = (r, c)
    visited[start[0]][start[1]] = True
    possible_paths: List[Path] = [[start]]
    next_possible_paths: List[Path] = []
    best_path: Path = []

    while True:
        # Discover the next possible paths (breadth-first search)
        for path in possible_paths:
            next_possible_paths += get_next_possible_paths(path, matrix, visited, part_1)
        if not next_possible_paths:
            raise ValueError("There are no solutions!")
        # Check if we reached the end in any of them
        for path in next_possible_paths:
            if matrix[path[-1][0]][path[-1][1]] == (END if part_1 else END_PART_2):
                best_path = path
        if best_path:
            break
        # Prepare for next round
        possible_paths = next_possible_paths
        next_possible_paths = []

    # Uncomment to print the path, and also comment the doctest assertion below
    # print(best_path)
    # print("".join([matrix[step[0]][step[1]] for step in best_path]))
    return len(best_path) - 1


if __name__ == "__main__":
    assert not doctest.testmod().failed
    with open(FILE_INPUT) as f:
        lines = f.read().rstrip().split("\n")

    print(best_path_length(lines, part_1=True))
    print(best_path_length(lines, part_1=False))
    exit()
