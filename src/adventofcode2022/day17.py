from collections import deque
from dataclasses import dataclass

# import doctest
from timeit import default_timer as timer
from typing import Callable, Iterator, List, NamedTuple, Union


class P(NamedTuple):
    x: int
    y: int


@dataclass
class Piece:
    type_index: int
    position: P
    ticks: int = 0
    movement: P = P(0, 0)


PRINT_ROCKS = False  # Set it to true to print the rocks
FILE_INPUT = "src/adventofcode2022/day17_input.txt"
EXAMPLE_TXT = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
WALL_L = 0
WALL_R = 8
FLOOR = 0
SPAWN_X = 3  # Leave 2 gaps to the left wall
SPAWN_Y = 4  # Leave 3 gaps to the tallest rock
NUM_PIECES_1 = 2022
NUM_PIECES_2 = 1_000_000_000_000
PIECES = (
    # ####
    (P(0, 0), P(1, 0), P(2, 0), P(3, 0)),
    # .#.
    # ###
    # .#.
    (P(1, 0), P(0, 1), P(1, 1), P(2, 1), P(1, 2)),
    #
    # ..#
    # ..#
    # ###
    (P(0, 0), P(1, 0), P(2, 0), P(2, 1), P(2, 2)),
    # #
    # #
    # #
    # #
    (P(0, 0), P(0, 1), P(0, 2), P(0, 3)),
    # ##
    # ##
    (P(0, 0), P(1, 0), P(0, 1), P(1, 1)),
)

# Global variables
rocks: deque[P] = deque(maxlen=100)
highest_rock = FLOOR
fallen_pieces: List[Piece] = []


def move_piece(p: Piece, direction: P) -> Piece:
    """Returns a new piece, which has moved if possible"""
    p_next = Piece(
        type_index=p.type_index,
        position=P(p.position.x + direction.x, p.position.y + direction.y),
        ticks=p.ticks + 1,
        movement=P(p.movement.x + direction.x, p.movement.y + direction.y),
    )
    piece_blocks = [P(block.x + p_next.position.x, block.y + p_next.position.y) for block in PIECES[p.type_index]]
    for block in piece_blocks:
        if block.x == WALL_L or block.x == WALL_R or block in rocks or block.y == FLOOR:
            # Piece can't move
            return Piece(p.type_index, p.position, p.ticks + 1, p.movement)
    # Piece moves
    return p_next


def wind_direction_maker(wind: str) -> Callable[[], Iterator[P]]:
    """Returns a generator of wind direction"""
    n = 0

    def wind_direction() -> Iterator[P]:
        """Returns the next wind direction"""
        nonlocal n
        w = wind[n % len(wind)]
        n += 1
        yield P(1, 0) if w == ">" else P(-1, 0)

    return wind_direction


def print_rocks(rocks: Union[List[P], deque[P]]) -> None:
    print("+       +")
    for y in range(highest_rock, FLOOR, -1):
        row = [rock.x for rock in rocks if rock.y == y]
        print("|" + "".join(["#" if x in row else " " for x in range(WALL_L + 1, WALL_R)]) + "|")
    print("+-------+")
    print()


def check_for_pattern() -> int:
    """
    Searches for a pattern at the end of fallen_pieces
    Returns the pattern length (number of pieces), or 0 if no pattern was found.
    """
    i_high = len(fallen_pieces) - 1
    p_high = fallen_pieces[i_high]
    # Jumps of 5, starting at 5, until the end of fallen_pieces
    for gap in range(len(PIECES), len(fallen_pieces), len(PIECES)):
        i_low = i_high - gap
        p_low = fallen_pieces[i_low]
        if p_low.movement == p_high.movement and p_low.ticks == p_high.ticks:
            # Check all pairs of pieces separated by gap
            for n in range(gap + 1):
                pn_high = fallen_pieces[i_high - n]
                pn_low = fallen_pieces[i_low - n]
                if not (pn_high.movement == pn_low.movement and pn_high.ticks == pn_low.ticks):
                    # Pattern is broken
                    break
            else:
                # Pattern is found
                return gap
    return 0


