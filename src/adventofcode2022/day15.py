import doctest
from functools import lru_cache
import re
from typing import Dict, Iterable, List, NamedTuple, Set, Tuple


class P(NamedTuple):
    x: int
    y: int


FILE_INPUT_EX = "src/adventofcode2022/day15_input_ex.txt"
FILE_INPUT = "src/adventofcode2022/day15_input.txt"
# Part 1
DEMO = False  # If True it runs with the example data and settings
DEMO_Y_LINE = 10
PART1_Y_LINE = 2_000_000
# Part 2
EXIT_ON_1ST_SOLUTION_FOUND = True  # This was used so the solution is presented much faster (~1 min)
DEMO_MAX_XY = 20
MIN_XY = 0
MAX_XY = 4_000_000
TUNING_FACTOR = 4_000_000


def print_plot(t: Dict[Tuple[int, int], str], tick: int = 10) -> None:
    """
    Prints a plot of Points in the terminal. The values of the dict t must be single characters.
    tick determines how far apart to print the axis values
    TODO: debug the X axis, it's wrong
    """
    number_len = tick - 1
    xl = min([p[0] for p in t])
    xh = max([p[0] for p in t])
    yl = min([p[1] for p in t])
    yh = max([p[1] for p in t])
    x_offset = xl % tick + tick
    # s_x is tick characters long
    s_x = "{x: >" + str(tick) + "}"
    # s_y is number_len + 2 characters long
    s_y = "{y: >" + str(number_len) + "}" + " │"
    # header is the size of number_len
    header = " " * number_len
    x_legend = (
        header
        + "  "
        + " " * (tick - x_offset + 1)
        + "".join(s_x.format(x=x) for x in range(xl + tick, xh + 1) if not x % tick)
    )
    x_top_grid = header + " ┌" + "".join("─" if x % tick != 0 else "┴" for x in range(xl, xh + 1)) + "┐"
    x_bottom_grid = header + " └" + "─" * (xh - xl + 1) + "┘"
    for y in range(yl, yh + 1):
        # Top lines
        if y == yl:
            print(x_legend)
            print(x_top_grid)
        # Middle lines
        print(header + " │" if y % tick != 0 else s_y.format(y=y), end="")
        for x in range(xl, xh + 1):
            print(t[(x, y)] if (x, y) in t else " ", end="")
        print("│")
        # Bottom line
        if y == yh:
            print(x_bottom_grid)


def print_plot_no_borders(t: Dict[Tuple[int, int], str]) -> None:
    xl = min([p[0] for p in t])
    xh = max([p[0] for p in t])
    yl = min([p[1] for p in t])
    yh = max([p[1] for p in t])
    for y in range(yl, yh + 1):
        for x in range(xl, xh + 1):
            print(t[x, y] if (x, y) in t else " ", end="")
        print()


@lru_cache
def get_distance(p1: P, p2: P) -> int:
    """
    Manhatan distance between 2 Points
    >>> get_distance(P(1, 2), P(3, 4))
    4
    """
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def get_neighbors(p: P, distance: int) -> Iterable[P]:
    """
    Created for the brute force approach

    >>> list(get_neighbors(P(0, 0), 2))
    [P(x=-2, y=0), P(x=-1, y=-1), P(x=-1, y=0), P(x=-1, y=1), P(x=0, y=-2), P(x=0, y=-1), P(x=0, y=0), P(x=0, y=1), P(x=0, y=2), P(x=1, y=-1), P(x=1, y=0), P(x=1, y=1), P(x=2, y=0)]
    """
    for x in range(-distance, distance + 1):
        y_range = distance - abs(x)
        for y in range(-y_range, y_range + 1):
            yield P(p.x + x, p.y + y)


def get_neighbors_with_given_y(p: P, distance: int, y: int) -> Iterable[P]:
    """
    Created for the smart approach of part 1

    >>> list(get_neighbors_with_given_y(P(8, 8), 3, 10))
    [P(x=7, y=10), P(x=8, y=10), P(x=9, y=10)]
    >>> list(get_neighbors_with_given_y(P(8, 7), 3, 10))
    [P(x=8, y=10)]
    >>> list(get_neighbors_with_given_y(P(8, 6), 3, 10))
    []
    """
    # Distance to the horizontal line with constant y
    distance_A = abs(p.y - y)
    # Distance that the interception extends to each side
    distance_B = distance - distance_A
    for i in range(-distance_B, distance_B + 1):
        yield P(p.x + i, y)


