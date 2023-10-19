import doctest
from typing import List

FILE_INPUT = "src/adventofcode2022/day25_input.txt"
BASE5_DIGITS = "01234"
SNAFU_DIGITS = "012=-"
CONVERT_TO_SNAFU = dict(zip(BASE5_DIGITS, SNAFU_DIGITS))
CONVERT_FROM_SNAFU = dict(zip(SNAFU_DIGITS, BASE5_DIGITS))


def to_base_5(n: int) -> str:
    """
    >>> to_base_5(6)
    '11'
    """
    s = ""
    while n != 0:
        s = str(n % 5) + s
        n //= 5
    return s


def to_snafu(n: int) -> str:
    """
    >>> to_snafu(4)
    '1-'
    >>> to_snafu(6)
    '11'
    >>> to_snafu(15)
    '1=0'
    >>> to_snafu(2022)
    '1=11-2'
    >>> to_snafu(97)
    '1--2'
    >>> to_snafu(98)
    '1-0='
    >>> to_snafu(99)
    '1-0-'
    """
    s = ""
    carry = 0
    while n != 0 or carry == 1:
        carry2 = False
        d = n % 5 + carry
        if d == 5:
            # The examples 98 and 99 fall here
            d = d % 5
            carry2 = True
        s_ = CONVERT_TO_SNAFU[str(d)]
        carry = 1 if (carry2 or s_ in "=-") else 0
        s = s_ + s
        n //= 5
    return s


def from_snafu(s: str) -> int:
    """
    >>> from_snafu('1-')
    4
    >>> from_snafu('11')
    6
    >>> from_snafu('1=0')
    15
    >>> from_snafu('1=11-2')
    2022
    >>> from_snafu('1--2')
    97
    >>> from_snafu('1-0=')
    98
    >>> from_snafu('1-0-')
    99
    """
    n = 0
    power = 0
    carry = 0
    for c in s[::-1]:
        d = int(CONVERT_FROM_SNAFU[c]) - carry
        carry = 1 if c in ["=", "-"] else 0
        n += d * 5**power
        power += 1
    return n


def part1(snafu_numbers: List[str]) -> int:
    """
    >>> snafu_numbers = [
    ...     "1=-0-2",
    ...     "12111",
    ...     "2=0=",
    ...     "21",
    ...     "2=01",
    ...     "111",
    ...     "20012",
    ...     "112",
    ...     "1=-1=",
    ...     "1-12",
    ...     "12",
    ...     "1=",
    ...     "122",
    ... ]
    >>> part1(snafu_numbers)
    4890
    """
    numbers = [from_snafu(n) for n in snafu_numbers]
    return sum(numbers)


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        snafu_numbers = f.read().rstrip().split("\n")

    result = part1(snafu_numbers)
    print(to_snafu(result))
    print("2=12-100--1012-0=012")
    exit()
