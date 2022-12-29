from collections import deque
from dataclasses import dataclass
import doctest
from functools import lru_cache
from typing import NamedTuple


class P(NamedTuple):
    x: int
    y: int


@dataclass
class Blizzard:
    p: P
    dir: P
    limits: tuple[int, int, int, int]

    def move(self, turns: int) -> P:
        """
        >>> b = Blizzard(P(3, 1), P(-1, 0), (0, 7, 0, 5))
        >>> b.move(1)
        P(x=2, y=1)
        >>> b = Blizzard(P(5, 1), P(0, -1), (0, 7, 0, 5))
        >>> b.move(1)
        P(x=5, y=4)
        """
        x_min, x_max, y_min, y_max = self.limits
        d_x = x_max - x_min - 1
        d_y = y_max - y_min - 1
        return P(
            (self.p.x - x_min - 1 + self.dir.x * turns) % d_x + x_min + 1,
            (self.p.y - y_min - 1 + self.dir.y * turns) % d_y + y_min + 1,
        )


FILE_INPUT = "puzzles/day24_input.txt"
DIR = {
    ">": P(1, 0),
    "v": P(0, 1),
    "<": P(-1, 0),
    "^": P(0, -1),
}
# Global vars
start: P
end: P
limits: tuple[int, int, int, int]
moves_stack: deque[tuple[P, int]]
blizzards: list[Blizzard]


@lru_cache(maxsize=None)
def blizzards_at_turn(turn: int) -> set[P]:
    """Returns the set of points with blizzards at a given turn"""
    blizzards_at_turn: set[P] = set()
    for b in blizzards:
        blizzards_at_turn.add(b.move(turn))
    return blizzards_at_turn


def print_blizzards(blizzard_state: set[P]) -> None:
    x_min, x_max, y_min, y_max = limits
    for y in range(y_min, y_max + 1):
        if y == y_min or y == y_max:
            print("#" * (x_max - x_min + 1))
            continue
        line = ""
        for x in range(x_min, x_max + 1):
            if x == x_min or x == x_max:
                line += "#"
                continue
            c = " " if P(x, y) in blizzard_state else "."
            line += c
        print(line)


def get_neighbors(p: P) -> list[P]:
    return [P(p.x + d.x, p.y + d.y) for d in DIR.values()]


@lru_cache(maxsize=None)
def next_moves(p: P, turn: int, goal: P) -> int:
    """The function that fills the stack for the breadth first search
    It's memoized so that we don't recalculate the same state twice
    """
    global moves_stack
    x_min, x_max, y_min, y_max = limits
    # Determine how the blizzards will be at this time
    blizzard_state = blizzards_at_turn(turn)
    for n in get_neighbors(p):
        if n == goal:
            # We can always move to the goal
            moves_stack.append((n, turn + 1))
            return turn
        if not (x_min < n.x < x_max and y_min < n.y < y_max):
            # We can't move to out of bound points
            continue
        if n in blizzard_state:
            # We can't move to blizzards
            continue
        # Neighbor is good to move to
        moves_stack.append((n, turn + 1))
    if p not in blizzard_state:
        # Also add the option of staying in place
        moves_stack.append((p, turn + 1))
    # Returns 0 if it didn't reach the goal yet
    return 0


def simulate(lines: list[str], part: int) -> int:
    """
    >>> lines = [
    ...     "#.######",
    ...     "#>>.<^<#",
    ...     "#.<..<<#",
    ...     "#>v.><>#",
    ...     "#<^v^^>#",
    ...     "######.#",
    ... ]
    >>> simulate(lines, part=1)
    18
    >>> simulate(lines, part=2)
    54
    """
    # Build blizzards
    global start
    global end
    global limits
    global moves_stack
    global blizzards
    next_moves.cache_clear()
    blizzards_at_turn.cache_clear()
    limits = (0, len(lines[0]) - 1, 0, len(lines) - 1)
    blizzards = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if y == 0:
                if c == ".":
                    start = P(x, y)
                    continue
            if y == len(lines) - 1:
                if c == ".":
                    end = P(x, y)
                    continue
            if c in ">v<^":
                blizzards.append(Blizzard(P(x, y), DIR[c], limits))
    # print_blizzards(blizzards_at_turn(0))

    # Walk the path
    goals = [end] if part == 1 else [end, start, end]
    total_turns = 0
    for goal in goals:
        p = start if goal == end else end
        moves_stack = deque()
        moves_stack.append((p, total_turns + 1))
        ended = 0
        while moves_stack and not ended:
            ended = next_moves(*moves_stack.popleft(), goal)
        total_turns = ended

    return total_turns


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        lines = f.read().rstrip().split("\n")

    print(simulate(lines, part=1))
    print(simulate(lines, part=2))
    exit()
