from collections import deque, Counter
from dataclasses import dataclass, field
import doctest
from typing import NamedTuple


class P(NamedTuple):
    x: int
    y: int


FILE_INPUT = "puzzles/day23_input.txt"
NUM_ROUNDS_PART1 = 10
DIR = {
    "N": P(0, 1),
    "NE": P(1, 1),
    "E": P(1, 0),
    "SE": P(1, -1),
    "S": P(0, -1),
    "SW": P(-1, -1),
    "W": P(-1, 0),
    "NW": P(-1, 1),
}
PREFERRED_DIR_ORDER = ("N", "S", "W", "E")


@dataclass
class Elf:
    p: P
    next_dirs: deque[str] = field(default_factory=lambda: deque(PREFERRED_DIR_ORDER))  # type: ignore
    preferred_move: P | None = None


def get_neighbors(p: P) -> list[P]:
    return [P(p.x + d.x, p.y + d.y) for d in DIR.values()]


def preferred_move(elf: Elf, elves_positions: list[P]) -> P | None:
    # Elf doesn't want to move if there's no one around him
    if not (set(get_neighbors(elf.p)) & set(elves_positions)):
        return None
    # Determine preferred move
    for d in elf.next_dirs:
        facing_dirs = [_d for _d in DIR if d in _d]
        facing_moves = [DIR[_d] for _d in facing_dirs]
        facing_points = [P(elf.p.x + p.x, elf.p.y + p.y) for p in facing_moves]
        # If move is clear
        if not (set(facing_points) & set(elves_positions)):
            return P(elf.p.x + DIR[d].x, elf.p.y + DIR[d].y)
    # No places to move to
    return None


def get_min_max(positions: list[P]) -> tuple[int, int, int, int]:
    min_x = min([p.x for p in positions])
    max_x = max([p.x for p in positions])
    min_y = min([p.y for p in positions])
    max_y = max([p.y for p in positions])
    return min_x, max_x, min_y, max_y


def print_elves(positions: list[P]) -> None:
    min_x, max_x, min_y, max_y = get_min_max(positions)
    for y in range(max_y, min_y - 1, -1):
        line = ""
        for x in range(min_x, max_x + 1):
            c = "#" if P(x, y) in positions else "."
            line += c
        print(line)


def simulate(map_lines: list[str]) -> None:
    """
    >>> map_lines = [
    ...     "....#..",
    ...     "..###.#",
    ...     "#...#.#",
    ...     ".#...##",
    ...     "#.###..",
    ...     "##.#.##",
    ...     ".#..#..",
    ... ]
    >>> simulate(map_lines)
    Part 1: 110 empty squares after 10 rounds.
    Part 2: 20 rounds until the elves stop.
    """
    # Build elves
    elves: list[Elf] = []
    for y, line in enumerate(map_lines):
        for x, char in enumerate(line):
            if char == "#":
                p = P(x, len(map_lines) - 1 - y)
                elves.append(Elf(p))

    # Play rounds
    num_round = 0
    preferred_moves: Counter[P] = Counter()
    elves_positions = [elf.p for elf in elves]
    while True:
        if num_round == NUM_ROUNDS_PART1:
            # Part 1 amswer: Determine number of empty squares
            min_x, max_x, min_y, max_y = get_min_max(elves_positions)
            empty_squares = (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves_positions)
            print(f"Part 1: {empty_squares} empty squares after {NUM_ROUNDS_PART1} rounds.")
        # Pre-round: Determine preferred moves
        for elf in elves:
            move = preferred_move(elf, elves_positions)
            elf.preferred_move = move
            if move is not None:
                preferred_moves[move] += 1
        # End if no elf wants to move
        if not preferred_moves:
            break
        # New round starts: Elves move
        num_round += 1
        for elf in elves:
            if elf.preferred_move is None:
                continue
            if preferred_moves[elf.preferred_move] > 1:
                continue
            elf.p = elf.preferred_move
            elf.preferred_move = None
        # Round ended: Prepare for next round
        preferred_moves = Counter()
        elves_positions = [elf.p for elf in elves]
        for elf in elves:
            elf.next_dirs.append(elf.next_dirs.popleft())
        # print(f"End of round {num_round}")
        # print_elves(elves_positions)
        # print()

    print(f"Part 2: {num_round + 1} rounds until the elves stop.")


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        map_lines = f.read().rstrip().split("\n")

    simulate(map_lines)
    exit()
