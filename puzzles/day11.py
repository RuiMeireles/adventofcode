import doctest
from collections import Counter
from typing import Any, Dict, List

FILE_INPUT_EX = "puzzles/day11_input_ex.txt"
FILE_INPUT = "puzzles/day11_input.txt"
NUM_ROUNDS = {
    "part_1": 20,
    "part_2": 10_000,
}


def process_input(lines: List[str]) -> List[Dict[str, Any]]:
    monkey_num = 0
    monkeys: List[Dict[str, Any]] = []
    for line in lines:
        words = line.split(" ")

        if words[0] == "Monkey":
            monkey_num = int(words[1].split(":")[0])
            monkeys.append({})

        if words[0] == "Starting":
            numbers_txt = line.split(": ")[1]
            items = [int(n) for n in numbers_txt.split(", ")]
            monkeys[monkey_num]["items"] = items

        if words[0] == "Operation:":
            operation_txt = line.split(" = ")[1]
            operators = operation_txt.split(" ")
            monkeys[monkey_num]["operators"] = [operators[-2], operators[-1]]

        if words[0] == "Test:":
            divisor = int(line.split(" ")[-1])
            monkeys[monkey_num]["test_divisor"] = divisor

        if words[0] == "If" and words[1] == "true:":
            monkey_to = int(line.split(" ")[-1])
            monkeys[monkey_num]["if_test_true"] = monkey_to

        if words[0] == "If" and words[1] == "false:":
            monkey_to = int(line.split(" ")[-1])
            monkeys[monkey_num]["if_test_false"] = monkey_to

    # Build "items_mod" keys for Part 2
    divisors = sorted([m["test_divisor"] for m in monkeys])
    item_id = 0
    for monkey in monkeys:
        for item in monkey["items"]:
            monkey.setdefault("items_mod", {})
            monkey["items_mod"][item_id] = {divisor: item % divisor for divisor in divisors}
            item_id += 1
    return monkeys


def part_1(monkeys: List[Dict[str, Any]]) -> Counter[int]:
    inspected: Counter[int] = Counter()
    num_rounds = NUM_ROUNDS["part_1"]
    for _ in range(num_rounds):
        for m, monkey in enumerate(monkeys):
            for item in monkey["items"]:
                # Inspect
                inspected[m] += 1
                # Worry level goes up
                operation_txt, operator_txt = monkey["operators"]
                operator = int(operator_txt) if operator_txt.isdigit() else item
                if operation_txt == "+":
                    item = item + operator
                elif operation_txt == "-":
                    item = item - operator
                elif operation_txt == "*":
                    item = item * operator
                # Worry level goes down
                item //= 3
                # Test and throw item to other monkey
                if not item % monkey["test_divisor"]:
                    monkeys[monkey["if_test_true"]]["items"].append(item)
                else:
                    monkeys[monkey["if_test_false"]]["items"].append(item)
            # Monkey has no items now
            monkey["items"] = []
    return inspected


def part_2(monkeys: List[Dict[str, Any]]) -> Counter[int]:
    inspected: Counter[int] = Counter()
    num_rounds = NUM_ROUNDS["part_2"]
    for num_round in range(num_rounds):
        for m, monkey in enumerate(monkeys):
            for item_id, modulos in monkey["items_mod"].items():
                item = None
                # Inspect
                inspected[m] += 1
                # Worry level goes up
                operation_txt, operator_txt = monkey["operators"]
                operator = int(operator_txt) if operator_txt.isdigit() else None
                if operation_txt == "+":
                    assert operator is not None
                    item = {divisor: (modulo + operator) % divisor for divisor, modulo in modulos.items()}
                elif operation_txt == "-":
                    assert operator is not None
                    item = {divisor: (modulo - operator) % divisor for divisor, modulo in modulos.items()}
                elif operation_txt == "*":
                    if operator is not None:
                        item = {divisor: (modulo * operator) % divisor for divisor, modulo in modulos.items()}
                    else:
                        item = {divisor: (modulo * modulo) % divisor for divisor, modulo in modulos.items()}
                # Worry level doesn't go down
                # (do nothing)
                # Test and throw item to other monkey
                assert item is not None
                if item[monkey["test_divisor"]] == 0:
                    monkeys[monkey["if_test_true"]]["items_mod"][item_id] = item
                else:
                    monkeys[monkey["if_test_false"]]["items_mod"][item_id] = item
            # Monkey has no items now
            monkey["items_mod"] = {}
        # End of round
        if num_round + 1 in [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]:
            print(num_round + 1, dict(inspected))
    return inspected


def monkey_business(inspected: Counter[int]) -> int:
    monkey_business = 1
    for _, i in inspected.most_common()[0:2]:
        monkey_business *= i
    return monkey_business


if __name__ == "__main__":
    assert not doctest.testmod().failed

    # with open(FILE_INPUT_EX) as f:
    with open(FILE_INPUT) as f:
        lines = f.read().rstrip().split("\n")
        lines = [line.strip() for line in lines]

    # Part 1
    monkeys = process_input(lines)
    inspected = part_1(monkeys)
    print(monkey_business(inspected))
    # Part 2
    monkeys = process_input(lines)
    inspected = part_2(monkeys)
    print(monkey_business(inspected))
    exit()
