import doctest
from functools import lru_cache
from itertools import permutations
from queue import PriorityQueue
from timeit import default_timer as timer
from typing import Dict, List, NamedTuple, Set, Tuple
import sys

sys.setrecursionlimit(100_000)

RUN_EXAMPLE = False
FILE_INPUT_EX = "src/adventofcode2022/day16_input_ex.txt"
FILE_INPUT = "src/adventofcode2022/day16_input.txt"
TOTAL_MINUTES_PART1 = 30
TOTAL_MINUTES_PART2 = 26
STARTING_NODE = "AA"
NUM_VALVES_PLAYER_1 = 12


class PathElement(NamedTuple):
    cost: int
    to_node: str
    path: List[str]


# Global Variables
nodes: Set[str] = set()  # The names of the nodes
connected_to: Dict[str, List[str]] = {}  # The connections between nodes
valve_rates: Dict[str, int] = {}  # The rate of each node's valve when open
openable_valves: Set[str] = set()  # The valves that are closed at the beginning
best_paths: Dict[str, Dict[str, PathElement]]  # The Dijkstra's algorythm results


def dijkstra_cost_1(node: str, connected_to: Dict[str, List[str]]) -> Dict[str, PathElement]:
    """
    Implements Dijkstra's algorithm to figure out the shortest paths from 1 node to all other nodes.
    It assumes that all costs between nodes are 1.
    """
    pq: PriorityQueue[PathElement] = PriorityQueue()
    shortest_paths: Dict[str, PathElement] = {}
    cost = 1

    # Add itself to the shortest_paths
    shortest_paths[node] = PathElement(0, node, [])
    # Initial population of queue
    for n in connected_to[node]:
        pq.put(PathElement(cost, n, [n]))

    while not pq.empty():
        path_element = pq.get()
        new_node = path_element.to_node
        # Ignore path if we already have a better path to that node
        if new_node in shortest_paths:
            continue
        # Add node to shortest path
        shortest_paths[new_node] = path_element
        # Add node paths to queue
        for n in connected_to[new_node]:
            if n not in shortest_paths:
                pq.put(PathElement(path_element.cost + cost, n, path_element.path.copy() + [n]))
    return shortest_paths


@lru_cache(maxsize=None)
def dp_part_1(node: str, minutes_left: int, open_valves: Tuple[str, ...]) -> int:
    """
    Part 1
    Dynamic Programming approach
    Returns the amount of pressure that this state can generate in the remaining time
    """
    options: List[int] = []
    rate = sum([valve_rates[v] for v in open_valves])
    # If time is over
    if minutes_left <= 0:
        return 0
    # A) Do nothing until the end
    options.append(minutes_left * rate)
    # B) If valve can still be opened
    if node in openable_valves and node not in open_valves:
        next_open_valves = tuple(sorted(list(open_valves) + [node]))
        options.append(dp_part_1(node, minutes_left - 1, next_open_valves) + rate)
    # C) Try available tunnels
    for next_node, path in best_paths[node].items():
        # Only travel to nodes with unopened valves
        if next_node not in (openable_valves - set(open_valves) - set([node])):
            continue
        pressure_while_travelling = min(path.cost, minutes_left) * rate
        options.append(dp_part_1(next_node, minutes_left - path.cost, open_valves) + pressure_while_travelling)
    return max(options)


