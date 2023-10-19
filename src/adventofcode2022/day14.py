import doctest
from typing import Dict, List, NamedTuple


class P(NamedTuple):
    x: int
    y: int


FILE_INPUT = "src/adventofcode2022/day14_input.txt"
HOLE = P(500, 0)
DIRECTIONS = [P(0, 1), P(-1, 1), P(1, 1)]


def parse_rock_lines(lines: List[str]) -> List[List[P]]:
    """
    >>> lines = [
    ...     "498,4 -> 498,6 -> 496,6",
    ...     "503,4 -> 502,4 -> 502,9 -> 494,9",
    ... ]
    >>> parse_rock_lines(lines)
    [[P(x=498, y=4), P(x=498, y=6), P(x=496, y=6)], [P(x=503, y=4), P(x=502, y=4), P(x=502, y=9), P(x=494, y=9)]]
    """
    rock_lines: List[List[P]] = []
    for line in lines:
        words = line.split(" -> ")
        points: List[P] = []
        for word in words:
            x, y = word.split(",")
            points.append(P(int(x), int(y)))
        rock_lines.append(points)
    return rock_lines


def build_cave(rock_lines: List[List[P]]) -> Dict[P, str]:
    """
    >>> rock_lines = [[P(x=498, y=4), P(x=498, y=6), P(x=496, y=6)], [P(x=503, y=4), P(x=502, y=4), P(x=502, y=9), P(x=494, y=9)]]
    >>> build_cave(rock_lines)
    {P(x=498, y=4): 'R', P(x=498, y=5): 'R', P(x=498, y=6): 'R', P(x=497, y=6): 'R', P(x=496, y=6): 'R', P(x=503, y=4): 'R', P(x=502, y=4): 'R', P(x=502, y=5): 'R', P(x=502, y=6): 'R', P(x=502, y=7): 'R', P(x=502, y=8): 'R', P(x=502, y=9): 'R', P(x=501, y=9): 'R', P(x=500, y=9): 'R', P(x=499, y=9): 'R', P(x=498, y=9): 'R', P(x=497, y=9): 'R', P(x=496, y=9): 'R', P(x=495, y=9): 'R', P(x=494, y=9): 'R'}
    """
    cave: Dict[P, str] = {}
    for line in rock_lines:
        for i, point in enumerate(line):
            if i == 0:
                continue
            previous_point = line[i - 1]
            # If both points are in the same vertical line
            if point.x == previous_point.x:
                step = 1 if previous_point.y < point.y else -1
                for z in range(previous_point.y, point.y + step, step):
                    cave[P(point.x, z)] = "R"
                continue
            # If both points are in the same horizontal line
            if point.y == previous_point.y:
                step = 1 if previous_point.x < point.x else -1
                for z in range(previous_point.x, point.x + step, step):
                    cave[P(z, point.y)] = "R"
                continue
            assert False
    return cave


def drop_sand_1(cave: Dict[P, str], hole: P) -> int:
    """
    >>> rock_lines = [[P(x=498, y=4), P(x=498, y=6), P(x=496, y=6)], [P(x=503, y=4), P(x=502, y=4), P(x=502, y=9), P(x=494, y=9)]]
    >>> drop_sand_1(build_cave(rock_lines), HOLE)
    24
    """
    y_lowest_rock = max(p.y for p in cave)
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
                sand_next = P(sand.x + d.x, sand.y + d.y)
                if sand_next not in cave:
                    # Check if sand is pouring off the lowest rock
                    if sand_next.y >= y_lowest_rock:
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
                cave[P(sand.x, sand.y)] = "S"
                break
    return num_sand_units


def drop_sand_2(cave: Dict[P, str], hole: P) -> int:
    """
    >>> rock_lines = [[P(x=498, y=4), P(x=498, y=6), P(x=496, y=6)], [P(x=503, y=4), P(x=502, y=4), P(x=502, y=9), P(x=494, y=9)]]
    >>> drop_sand_2(build_cave(rock_lines), HOLE)
    93
    """
    y_lowest_rock = max(p.y for p in cave)
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
                sand_next = P(sand.x + d.x, sand.y + d.y)
                if sand_next not in cave:
                    # Check if this sand unit has hit the floor
                    if sand_next.y == y_floor:
                        break
                    # Sand moves to next position
                    sand = sand_next
                    num_sand_unit_movements += 1
                    next_position_found = True
                    break
            if not next_position_found:
                # Sand stops here
                cave[P(sand.x, sand.y)] = "S"
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
