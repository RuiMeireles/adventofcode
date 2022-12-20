import doctest
from functools import lru_cache
import sys
from typing import Iterator, List, NamedTuple, Tuple


sys.setrecursionlimit(100_000)


class P(NamedTuple):
    x: int
    y: int
    z: int


FILE_INPUT = "puzzles/day18_input.txt"
DIRECTIONS = [
    P(-1, 0, 0),
    P(1, 0, 0),
    P(0, -1, 0),
    P(0, 1, 0),
    P(0, 0, -1),
    P(0, 0, 1),
]


def get_neighbors(p: P) -> Iterator[P]:
    """
    >>> list(get_neighbors(P(1, 1, 1)))
    [P(x=0, y=1, z=1), P(x=2, y=1, z=1), P(x=1, y=0, z=1), P(x=1, y=2, z=1), P(x=1, y=1, z=0), P(x=1, y=1, z=2)]
    """
    for d in DIRECTIONS:
        yield P(p.x + d.x, p.y + d.y, p.z + d.z)


@lru_cache
def cubes_limits(cubes: Tuple[P]) -> Tuple[int, int, int, int, int, int]:
    x_min = min(cubes, key=lambda p: p.x).x
    x_max = max(cubes, key=lambda p: p.x).x
    y_min = min(cubes, key=lambda p: p.y).y
    y_max = max(cubes, key=lambda p: p.y).y
    z_min = min(cubes, key=lambda p: p.z).z
    z_max = max(cubes, key=lambda p: p.z).z
    return (x_min, x_max, y_min, y_max, z_min, z_max)


def part1(cubes: List[P]) -> int:
    """
    >>> cubes = [
    ...     P(2, 2, 2),
    ...     P(1, 2, 2),
    ...     P(3, 2, 2),
    ...     P(2, 1, 2),
    ...     P(2, 3, 2),
    ...     P(2, 2, 1),
    ...     P(2, 2, 3),
    ...     P(2, 2, 4),
    ...     P(2, 2, 6),
    ...     P(1, 2, 5),
    ...     P(3, 2, 5),
    ...     P(2, 1, 5),
    ...     P(2, 3, 5),
    ... ]
    >>> part1(cubes)
    64
    """
    counter = 0
    for cube in cubes:
        for n in get_neighbors(cube):
            if n not in cubes:
                counter += 1
    return counter


def expand_outside_neighborhood(p: P, cubes: List[P], outside: List[P]) -> None:
    assert p not in cubes
    (x_min, x_max, y_min, y_max, z_min, z_max) = cubes_limits(tuple(cubes))
    for n in get_neighbors(p):
        if not (x_min <= n.x <= x_max and y_min <= n.y <= y_max and z_min <= n.z <= z_max):
            continue
        if n in cubes:
            continue
        if n in outside:
            continue
        # New outside point found
        outside.append(n)
        expand_outside_neighborhood(n, cubes, outside)


def part2(cubes: List[P]) -> int:
    """
    >>> cubes = [
    ...     P(2, 2, 2),
    ...     P(1, 2, 2),
    ...     P(3, 2, 2),
    ...     P(2, 1, 2),
    ...     P(2, 3, 2),
    ...     P(2, 2, 1),
    ...     P(2, 2, 3),
    ...     P(2, 2, 4),
    ...     P(2, 2, 6),
    ...     P(1, 2, 5),
    ...     P(3, 2, 5),
    ...     P(2, 1, 5),
    ...     P(2, 3, 5),
    ... ]
    >>> part2(cubes)
    58
    """
    (x_min, x_max, y_min, y_max, z_min, z_max) = cubes_limits(tuple(cubes))
    # Determine starting_points for the search
    starting_points: List[P] = []
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            for z in range(z_min, z_max + 1):
                # Eliminate non-edge points
                if x != x_min and x != x_max and y != y_min and y != y_max and z != z_min and z != z_max:
                    continue
                p = P(x, y, z)
                if p not in cubes:
                    starting_points.append(p)
    # Determine outside points
    outside: List[P] = []
    while starting_points:
        p = starting_points.pop()
        if p in outside:
            # Point was already examined
            continue
        outside.append(p)
        expand_outside_neighborhood(p, cubes, outside)
    # Count the number of cube sides facing outside
    counter = 0
    for cube in cubes:
        for n in get_neighbors(cube):
            if n in outside or not (x_min <= n.x <= x_max and y_min <= n.y <= y_max and z_min <= n.z <= z_max):
                counter += 1
    return counter


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        lines = f.read().rstrip().split("\n")
        coordinates = [line.split(",") for line in lines if lines]
        cubes = [P(*map(int, c)) for c in coordinates]

    print(part1(cubes))
    print(part2(cubes))
    exit()
