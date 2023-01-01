import doctest
from functools import lru_cache
import re
import sys
from typing import Callable

sys.setrecursionlimit(100_000)

Amount = tuple[int, int, int, int]

FILE_INPUT = "puzzles/day19_input.txt"
TOTAL_MINUTES = 24
INITIAL_ROBOTS = (1, 0, 0, 0)
RESOURCE_INDEX = {
    "ore": 0,
    "clay": 1,
    "obsidian": 2,
    "geode": 3,
}


def get_blueprints(lines: list[str]) -> list[dict[str, Amount]]:
    """
    >>> lines = [
    ...     "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.",
    ...     "Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.",
    ... ]
    >>> get_blueprints(lines)
    [{'ore': (4, 0, 0, 0), 'clay': (2, 0, 0, 0), 'obsidian': (3, 14, 0, 0), 'geode': (2, 0, 7, 0)}, {'ore': (2, 0, 0, 0), 'clay': (3, 0, 0, 0), 'obsidian': (3, 8, 0, 0), 'geode': (3, 0, 12, 0)}]
    """
    blueprints: list[dict[str, Amount]] = []
    for line in lines:
        robot_costs: dict[str, Amount] = {}
        line = re.sub(r"^Blueprint \d+: ", "", line) + " "
        blocks = line.split(". ")
        for block in blocks:
            if not block:
                continue
            _costs = [0, 0, 0, 0]
            r1 = re.search(r"Each (\w+) robot costs (.+)", block)
            assert r1 is not None
            material1, resources_txt = r1.groups()
            for resource_txt in resources_txt.split(" and "):
                n, material2 = resource_txt.split(" ")
                _costs[RESOURCE_INDEX[material2]] = int(n)
            robot_costs[material1] = tuple(_costs)  # type: ignore
        blueprints.append(robot_costs)
    return blueprints


def make_dp_turn(blueprint: dict[str, Amount]) -> Callable[[int, Amount, Amount], int]:
    """Returns the memoized DP function.
    This closure allows the DP function to use blueprint without being passed as an argument

    >>> blueprint1 = {'ore': (4, 0, 0, 0), 'clay': (2, 0, 0, 0), 'obsidian': (3, 14, 0, 0), 'geode': (2, 0, 7, 0)}
    >>> blueprint2 = {'ore': (2, 0, 0, 0), 'clay': (3, 0, 0, 0), 'obsidian': (3, 8, 0, 0), 'geode': (3, 0, 12, 0)}

    >>> dp_turn = make_dp_turn(blueprint1)
    >>> dp_turn(24, (0, 0, 0, 1), (0, 0, 0, 0))
    24
    >>> dp_turn = make_dp_turn(blueprint1)
    >>> dp_turn(24, (1, 0, 0, 0), (0, 0, 0, 0))
    9
    >>> dp_turn = make_dp_turn(blueprint2)
    >>> dp_turn(24, (1, 0, 0, 0), (0, 0, 0, 0))
    12
    """

    @lru_cache(maxsize=None)
    def dp_turn(minutes_left: int, robots: Amount, resources: Amount) -> int:
        """Dynamic Programming function
        Returns the maximum number of geodes that is possible to get given the initial conditions
        """
        # print(robot_costs)
        possible_number_geodes: list[int] = []

        # Option A: Build nothing until the end
        end_resources = [res + rob * minutes_left for res, rob in zip(resources, robots)]
        possible_number_geodes.append(end_resources[RESOURCE_INDEX["geode"]])

        # Option B: Build a robot of resource_type. Start with geode
        if minutes_left > 1:  # We only want another robot if it has time to contribute
            for robot_resource, index in reversed(RESOURCE_INDEX.items()):
                robot_cost = blueprint[robot_resource]

                # Don't build the robot if we already generate more resources of that type than we will ever need
                max_resource_needed_per_min = max([costs[index] for costs in blueprint.values()])
                if robot_resource != "geode" and robots[index] >= max_resource_needed_per_min:
                    continue

                can_build_now = True if all([res >= cost for res, cost in zip(resources, robot_cost)]) else False
                can_build_later = all(
                    [not bool(cost) or (bool(cost) and bool(num_rob)) for cost, num_rob in zip(robot_cost, robots)]
                )
                if not (can_build_now or can_build_later):
                    continue
                if can_build_now:
                    waiting_minutes = 0
                else:
                    waiting_minutes = -1
                    for i in RESOURCE_INDEX.values():
                        if robot_cost[i] > resources[i] and robots[i] > 0:
                            # The integer division // always rounds down. But we want to round up.
                            # So we use a negative numerator, to get a floored negative result,
                            # and then negate, to get a ceiling positive result.
                            waiting_minutes = max(waiting_minutes, -((resources[i] - robot_cost[i]) // robots[i]))
                    assert waiting_minutes > 0
                # Don't build the robot if there's no time
                if waiting_minutes >= minutes_left:
                    continue
                # Spend the resources in the new robot
                new_resources = [res - cost for res, cost in zip(resources, robot_cost)]
                # Increase the resources by waiting the amount of minutes needed to gather the resources AND build the robot
                new_resources = [res + (waiting_minutes + 1) * num_rob for res, num_rob in zip(new_resources, robots)]
                new_robots = list(robots)
                new_robots[index] += 1
                possible_number_geodes.append(
                    dp_turn(minutes_left - waiting_minutes - 1, tuple(new_robots), tuple(new_resources))
                )
                # If we were able to build a geode robot without waiting, don't even test the other options
                if waiting_minutes == 0 and robot_resource == "geode":
                    break

        # Select the best of the options
        return max(possible_number_geodes)

    return dp_turn


def sum_quality_levels(results: list[int]) -> int:
    """
    >>> sum_quality_levels([9, 12])
    33
    """
    return sum([(i + 1) * result for i, result in enumerate(results)])


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        lines = f.read().rstrip().split("\n")

    blueprint: dict[str, Amount] = {}
    blueprints = get_blueprints(lines)
    results: list[int] = []
    for i, blueprint in enumerate(blueprints):
        print(f"{i + 1}: {blueprint}")
        dp_turn = make_dp_turn(blueprint)
        max_num_geodes = dp_turn(TOTAL_MINUTES, INITIAL_ROBOTS, (0, 0, 0, 0))
        print(max_num_geodes)
        results.append(max_num_geodes)

    print(sum_quality_levels(results))
    exit()
