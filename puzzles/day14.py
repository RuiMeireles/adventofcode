import doctest
from typing import Dict, List, Tuple

FILE_INPUT = "puzzles/day14_input.txt"
HOLE = (500, 0)
DIRECTIONS = [(0, 1), (-1, 1), (1, 1)]
Point = Tuple[int, int]


def parse_rock_lines(lines: List[str]) -> List[List[Point]]:
    """
    >>> lines = [
    ...     "498,4 -> 498,6 -> 496,6",
    ...     "503,4 -> 502,4 -> 502,9 -> 494,9",
    ... ]
    >>> parse_rock_lines(lines)
    [[(498, 4), (498, 6), (496, 6)], [(503, 4), (502, 4), (502, 9), (494, 9)]]
    """
    rock_lines: List[List[Point]] = []
    for line in lines:
        words = line.split(" -> ")
        points: List[Point] = []
        for word in words:
            x, y = word.split(",")
            points.append((int(x), int(y)))
        rock_lines.append(points)
    return rock_lines


def build_cave(rock_lines: List[List[Point]]) -> Dict[Point, str]:
    """
    >>> rock_lines = [[(498, 4), (498, 6), (496, 6)], [(503, 4), (502, 4), (502, 9), (494, 9)]]
    >>> build_cave(rock_lines)
    {(498, 4): 'R', (498, 5): 'R', (498, 6): 'R', (497, 6): 'R', (496, 6): 'R', (503, 4): 'R', (502, 4): 'R', (502, 5): 'R', (502, 6): 'R', (502, 7): 'R', (502, 8): 'R', (502, 9): 'R', (501, 9): 'R', (500, 9): 'R', (499, 9): 'R', (498, 9): 'R', (497, 9): 'R', (496, 9): 'R', (495, 9): 'R', (494, 9): 'R'}
    """
    cave: Dict[Point, str] = {}
    for line in rock_lines:
        for i, point in enumerate(line):
            if i == 0:
                continue
            previous_point = line[i - 1]
            # If both points are in the same vertical line
            if point[0] == previous_point[0]:
                step = 1 if previous_point[1] < point[1] else -1
                for x in range(previous_point[1], point[1] + step, step):
                    cave[(point[0], x)] = "R"
                continue
            # If both points are in the same horizontal line
            if point[1] == previous_point[1]:
                step = 1 if previous_point[0] < point[0] else -1
                for x in range(previous_point[0], point[0] + step, step):
                    cave[(x, point[1])] = "R"
                continue
            assert False
    return cave


def drop_sand_1(cave: Dict[Point, str], hole: Point) -> int:
    """
    >>> rock_lines = [[(498, 4), (498, 6), (496, 6)], [(503, 4), (502, 4), (502, 9), (494, 9)]]
    >>> drop_sand_1(build_cave(rock_lines), HOLE)
    24
    """
    y_lowest_rock = max(p[1] for p in cave)
    num_sand_units = 0
    is_sand_stack_full = False
    # Cycle 1: Many sand units
    while not is_sand_stack_full:
        num_sand_units += 1
        sand = hole
        num_sand_unit_movements = 0
        # Cycle 2: One sand unit falls from hole
        while True:
            next_position_found = False
            for d in DIRECTIONS:
                sand_next = (sand[0] + d[0], sand[1] + d[1])
                if sand_next not in cave:
                    # Check if sand is pouring off the lowest rock
                    if sand_next[1] >= y_lowest_rock:
                        # Do not count this sand unit
                        num_sand_units -= 1
                        is_sand_stack_full = True
                        break
                    # Sand moves to next position
                    sand = sand_next
                    num_sand_unit_movements += 1
                    next_position_found = True
                    break
            if is_sand_stack_full:
                break
            # If the sand unit didn't find a place to move to
            if not next_position_found:
                # Sand stops here
                cave[sand[0], sand[1]] = "S"
                break
    return num_sand_units


def drop_sand_2(cave: Dict[Point, str], hole: Point) -> int:
    """
    >>> rock_lines = [[(498, 4), (498, 6), (496, 6)], [(503, 4), (502, 4), (502, 9), (494, 9)]]
    >>> drop_sand_2(build_cave(rock_lines), HOLE)
    93
    """
    y_lowest_rock = max(p[1] for p in cave)
    y_floor = y_lowest_rock + 2
    num_sand_units = 0
    # Cycle 1: Many sand units until the hole is covered
    while hole not in cave:
        num_sand_units += 1
        sand = hole
        num_sand_unit_movements = 0
        # Cycle 2: One sand unit falls from hole
        while True:
            next_position_found = False
            for d in DIRECTIONS:
                sand_next = (sand[0] + d[0], sand[1] + d[1])
                if sand_next not in cave:
                    # Check if this sand unit has hit the floor
                    if sand_next[1] == y_floor:
                        break
                    # Sand moves to next position
                    sand = sand_next
                    num_sand_unit_movements += 1
                    next_position_found = True
                    break
            if not next_position_found:
                # Sand stops here
                cave[sand[0], sand[1]] = "S"
                break
    return num_sand_units


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        lines = f.read().rstrip().split("\n")

    rock_lines = parse_rock_lines(lines)
    cave = build_cave(rock_lines)
    print(drop_sand_1(cave, HOLE))
    cave = build_cave(rock_lines)
    print(drop_sand_2(cave, HOLE))
    exit()
