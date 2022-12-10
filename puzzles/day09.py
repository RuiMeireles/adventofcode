import doctest
from typing import List, Set, Tuple

FILE_INPUT = "puzzles/day09_input.txt"
DIRECTIONS_ORT = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
}
DIRECTIONS_DIAG = {
    "UR": (1, 1),
    "UL": (-1, 1),
    "DR": (1, -1),
    "DL": (-1, -1),
}
NUM_TAILS = 9
Position = Tuple[int, int]
Instruction = Tuple[str, int]


def get_neighborhood(position: Position) -> List[Position]:
    """
    >>> get_neighborhood((1, 1))
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    """
    return [(position[0] + i, position[1] + j) for i in range(-1, 2) for j in range(-1, 2)]


def get_ortogonal_neighbors(position: Position) -> List[Position]:
    """
    >>> get_ortogonal_neighbors((1, 1))
    [(1, 2), (1, 0), (0, 1), (2, 1)]
    """
    return [(position[0] + direction[0], position[1] + direction[1]) for direction in DIRECTIONS_ORT.values()]


def get_diagonal_neighbors(position: Position) -> List[Position]:
    """
    >>> get_diagonal_neighbors((1, 1))
    [(2, 2), (0, 2), (2, 0), (0, 0)]
    """
    return [(position[0] + direction[0], position[1] + direction[1]) for direction in DIRECTIONS_DIAG.values()]


def part1(instructions: List[Instruction]) -> int:
    """
    >>> instructions = [
    ...     ("R", 4),
    ...     ("U", 4),
    ...     ("L", 3),
    ...     ("D", 1),
    ...     ("R", 4),
    ...     ("D", 1),
    ...     ("L", 5),
    ...     ("R", 2),
    ... ]
    >>> part1(instructions)
    13
    """
    head = tail = (0, 0)
    visited_by_tail: Set[Position] = {tail}
    for direction, count in instructions:
        offset = DIRECTIONS_ORT[direction]
        for _ in range(count):
            # Move head
            head = (head[0] + offset[0], head[1] + offset[1])
            if tail not in get_neighborhood(head):
                # With only 1 tail, it's always possible to move to an ortogonal neighbor of the head
                tail = list(set(get_neighborhood(tail)) & set(get_ortogonal_neighbors(head)))[0]
                visited_by_tail.add(tail)
    return len(visited_by_tail)


def part2(instructions: List[Instruction]) -> int:
    """
    >>> instructions = [
    ...     ("R", 5),
    ...     ("U", 8),
    ...     ("L", 8),
    ...     ("D", 3),
    ...     ("R", 17),
    ...     ("D", 10),
    ...     ("L", 25),
    ...     ("U", 20),
    ... ]
    >>> part2(instructions)
    36
    """
    head = (0, 0)
    # In these 2 lists, position 0 represents the head
    current_positions: List[Position] = [head for _ in range(NUM_TAILS + 1)]
    visited: List[Set[Position]] = [set([head]) for _ in range(NUM_TAILS + 1)]
    for direction, count in instructions:
        offset = DIRECTIONS_ORT[direction]
        for _ in range(count):
            # Move head
            head = (head[0] + offset[0], head[1] + offset[1])
            current_positions[0] = head
            visited[0].add(head)
            for tail_number in range(1, NUM_TAILS + 1):
                this_position = current_positions[tail_number]
                preceding_position = current_positions[tail_number - 1]
                if this_position not in get_neighborhood(preceding_position):
                    # Move tail
                    my_neighborhood = set(get_neighborhood(this_position))
                    ort_move_options = my_neighborhood & set(get_ortogonal_neighbors(preceding_position))
                    diag_move_options = my_neighborhood & set(get_diagonal_neighbors(preceding_position))
                    # When moving, prefer the position ortogonal to the preceding knot, if available
                    # There's always a maximum of 1 ortogonal move option
                    # When no ortogonal moves are available, there's always a maximum of 1 diagonal move option
                    new_position = list(ort_move_options)[0] if ort_move_options else list(diag_move_options)[0]
                    current_positions[tail_number] = new_position
                    visited[tail_number].add(new_position)
    return len(visited[NUM_TAILS])


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        lines = f.read().split("\n")
        split_lines = [line.split(" ") for line in lines]
        instructions = [(words[0], int(words[1])) for words in split_lines]

    print(part1(instructions))
    print(part2(instructions))
    exit()
