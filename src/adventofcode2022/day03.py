from collections import Counter
import doctest
from typing import List

from commonlib import chunks

FILE_INPUT = "src/adventofcode2022/day03_input.txt"


def item_priority(item: str) -> int:
    """
    >>> item_priority("a")
    1
    >>> item_priority("z")
    26
    >>> item_priority("A")
    27
    >>> item_priority("Z")
    52
    """
    char_number = ord(item)
    if ord("a") <= char_number <= ord("z"):
        return char_number - ord("a") + 1
    if ord("A") <= char_number <= ord("Z"):
        return char_number - ord("A") + 27
    raise ValueError(f"Item {item} is not a valid letter")


def duplicate_item_in_rucksack(items: str) -> str:
    """
    >>> duplicate_item_in_rucksack('vJrwpWtwJgWrhcsFMMfFFhFp')
    'p'
    """
    if len(items) % 2:
        raise ValueError("items must be a string with even number of characters")
    middle = len(items) // 2
    compartment_1 = items[0:middle]
    compartment_2 = items[middle:]
    c1 = Counter(compartment_1)
    c2 = Counter(compartment_2)
    duplicate_items = c1 & c2
    if len(duplicate_items) != 1:
        raise ValueError("items does not contain exacly 1 duplicate item in each compartment")
    return list(duplicate_items)[0]


def priority_of_duplicate_items_in_rucksack(items_list: List[str]) -> int:
    """
    >>> items_list = [
    ...     'vJrwpWtwJgWrhcsFMMfFFhFp',
    ...     'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
    ...     'PmmdzqPrVvPwwTWBwg',
    ...     'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
    ...     'ttgJtRGJQctTZtZT',
    ...     'CrZsJsPPZsGzwwsLwLmpwMDw',
    ... ]
    >>> priority_of_duplicate_items_in_rucksack(items_list)
    157
    """
    total_priority = 0
    for items in items_list:
        total_priority += item_priority(duplicate_item_in_rucksack(items))
    return total_priority


# Part 2


def common_item_from_several_elfs(items_list: List[str]) -> str:
    """
    >>> items_list = [
    ...     'vJrwpWtwJgWrhcsFMMfFFhFp',
    ...     'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
    ...     'PmmdzqPrVvPwwTWBwg',
    ... ]
    >>> common_item_from_several_elfs(items_list)
    'r'
    """
    common_items = Counter(items_list[0])
    for i, items in enumerate(items_list):
        if i > 0:
            common_items = common_items & Counter(items)
    if len(common_items) != 1:
        raise ValueError("items_list doesn't have exactly 1 item in common between all elfs")
    return list(common_items)[0]


def priority_of_group_badges_in_rucksack(items_list: List[str]) -> int:
    """
    >>> items_list = [
    ...     'vJrwpWtwJgWrhcsFMMfFFhFp',
    ...     'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
    ...     'PmmdzqPrVvPwwTWBwg',
    ...     'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
    ...     'ttgJtRGJQctTZtZT',
    ...     'CrZsJsPPZsGzwwsLwLmpwMDw',
    ... ]
    >>> priority_of_group_badges_in_rucksack(items_list)
    70
    """
    badges_priority = 0
    for group_of_3 in list(chunks(items_list, 3)):
        badges_priority += item_priority(common_item_from_several_elfs(group_of_3))
    return badges_priority


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        items_list = [line.strip() for line in f.readlines()]

    total_priority = priority_of_duplicate_items_in_rucksack(items_list)
    print(f"Total priority of repeated items = {total_priority}")
    badges_priority = priority_of_group_badges_in_rucksack(items_list)
    print(f"Badges priority = {badges_priority}")