@lru_cache(maxsize=None)
def dp_part_2(
    node: str, minutes_left: int, open_valves: Tuple[str, ...], openable_valves: Tuple[str, ...], num_player: int
) -> int:
    """
    Part 2
    Dynamic Programming approach
    Returns the amount of pressure that this state can generate in the remaining time
    """
    options: List[int] = []
    rate = sum([valve_rates[v] for v in open_valves])
    # If time is over
    if minutes_left <= 0:
        if num_player == 1:
            return 0
        # Now do the elephant's turn
        remaining_valves = tuple(sorted(list(set(openable_valves) - set(open_valves))))
        other_players_pressure = dp_part_2(
            STARTING_NODE, TOTAL_MINUTES_PART2, tuple([]), remaining_valves, num_player - 1
        )
        return other_players_pressure
    # A) Do nothing until the end
    if num_player == 1:
        options.append(minutes_left * rate)
    # Hack: only "do nothing" when we already have X open valves
    ### else:
    elif RUN_EXAMPLE or len(open_valves) == NUM_VALVES_PLAYER_1:
        remaining_valves = tuple(sorted(list(set(openable_valves) - set(open_valves))))
        other_players_pressure = dp_part_2(
            STARTING_NODE, TOTAL_MINUTES_PART2, tuple([]), remaining_valves, num_player - 1
        )
        options.append(minutes_left * rate + other_players_pressure)
    # B) If valve can still be opened
    if node in openable_valves and node not in open_valves:
        # Hack
        if RUN_EXAMPLE or (num_player > 1 and len(open_valves) < NUM_VALVES_PLAYER_1):
            next_open_valves = tuple(sorted(list(open_valves) + [node]))
            options.append(dp_part_2(node, minutes_left - 1, next_open_valves, openable_valves, num_player) + rate)
    # C) Try available tunnels
    for next_node, path in best_paths[node].items():
        # Only travel to nodes with unopened valves
        if next_node not in (set(openable_valves) - set(open_valves) - set([node])):
            continue
        pressure_while_travelling = min(path.cost, minutes_left) * rate
        if RUN_EXAMPLE or (num_player > 1 and len(open_valves) < NUM_VALVES_PLAYER_1):
            options.append(
                dp_part_2(next_node, minutes_left - path.cost, open_valves, openable_valves, num_player)
                + pressure_while_travelling
            )
    return max(options)


if __name__ == "__main__":
    assert not doctest.testmod().failed

    # Read input
    file_input = FILE_INPUT_EX if RUN_EXAMPLE else FILE_INPUT
    with open(file_input) as f:
        lines = f.read().rstrip().split("\n")
        for line in lines:
            words = line.split(" ")
            valve = words[1]
            rate = int(words[4].split("=")[1][:-1])
            valves_connected = " ".join(words[9:]).split(", ")
            # Build variables
            nodes.add(valve)
            connected_to[valve] = valves_connected
            valve_rates[valve] = rate
            if rate != 0:
                openable_valves.add(valve)

    #####
    # Part 1
    #####

    # Step 1: Calculate best paths from all nodes to all nodes
    best_paths = {node: dijkstra_cost_1(node, connected_to) for node in nodes}
    # Assert
    for i in nodes:
        for j in nodes:
            assert best_paths[i][j].cost == best_paths[j][i].cost

    # Solution A: Bruteforce (only runs with the example)
    if RUN_EXAMPLE:
        # Step 2: Explore all possible opening sequences of the closed valves
        # With example: 6 nodes = 720 sequences
        # With problem input: 16 nodes = can't even compute the the permutations...
        print("Solution A: Bruteforce - Check all permutations")
        start = timer()
        total_rates: Dict[Tuple[str, ...], int] = {}
        for opening_sequence in permutations(openable_valves):
            node_cur = STARTING_NODE
            minutes_left = TOTAL_MINUTES_PART1
            total_pressure = 0
            for node in opening_sequence:
                # Walk to node
                minutes_left -= best_paths[node_cur][node].cost
                node_cur = node
                if minutes_left <= 0:
                    break
                # Open valve
                minutes_left -= 1
                if minutes_left <= 0:
                    break
                total_pressure += minutes_left * valve_rates[node]
            total_rates[opening_sequence] = total_pressure
        print(sorted([(v, k) for k, v in total_rates.items()])[-1])
        print(f"{timer() - start:4f} seconds")

    # Solution B: Dynamic Programming (DP)
    print("Solution B: Dynamic Programming")
    start = timer()
    ###print(dp_part_1(STARTING_NODE, TOTAL_MINUTES_PART1, tuple([])))
    print(f"{timer() - start:4f} seconds")

    #####
    # Part 2 - Dynamic Programming (DP)
    #####
    print("Part 2: Dynamic Programming")
    start = timer()
    print(dp_part_2(STARTING_NODE, TOTAL_MINUTES_PART2, tuple([]), tuple(sorted(list(openable_valves))), 2))
    print(f"{timer() - start:4f} seconds")

    # Wrong answers: 1442, 1490
    exit()
