import doctest
import re

Matrix = list[list[str]]
P = tuple[int, int]

FILE_INPUT = "puzzles/day22_input.txt"

DIRECTIONS = {
    "U": (-1, 0),
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
}

TURN_R = {
    "U": "R",
    "R": "D",
    "D": "L",
    "L": "U",
}

TURN_L = {
    "U": "L",
    "R": "U",
    "D": "R",
    "L": "D",
}

FACING_VALUE = {
    "U": 3,
    "R": 0,
    "D": 1,
    "L": 2,
}

MAP_LINES_EX = [
    "        ...#",
    "        .#..",
    "        #...",
    "        ....",
    "...#.......#",
    "........#...",
    "..#....#....",
    "..........#.",
    "        ...#....",
    "        .....#..",
    "        .#......",
    "        ......#.",
]

CUBE = {
    True: {
        "side_size": 4,
        "layout": (3, 4),
        "faces_plan": [
            "  A ",
            "DCB ",
            "  EF",
        ],
        # Eg: Going out of "A" facing "L" becomes going in on "C" facing "D"
        "wrapping": {
            ("A", "L"): ("C", "D"),
            ("A", "U"): ("D", "D"),
            ("A", "R"): ("F", "L"),
            ("D", "U"): ("A", "D"),
            ("D", "L"): ("F", "U"),
            ("D", "D"): ("E", "U"),
            ("C", "U"): ("A", "R"),
            ("C", "D"): ("E", "R"),
            ("B", "R"): ("F", "D"),
            ("E", "L"): ("C", "U"),
            ("E", "D"): ("D", "U"),
            ("F", "U"): ("B", "L"),
            ("F", "R"): ("A", "L"),
            ("F", "D"): ("D", "R"),
        },
    }
}