def get_neighborhood_edge(p: P, distance: int) -> Iterable[P]:
    """
    >>> list(get_neighborhood_edge(P(0, 0), 2))
    [P(x=-2, y=0), P(x=-1, y=1), P(x=-1, y=-1), P(x=0, y=2), P(x=0, y=-2), P(x=1, y=1), P(x=1, y=-1), P(x=2, y=0)]
    """
    yield P(p.x - distance, p.y)
    for dx in range(-distance + 1, distance):
        dy = distance - abs(dx)
        yield P(p.x + dx, p.y + dy)
        yield P(p.x + dx, p.y - dy)
    yield P(p.x + distance, p.y)


if __name__ == "__main__":
    assert not doctest.testmod().failed

    # The tunnels dict is only used in the brute force approach (DEMO=True), and to display the plot
    tunnels: Dict[P, str] = {}
    closest_pairs: List[Tuple[P, P]] = []
    file_input = FILE_INPUT_EX if DEMO else FILE_INPUT
    with open(file_input) as f:
        lines = f.read().rstrip().split("\n")
        for line in lines:
            r = re.search(r"x=(-?\d+).*y=(-?\d+).*x=(-?\d+).*y=(-?\d+)", line)
            assert r is not None
            sx, sy, bx, by = map(int, r.groups())
            sensor = P(sx, sy)
            beacon = P(bx, by)
            closest_pairs.append((sensor, beacon))
            tunnels[sensor] = "S"
            tunnels[beacon] = "B"

    # Part 1: Brute force approach
    if DEMO:
        # Just show sensors and closest beacons
        print_plot(tunnels, 5)
        print()
        # Discover all non-beacon points
        for sensor, beacon in closest_pairs:
            distance = get_distance(sensor, beacon)
            for p in get_neighbors(sensor, distance):
                if p not in tunnels:
                    tunnels[p] = "#"
        # Also show non-beacon points
        print_plot(tunnels, 5)
        print()
        line_number = DEMO_Y_LINE if DEMO else PART1_Y_LINE
        print(len([p for p, v in tunnels.items() if p.y == line_number and v != "B"]))

    # Part 1: Smart approach
    else:
        no_beacon_points: Set[P] = set()
        for sensor, beacon in closest_pairs:
            distance = get_distance(sensor, beacon)
            no_beacon_points.update(get_neighbors_with_given_y(sensor, distance, PART1_Y_LINE))
        # We need to remove potencial beacons that intersect with the no_beacon_points
        for _, beacon in closest_pairs:
            no_beacon_points.discard(beacon)
        print(len(no_beacon_points))

    # Part 2
    is_solution_found = False
    potential_beacons: Set[P] = set()
    max_xy = DEMO_MAX_XY if DEMO else MAX_XY
    for sensor, beacon in closest_pairs:
        distance = get_distance(sensor, beacon)
        # Check all points that are just outside the neighborhood
        for p in get_neighborhood_edge(sensor, distance + 1):
            is_point_invalid = False
            # Check if port falls into boundaries
            if not (MIN_XY <= p.x <= max_xy and MIN_XY <= p.y <= max_xy):
                continue
            # Check point distance to other sensors to verify if it can be a beacon
            for s, b in closest_pairs:
                # Invalidate point if it falls in any sensor's neighborhood
                if get_distance(p, s) <= get_distance(s, b):
                    is_point_invalid = True
                    break
            if not is_point_invalid:
                # Point is a potential beacon
                potential_beacons.add(p)
                if EXIT_ON_1ST_SOLUTION_FOUND:
                    is_solution_found = True
                    break
        if is_solution_found:
            break
    print(list(potential_beacons))
    p = list(potential_beacons)[0]  # With this data, only 1 solution exists
    print(TUNING_FACTOR * p.x + p.y)

    exit()
