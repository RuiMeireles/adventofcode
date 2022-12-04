import doctest
from typing import List

FILE_INPUT = "puzzles/day04_input.txt"


def get_range(range_txt: str) -> List[int]:
    """
    >>> get_range('2-4')
    [2, 3, 4]
    """
    low, high = range_txt.split("-")
    return [i for i in range(int(low), int(high) + 1)]


def count_completely_overlapped_pairs_in_range(ranges: List[str]) -> int:
    """
    >>> items_list = [
    ...     '2-4,6-8',
    ...     '2-3,4-5',
    ...     '5-7,7-9',
    ...     '2-8,3-7',
    ...     '6-6,4-6',
    ...     '2-6,4-8',
    ... ]
    >>> count_completely_overlapped_pairs_in_range(items_list)
    2
    """
    num_completely_overlapped_pairs = 0
    for range_pair in ranges:
        range1_txt, range2_txt = range_pair.split(",")
        range1 = set(get_range(range1_txt))
        range2 = set(get_range(range2_txt))
        if range1.issubset(range2) or range1.issuperset(range2):
            num_completely_overlapped_pairs += 1
    return num_completely_overlapped_pairs


def count_overlapping_pairs_in_range(ranges: List[str]) -> int:
    """
    >>> items_list = [
    ...     '2-4,6-8',
    ...     '2-3,4-5',
    ...     '5-7,7-9',
    ...     '2-8,3-7',
    ...     '6-6,4-6',
    ...     '2-6,4-8',
    ... ]
    >>> count_overlapping_pairs_in_range(items_list)
    4
    """
    num_overlapping_pairs = 0
    for range_pair in ranges:
        range1_txt, range2_txt = range_pair.split(",")
        range1 = set(get_range(range1_txt))
        range2 = set(get_range(range2_txt))
        if range1 & range2:
            num_overlapping_pairs += 1
    return num_overlapping_pairs


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        ranges = [line.strip() for line in f.readlines()]

    num_completely_overlapped_pairs = count_completely_overlapped_pairs_in_range(ranges)
    print(f"Number of completely overlapped pairs: {num_completely_overlapped_pairs}")
    num_overlapping_pairs = count_overlapping_pairs_in_range(ranges)
    print(f"Number of overlapping pairs: {num_overlapping_pairs}")