def find_quadrant(p: P, example: bool = True) -> P:
    """
    >>> find_quadrant((1, 3))
    (0, 0)
    >>> find_quadrant((8, 2))
    (2, 0)
    >>> find_quadrant((10, 6))
    (2, 1)
    >>> find_quadrant((11, 15))
    (2, 3)
    """
    cube = CUBE[example]
    return (p[0] // cube["side_size"], p[1] // (cube["side_size"]))  # type: ignore


def find_face(p: P, example: bool = True) -> P:
    """
    >>> find_face((1, 10))
    'A'
    >>> find_face((7, 2))
    'D'
    >>> find_face((6, 6))
    'C'
    >>> find_face((11, 15))
    'F'
    """
    cube = CUBE[example]
    q = find_quadrant(p, example)
    return cube["faces_plan"][q[0]][q[1]]  # type: ignore


def matrix_to_str(matrix: Matrix) -> str:
    return "\n".join(["".join(row) for row in matrix])


def create_matrix(map_lines: list[str]) -> Matrix:
    """
    >>> matrix = create_matrix(MAP_LINES_EX)
    >>> matrix_to_str(matrix)
    '        ...#    \\n        .#..    \\n        #...    \\n        ....    \\n...#.......#    \\n........#...    \\n..#....#....    \\n..........#.    \\n        ...#....\\n        .....#..\\n        .#......\\n        ......#.'
    """
    num_rows = len(map_lines)
    num_cols = max([len(line) for line in map_lines])
    matrix: list[list[str]] = [[" " for _ in range(num_cols)] for _ in range(num_rows)]
    for i in range(num_rows):
        for j in range(num_cols):
            v = " " if j >= len(map_lines[i]) else map_lines[i][j]
            matrix[i][j] = v
    # print(matrix_to_str(matrix))
    return matrix


def get_starting_point(matrix: Matrix) -> P | None:
    """
    >>> matrix = create_matrix(MAP_LINES_EX)
    >>> get_starting_point(matrix)
    (0, 8)
    """
    for r, row in enumerate(matrix):
        for c, v in enumerate(row):
            if v == ".":
                return (r, c)
    return None


def walk_wrap(p: P, v: P, num_rows: int, num_cols: int) -> P:
    p2_r = (p[0] + v[0]) % num_rows
    p2_c = (p[1] + v[1]) % num_cols
    p2_r = p2_r + num_rows if p2_r < 0 else p2_r
    p2_c = p2_c + num_cols if p2_c < 0 else p2_c
    return (p2_r, p2_c)


def walk_wrap_cube(p: P, v: P, num_rows: int, num_cols: int) -> P:
    p2_r = (p[0] + v[0]) % num_rows
    p2_c = (p[1] + v[1]) % num_cols
    p2_r = p2_r + num_rows if p2_r < 0 else p2_r
    p2_c = p2_c + num_cols if p2_c < 0 else p2_c
    return (p2_r, p2_c)


def do_the_walk(matrix: Matrix, start: P, facing: str, distance: int) -> P:
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    direction = DIRECTIONS[facing]
    p1_r, p1_c = start
    for _ in range(distance):
        p2_r, p2_c = walk_wrap((p1_r, p1_c), direction, num_rows, num_cols)
        # If it's walking into a whitespace, continue walking
        while matrix[p2_r][p2_c] == " ":
            p2_r, p2_c = walk_wrap((p2_r, p2_c), direction, num_rows, num_cols)  # type: ignore
        # Hit the wall -> Stop
        if matrix[p2_r][p2_c] == "#":
            return (p1_r, p1_c)
        # Walk 1 point
        if matrix[p2_r][p2_c] == ".":
            p1_r, p1_c = p2_r, p2_c
            continue
    return (p1_r, p1_c)


def do_the_walk_cube(matrix: Matrix, start: P, facing: str, distance: int) -> P:
    num_rows = len(matrix)
    num_cols = max([len(line) for line in matrix])
    direction = DIRECTIONS[facing]
    p1_r, p1_c = start
    for _ in range(distance):
        p2_r, p2_c = walk_wrap((p1_r, p1_c), direction, num_rows, num_cols)
        # If it's walking into a whitespace, continue walking
        while matrix[p2_r][p2_c] == " ":
            p2_r, p2_c = walk_wrap((p2_r, p2_c), direction, num_rows, num_cols)  # type: ignore
        # Hit the wall -> Stop
        if matrix[p2_r][p2_c] == "#":
            return (p1_r, p1_c)
        # Walk 1 point
        if matrix[p2_r][p2_c] == ".":
            p1_r, p1_c = p2_r, p2_c
            continue
    return (p1_r, p1_c)


def final_password(p: P, facing: str) -> int:
    """
    >>> final_password((5, 7), "R")
    6032
    >>> final_password((4, 6), "U")
    5031
    """
    return 1000 * (p[0] + 1) + 4 * (p[1] + 1) + FACING_VALUE[facing]


def navigate(map_lines: list[str], instructions: str, wrap_cube: bool = False) -> tuple[P, str]:
    """
    >>> navigate(MAP_LINES_EX, "10R5L5R10L4R5L5")
    ((5, 7), 'R')
    >>> navigate(MAP_LINES_EX, "10R5L5R10L4R5L5", wrap_cube=True)
    ((4, 6), 'U')
    """
    do_the_walk_fn = do_the_walk_cube if wrap_cube else do_the_walk
    matrix = create_matrix(map_lines)
    p = get_starting_point(matrix)
    assert p is not None
    facing = "U"
    # An initial rotation to the right was added to make the regex easier to parse
    for rotate, _distance in re.findall(r"([RL])(\d+)", "R" + instructions):
        # Rotate
        facing = TURN_R[facing] if rotate == "R" else TURN_L[facing]
        # Walk
        p = do_the_walk_fn(matrix, p, facing, int(_distance))
    return (p, facing)


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        map_txt, instructions = f.read().rstrip().split("\n\n")
        map_lines = map_txt.split("\n")

    for part in [1, 2]:
        print(f"Part {part}:")
        wrap_cube = False if part == 1 else True
        p, facing = navigate(map_lines, instructions, wrap_cube)
        print(final_password(p, facing))
        print()
    exit()
