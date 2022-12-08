import doctest
from functools import lru_cache
from typing import List, Tuple

FILE_INPUT = "puzzles/day08_input.txt"

TEST_INPUT = [
    "30373",
    "25512",
    "65332",
    "33549",
    "35390",
]

Matrix = Tuple[Tuple[int, ...], ...]
Matrix_bool = Tuple[Tuple[bool, ...], ...]


def make_matrix(lines: List[str]) -> Matrix:
    """
    >>> make_matrix(TEST_INPUT)
    ((3, 0, 3, 7, 3), (2, 5, 5, 1, 2), (6, 5, 3, 3, 2), (3, 3, 5, 4, 9), (3, 5, 3, 9, 0))
    """
    return tuple(tuple(int(c) for c in line) for line in lines)


@lru_cache
def transpose(matrix: Matrix) -> Matrix:
    """
    To be able to memoize the transposed matrix, the input matrix must be immutable. That's why tuples were used.

    >>> transpose(make_matrix(TEST_INPUT))
    ((3, 2, 6, 3, 3), (0, 5, 5, 3, 5), (3, 5, 3, 5, 3), (7, 1, 3, 4, 9), (3, 2, 2, 9, 0))
    """
    if len(set(len(line) for line in matrix)) != 1:
        raise ValueError("All lines of the matrix must have the same length")
    num_lines = len(matrix)
    num_cols = len(matrix[0])
    return tuple(tuple(matrix[i][j] for i in range(0, num_lines)) for j in range(0, num_cols))


def is_tree_visible(matrix: Matrix, i: int, j: int) -> bool:
    """
    >>> is_tree_visible(make_matrix(TEST_INPUT), 3, 1)
    False
    >>> is_tree_visible(make_matrix(TEST_INPUT), 3, 2)
    True
    """
    num_lines = len(matrix)
    num_cols = len(matrix[0])
    height = matrix[i][j]
    matrix_t = transpose(matrix)

    if i == 0 or i == num_lines - 1 or j == 0 or j == num_cols - 1:
        return True

    north = matrix_t[j][0:i]
    south = matrix_t[j][i + 1 :]
    east = matrix[i][j + 1 :]
    west = matrix[i][0:j]
    for direction in [north, south, east, west]:
        if all(map(lambda x: x < height, direction)):
            return True
    return False


def visibility_matrix(matrix: Matrix) -> Matrix_bool:
    """
    >>> visibility_matrix(make_matrix(TEST_INPUT))
    ((True, True, True, True, True), (True, True, True, False, True), (True, True, False, True, True), (True, False, True, False, True), (True, True, True, True, True))
    """
    num_lines = len(matrix)
    num_cols = len(matrix[0])
    return tuple(tuple(is_tree_visible(matrix, i, j) for j in range(0, num_cols)) for i in range(0, num_lines))


def num_visible_trees(matrix: Matrix) -> int:
    """
    >>> num_visible_trees(make_matrix(TEST_INPUT))
    21
    """
    return len([value for row in visibility_matrix(matrix) for value in row if value is True])


# Part 2


def scenic_score(matrix: Matrix, i: int, j: int) -> int:
    """
    >>> scenic_score(make_matrix(TEST_INPUT), 1, 2)
    4
    >>> scenic_score(make_matrix(TEST_INPUT), 3, 2)
    8
    """
    num_lines = len(matrix)
    num_cols = len(matrix[0])
    height = matrix[i][j]
    matrix_t = transpose(matrix)

    if i == 0 or i == num_lines - 1 or j == 0 or j == num_cols - 1:
        return 0

    north = matrix_t[j][0:i]
    south = matrix_t[j][i + 1 :]
    east = matrix[i][j + 1 :]
    west = matrix[i][0:j]

    def num_visible_trees_from_height(row: Tuple[int, ...], height: int) -> int:
        """
        >>> num_visible_trees_from_height((2, 3, 5, 5, 8), 5)
        3
        """
        counter = 0
        for tree in row:
            counter += 1
            if tree >= height:
                return counter
        return counter

    scores: List[int] = []
    scores.append(num_visible_trees_from_height(north[::-1], height))
    scores.append(num_visible_trees_from_height(south, height))
    scores.append(num_visible_trees_from_height(east, height))
    scores.append(num_visible_trees_from_height(west[::-1], height))

    scenic_score = 1
    for score in scores:
        scenic_score *= score
    return scenic_score


def scenic_score_matrix(matrix: Matrix) -> Matrix:
    """
    >>> scenic_score_matrix(make_matrix(TEST_INPUT))
    ((0, 0, 0, 0, 0), (0, 1, 4, 1, 0), (0, 6, 1, 2, 0), (0, 1, 8, 3, 0), (0, 0, 0, 0, 0))
    """
    num_lines = len(matrix)
    num_cols = len(matrix[0])
    return tuple(tuple(scenic_score(matrix, i, j) for j in range(0, num_cols)) for i in range(0, num_lines))


def max_scenic_score(matrix: Matrix) -> int:
    """
    >>> max_scenic_score(make_matrix(TEST_INPUT))
    8
    """
    return max([value for row in scenic_score_matrix(matrix) for value in row])


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        lines = [line.rstrip() for line in f.readlines() if line]

    matrix = make_matrix(lines)
    print(num_visible_trees(matrix))
    print(max_scenic_score(matrix))
    exit()
