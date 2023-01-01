"""
Extremely ugly and convoluted solution. 
"""
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

DIRECTIONS_REV = {v: k for k, v in DIRECTIONS.items()}

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

OPPOSITE_DIR = {
    "U": "D",
    "R": "L",
    "D": "U",
    "L": "R",
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
        # Eg: "A" facing "L" maps into "C" facing "U"
        "wrapping": {
            ("A", "U"): ("D", "U"),
            ("A", "R"): ("F", "R"),
            ("A", "D"): ("B", "U"),  #
            ("A", "L"): ("C", "U"),
            ("B", "U"): ("A", "D"),  #
            ("B", "R"): ("F", "U"),
            ("B", "D"): ("E", "U"),  #
            ("B", "L"): ("C", "R"),  #
            ("C", "U"): ("A", "L"),
            ("C", "R"): ("B", "L"),  #
            ("C", "D"): ("E", "L"),
            ("C", "L"): ("D", "R"),  #
            ("D", "U"): ("A", "U"),
            ("D", "R"): ("C", "L"),  #
            ("D", "D"): ("E", "D"),
            ("D", "L"): ("F", "D"),
            ("E", "U"): ("B", "D"),  #
            ("E", "R"): ("F", "L"),  #
            ("E", "D"): ("D", "D"),
            ("E", "L"): ("C", "D"),
            ("F", "U"): ("B", "R"),
            ("F", "R"): ("A", "R"),
            ("F", "D"): ("D", "L"),
            ("F", "L"): ("E", "R"),  #
        },
    },
    False: {
        "side_size": 50,
        "layout": (4, 3),
        "faces_plan": [
            " AB",
            " C ",
            "DE ",
            "F  ",
        ],
        # Eg: "A" facing "L" maps into "C" facing "U"
        "wrapping": {
            ("A", "U"): ("F", "L"),
            ("A", "R"): ("B", "L"),  #
            ("A", "D"): ("C", "U"),  #
            ("A", "L"): ("D", "L"),
            ("B", "U"): ("F", "D"),
            ("B", "R"): ("E", "R"),
            ("B", "D"): ("C", "R"),
            ("B", "L"): ("A", "R"),  #
            ("C", "U"): ("A", "D"),  #
            ("C", "R"): ("B", "D"),
            ("C", "D"): ("E", "U"),  #
            ("C", "L"): ("D", "U"),
            ("D", "U"): ("C", "L"),
            ("D", "R"): ("E", "L"),  #
            ("D", "D"): ("F", "U"),  #
            ("D", "L"): ("A", "L"),
            ("E", "U"): ("C", "D"),  #
            ("E", "R"): ("B", "R"),
            ("E", "D"): ("F", "R"),
            ("E", "L"): ("D", "R"),  #
            ("F", "U"): ("D", "D"),  #
            ("F", "R"): ("E", "D"),
            ("F", "D"): ("B", "U"),
            ("F", "L"): ("A", "U"),
        },
    },
}


def face_to_quadrant(face: str, example: bool = True) -> P:
    """
    >>> face_to_quadrant("A")
    (0, 2)
    """
    cube = CUBE[example]
    ftq: dict[str, P] = {}
    line: str
    for r, line in enumerate(cube["faces_plan"]):  # type: ignore
        _face: str
        for c, _face in enumerate(line):
            ftq[_face] = (r, c)
    return ftq[face]


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


def get_borders(face: str, example: bool = True) -> dict[str, list[P]]:
    """
    >>> get_borders("A")
    {'U': [(0, 8), (0, 9), (0, 10), (0, 11)], 'R': [(0, 11), (1, 11), (2, 11), (3, 11)], 'D': [(3, 11), (3, 10), (3, 9), (3, 8)], 'L': [(3, 8), (2, 8), (1, 8), (0, 8)]}
    """
    cube = CUBE[example]
    q = face_to_quadrant(face, example)
    side: int = cube["side_size"]  # type: ignore
    p_ul = (q[0] * side, q[1] * side)
    p_ur = (p_ul[0], p_ul[1] + side - 1)
    p_dl = (p_ul[0] + side - 1, p_ul[1])
    p_dr = (p_ul[0] + side - 1, p_ul[1] + side - 1)
    return {
        "U": [(p_ul[0], i) for i in range(p_ul[1], p_ur[1] + 1)],
        "R": [(i, p_ur[1]) for i in range(p_ur[0], p_dr[0] + 1)],
        "D": [(p_dr[0], i) for i in range(p_dr[1], p_dl[1] - 1, -1)],
        "L": [(i, p_dl[1]) for i in range(p_dl[0], p_ul[0] - 1, -1)],
    }


