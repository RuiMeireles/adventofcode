import doctest
import operator
from sympy import Eq, symbols, solve  # type: ignore

FILE_INPUT = "src/adventofcode2022/day21_input.txt"
OPERATORS = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv}


def part1(lines: list[str]) -> int:
    """
    >>> lines = [
    ...     "root: pppw + sjmn",
    ...     "dbpl: 5",
    ...     "cczh: sllz + lgvd",
    ...     "zczc: 2",
    ...     "ptdq: humn - dvpt",
    ...     "dvpt: 3",
    ...     "lfqf: 4",
    ...     "humn: 5",
    ...     "ljgn: 2",
    ...     "sjmn: drzm * dbpl",
    ...     "sllz: 4",
    ...     "pppw: cczh / lfqf",
    ...     "lgvd: ljgn * ptdq",
    ...     "drzm: hmdt - zczc",
    ...     "hmdt: 32",
    ... ]
    >>> part1(lines)
    152
    """
    # Initial setup
    monkeys: dict[str, int] = {}
    equations: dict[str, str] = {}
    for line in lines:
        monkey_name, equation = line.split(": ")
        try:
            n = int(equation)
            monkeys[monkey_name] = n
        except ValueError:
            equations[monkey_name] = equation

    # Solve equations as they become solvable
    while equations:
        monkey_equations_solved: set[str] = set()
        for monkey_name, equation in equations.items():
            m1, op, m2 = equation.split(" ")
            if m1 in monkeys and m2 in monkeys:
                op_function = OPERATORS[op]  # type: ignore
                monkeys[monkey_name] = op_function(monkeys[m1], monkeys[m2])
                monkey_equations_solved.add(monkey_name)
        for monkey in monkey_equations_solved:
            del equations[monkey]

    return monkeys["root"]


def part2(lines: list[str]) -> int:
    """
    >>> lines = [
    ...     "root: pppw + sjmn",
    ...     "dbpl: 5",
    ...     "cczh: sllz + lgvd",
    ...     "zczc: 2",
    ...     "ptdq: humn - dvpt",
    ...     "dvpt: 3",
    ...     "lfqf: 4",
    ...     "humn: 5",
    ...     "ljgn: 2",
    ...     "sjmn: drzm * dbpl",
    ...     "sllz: 4",
    ...     "pppw: cczh / lfqf",
    ...     "lgvd: ljgn * ptdq",
    ...     "drzm: hmdt - zczc",
    ...     "hmdt: 32",
    ... ]
    >>> part2(lines)
    301
    """
    # Initial setup - Ignore "humn"
    monkeys: dict[str, int] = {}
    equations: dict[str, str] = {}
    for line in lines:
        monkey_name, equation = line.split(": ")
        if monkey_name == "humn":
            continue
        try:
            n = int(equation)
            monkeys[monkey_name] = n
        except ValueError:
            equations[monkey_name] = equation

    # Solve equations as they become solvable
    # Since now we don't know the value of human, some of them will remain unsolved
    root_equation = ""
    any_equation_solved = True
    while any_equation_solved:
        any_equation_solved = False
        monkey_equations_solved: set[str] = set()
        for monkey_name, equation in equations.items():
            assert monkey_name != "humn"
            if monkey_name == "root":
                root_equation = equation
                monkey_equations_solved.add(monkey_name)
                continue
            m1, op, m2 = equation.split(" ")
            if m1 in monkeys and m2 in monkeys:
                op_function = OPERATORS[op]  # type: ignore
                monkeys[monkey_name] = op_function(monkeys[m1], monkeys[m2])
                monkey_equations_solved.add(monkey_name)
                any_equation_solved = True
        for monkey in monkey_equations_solved:
            del equations[monkey]

    # Create the root equation: x1 = x2
    _x1, _, _x2 = root_equation.split(" ")
    root_equation = f"{_x1} = {_x2}"
    # Replace variables by their known equations
    replaced_variable = True
    while replaced_variable:
        replaced_variable = False
        for var, eq in equations.items():
            if var in root_equation:
                root_equation = root_equation.replace(var, f"({eq})")
                replaced_variable = True
    # Replace variables by their known values
    for monkey, value in monkeys.items():
        if monkey in root_equation:
            root_equation = root_equation.replace(monkey, str(value))
    # print(root_equation)

    # Solve equation
    humn = symbols("humn")  # noqa
    left_eq, right_eq = root_equation.split(" = ")
    root_eq = Eq(eval(left_eq), eval(right_eq))  # type: ignore
    return solve(root_eq)[0]  # type: ignore


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        lines = f.read().rstrip().split("\n")

    print(part1(lines))
    print(part2(lines))
    exit()