def part1(wind: str) -> int:
    """
    >>> part1(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>")
    3068
    """
    global rocks
    global highest_rock
    wind_direction = wind_direction_maker(wind)
    # Iterate through pieces
    for num_piece in range(NUM_PIECES_1):
        print(f"{100*(num_piece + 1)/NUM_PIECES_1:.2f} %", end="\r")
        if PRINT_ROCKS:
            print()
            print_rocks(rocks)
        piece_type = num_piece % len(PIECES)
        p = Piece(piece_type, P(SPAWN_X, SPAWN_Y + highest_rock))
        piece_ticks = 0
        wind_ticks = 0
        # Iterate trough ticks
        while True:
            is_falling = True if piece_ticks % 2 else False
            direction = P(0, -1) if is_falling else next(wind_direction())
            position = p.position
            p = move_piece(p, direction)
            if is_falling and p.position == position:
                # The piece hit the rock
                new_rocks = [P(block.x + p.position.x, block.y + p.position.y) for block in PIECES[p.type_index]]
                highest_rock = max(highest_rock, max([rock.y for rock in new_rocks]))
                rocks += new_rocks
                # Go to next piece
                break
            # Go to next tick
            piece_ticks += 1
            wind_ticks += 1
    print()
    return highest_rock


def part2(wind: str) -> int:
    """
    >>> part1(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>")
    1514285714288
    """
    global rocks
    global highest_rock
    wind_direction = wind_direction_maker(wind)
    pattern_length = 0
    num_piece = 0
    # Iterate through pieces
    for num_piece in range(NUM_PIECES_2):
        if pattern_length:
            print(f"{pattern_length = }")
            break
        print(f"{100*(num_piece + 1)/NUM_PIECES_2:.8f} %", end="\r")
        if PRINT_ROCKS:
            print()
            print_rocks(list(rocks))
        piece_type = num_piece % len(PIECES)
        p = Piece(piece_type, P(SPAWN_X, SPAWN_Y + highest_rock))
        piece_ticks = 0
        wind_ticks = 0
        # Iterate trough ticks
        while True:
            is_falling = True if piece_ticks % 2 else False
            direction = P(0, -1) if is_falling else next(wind_direction())
            position = p.position
            p = move_piece(p, direction)
            if is_falling and p.position == position:
                # The piece hit the rock
                new_rocks = [P(block.x + p.position.x, block.y + p.position.y) for block in PIECES[p.type_index]]
                highest_rock = max(highest_rock, max([rock.y for rock in new_rocks]))
                rocks += new_rocks
                # Go to next piece
                fallen_pieces.append(p)
                if p.type_index == len(PIECES) - 1:
                    pattern_length = check_for_pattern()
                break
            # Go to next tick
            piece_ticks += 1
            wind_ticks += 1

    # A: initial pieces
    # B: 1 x pattern <--- we are here with fallen_pieces
    # C: n x pattern
    # D: remaining pieces

    # Calculate height
    num_remaining_pieces = NUM_PIECES_2 - num_piece
    num_remaining_pattern_reps = num_remaining_pieces // pattern_length
    num_leftover_pieces = num_remaining_pieces % pattern_length

    # We will take the existing pieces in fallen_pieces and:
    # - Remove pieces (1x the pattern)
    # - Add the leftovers pieces
    # - Add the remaining_pattern_reps + 1
    #
    # pbp = piece before pattern
    # pl = plus leftovers
    index_of_pbp = len(fallen_pieces) - pattern_length - 1
    index_of_pbp_pl = index_of_pbp + num_leftover_pieces
    pbp_pl = fallen_pieces[index_of_pbp_pl]
    height_pbp_pl = pbp_pl.position.y + max([p.y for p in PIECES[pbp_pl.type_index]])
    pattern_height = fallen_pieces[-1].position.y - fallen_pieces[-pattern_length - 1].position.y
    total_height = height_pbp_pl + (num_remaining_pattern_reps + 1) * pattern_height
    return total_height


if __name__ == "__main__":
    # assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        wind = f.read().rstrip()

    for run_example in [True, False]:
        for part in [1, 2]:
            print("Example:" if run_example else "Problem:")
            rocks = deque()
            highest_rock = FLOOR
            start = timer()
            if part == 1:
                print("- Part 1:")
                print(part1(EXAMPLE_TXT if run_example else wind))
            else:
                print("- Part 2:")
                print(part2(EXAMPLE_TXT if run_example else wind))
            print(f"{timer() - start:4f} seconds")
            print()
    exit()