def find_index(p: P, direction: str, example: bool = True) -> int:
    """The distance from the quadrant limit

    >>> find_index((3, 10), "D")
    1
    >>> find_index((5, 11), "R")
    1
    """
    cube = CUBE[example]
    side: int = cube["side_size"]  # type: ignore
    q = find_quadrant(p, example)
    d_r = p[0] - q[0] * side
    d_c = p[1] - q[1] * side
    if direction == "D":
        return side - 1 - d_c
    if direction == "U":
        return d_c
    if direction == "L":
        return side - 1 - d_r
    if direction == "R":
        return d_r
    assert False


def get_indexed_point(face: str, direction: str, index: int, example: bool = True) -> P:
    """
    >>> get_indexed_point("B", "U", 2)
    (4, 10)
    """
    borders = get_borders(face, example)
    return borders[direction][index]


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


def walk_wrap_cube(p: P, v: P, num_rows: int, num_cols: int, example: bool = True) -> tuple[P, P]:
    """Returns the next point in the wrapped walk, and the next direction.

    >>> walk_wrap_cube((3, 10), (1, 0), 12, 16)
    ((4, 10), (1, 0))
    >>> walk_wrap_cube((5, 11), (0, 1), 12, 16)
    ((8, 14), (1, 0))
    """
    side = CUBE[example]["side_size"]
    face1 = find_face(p, example)
    p2 = walk_wrap(p, v, num_rows, num_cols)
    face2 = find_face(p2, example)
    # If point on the same face, no wrapping is needed
    if face1 == face2:
        return (p2, v)
    # Wrap previous point to the next face
    direction1 = DIRECTIONS_REV[v]  # type: ignore
    new_face, direction2 = CUBE[example]["wrapping"][(face1, direction1)]  # type: ignore
    index = find_index(p, direction1, example)
    p3 = get_indexed_point(new_face, direction2, side - 1 - index, example)  # type: ignore
    new_direction = OPPOSITE_DIR[direction2]  # type: ignore
    return (p3, DIRECTIONS[new_direction])


def do_the_walk(matrix: Matrix, start: P, facing: str, distance: int, example: bool = True) -> tuple[P, str]:
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
            return ((p1_r, p1_c), facing)
        # Walk 1 point
        if matrix[p2_r][p2_c] == ".":
            p1_r, p1_c = p2_r, p2_c
            continue
    return ((p1_r, p1_c), facing)


def do_the_walk_cube(matrix: Matrix, start: P, facing: str, distance: int, example: bool = True) -> tuple[P, str]:
    num_rows = len(matrix)
    num_cols = max([len(line) for line in matrix])
    direction = DIRECTIONS[facing]
    p1_r, p1_c = start
    for _ in range(distance):
        p2, new_direction = walk_wrap_cube((p1_r, p1_c), direction, num_rows, num_cols, example)
        p2_r, p2_c = p2
        assert matrix[p2_r][p2_c] != " "
        # Hit the wall -> Stop
        if matrix[p2_r][p2_c] == "#":
            return ((p1_r, p1_c), DIRECTIONS_REV[direction])  # type: ignore
        # Walk 1 point
        if matrix[p2_r][p2_c] == ".":
            p1_r, p1_c = p2_r, p2_c
            direction = new_direction
            continue
    return ((p1_r, p1_c), DIRECTIONS_REV[direction])  # type: ignore


def final_password(p: P, facing: str) -> int:
    """
    >>> final_password((5, 7), "R")
    6032
    >>> final_password((4, 6), "U")
    5031
    """
    return 1000 * (p[0] + 1) + 4 * (p[1] + 1) + FACING_VALUE[facing]


def navigate(map_lines: list[str], instructions: str, wrap_cube: bool = False, example: bool = True) -> tuple[P, str]:
    """
    navigate(MAP_LINES_EX, "10R5L5R10L4R5L5")
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
        p, facing = do_the_walk_fn(matrix, p, facing, int(_distance), example)
    return (p, facing)


if __name__ == "__main__":
    assert not doctest.testmod().failed
    # exit()

    with open(FILE_INPUT) as f:
        map_txt, instructions = f.read().rstrip().split("\n\n")
        map_lines = map_txt.split("\n")

    for part in [1, 2]:
        print(f"Part {part}:")
        wrap_cube = False if part == 1 else True
        p, facing = navigate(map_lines, instructions, wrap_cube, example=False)
        print(final_password(p, facing))
        print()
    exit()
