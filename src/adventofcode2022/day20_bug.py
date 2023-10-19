import doctest
from typing import List

FILE_INPUT = "src/adventofcode2022/day20_input.txt"


def mix(array: List[int], value: int) -> List[int]:
    """
    >> mix([1, 2, -3, 3, -2, 0, 4], 1)
    [2, 1, -3, 3, -2, 0, 4]
    >> mix([2, 1, -3, 3, -2, 0, 4], 2)
    [1, -3, 2, 3, -2, 0, 4]
    >> mix([1, -3, 2, 3, -2, 0, 4], -3)
    [1, 2, 3, -2, -3, 0, 4]
    >> mix([1, 2, 3, -2, -3, 0, 4], 3)
    [1, 2, -2, -3, 0, 3, 4]
    >> mix([1, 2, -2, -3, 0, 3, 4], -2)
    [1, 2, -3, 0, 3, 4, -2]
    >> mix([1, 2, -3, 0, 3, 4, -2], 0)
    [1, 2, -3, 0, 3, 4, -2]
    >> mix([1, 2, -3, 0, 3, 4, -2], 4)
    [1, 2, -3, 4, 0, 3, -2]
    >> mix([7, 2, -3, 3, -2, 0, 4], 7)
    [7, -3, 3, -2, 0, 4, 2]
    >> mix([14, 2, -3, 3, -2, 0, 4], 14)
    [14, 3, -2, 0, 4, 2, -3]
    >> mix([15, 2, -3, 3, -2, 0, 4], 15)
    [3, 15, -2, 0, 4, 2, -3]
    >>> mix([2, 8, -3, 3, -2, 0, 4], 8)
    [-3, 3, 8, -2, 0, 4, 2]
    >>> mix([4, 0, -2, 3, -3, 8, 2], 8)
    [0, -2, 3, -3, 2, 4, 8]
    >>> mix([2, -8, -3, 3, -2, 0, 4], -8)
    [-8, 4, 2, -3, 3, -2, 0]
    """
    i = array.index(value)
    d_left = i
    d_right = len(array) - 1 - i
    distance = d_right if value > 0 else d_left

    if value == 0:
        return array
    if value < 0:
        # Reverse array so the logic to the right also works to the left
        array = array[::-1]
        i = len(array) - i - 1

    # A: Rotate array so that value has index 0
    array_right = array[i::] + array[0:i]
    spins = abs(value) // len(array)
    steps = abs(value) % len(array)
    k = 0 if distance > steps else 1
    # B: Spin: Keep value fixed at index 0, rotate the rest to the left
    # TODO: work on spins to make last example work
    rots = spins % len(array)
    rots = rots % (len(array) - 1)
    array_right_spin = [value] + array_right[1 + rots :] + array_right[1 : 1 + rots]
    # C: Step: Shift value steps to the right
    array_right_step = array_right_spin[1 : steps + 1] + [value] + array_right_spin[steps + 1 :]
    # D: Rotate the array back
    # array_right_final = array_right_step[-i - k + rots : :] + array_right_step[0 : -i - k + rots]
    array_right_final = array_right_step[-i - k : :] + array_right_step[0 : -i - k]
    return array_right_final if value > 0 else array_right_final[::-1]


def mix_array(array: List[int]) -> List[int]:
    """
    Runs mix() for every elements of the array, in the order they originally appear

    >>> mix_array([1, 2, -3, 3, -2, 0, 4])
    [1, 2, -3, 4, 0, 3, -2]
    """
    for value in array:
        array = mix(array, value)
    return array


def sum_grove_coordinates(array: List[int]) -> int:
    """
    >>> sum_grove_coordinates([1, 2, -3, 4, 0, 3, -2])
    3
    """
    i = array.index(0)
    result = 0
    for n in [1000, 2000, 3000]:
        j_high = i + n
        j_low = j_high % len(array)
        result += array[j_low]
    return result


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        lines = f.read().rstrip().split("\n")
        array = [int(line) for line in lines]

    print("Part 1:")
    mixed_array = mix_array(array)
    print(sum_grove_coordinates(mixed_array))
    # -540
    # -15463
    exit()
