import doctest
from timeit import default_timer as timer
from typing import List, overload, TypeVar
from typing_extensions import SupportsIndex

_T = TypeVar("_T")


class CircularList(list[_T]):
    @overload
    def __getitem__(self, __i: SupportsIndex) -> _T:
        ...

    @overload
    def __getitem__(self, __s: slice) -> list[_T]:
        ...

    def __getitem__(self, __i: int) -> _T:  # type: ignore
        return super().__getitem__(__i % len(self))


FILE_INPUT = "puzzles/day20_input.txt"
DECRYPTION_KEY = 811589153
NUM_ROUNDS_PART_2 = 10


def rotate(c: CircularList[int], n: int) -> CircularList[int]:
    """
    >>> c = CircularList([1, 2, 3])
    >>> rotate(c, -1)
    [2, 3, 1]
    >>> rotate(c, 0)
    [1, 2, 3]
    >>> rotate(c, 1)
    [3, 1, 2]
    >>> rotate(c, 1000)
    [3, 1, 2]
    """
    return CircularList([c[i - n] for i in range(0, len(c))])


def shift(c: CircularList[int], value: int, n: int) -> CircularList[int]:
    """
    >>> shift(CircularList([1, 2, 3, 4, 5]), 2, 3)
    [1, 3, 4, 5, 2]
    >>> shift(CircularList([0, 2, 1, 3, 4, 5, 6]), 2, -3)
    [6, 0, 1, 3, 4, 2, 5]
    >>> shift(CircularList([1, 2, -3, 3, -2, 0, 4]), 1, 1)
    [2, 1, -3, 3, -2, 0, 4]
    >>> shift(CircularList([2, 1, -3, 3, -2, 0, 4]), 2, 2)
    [1, -3, 2, 3, -2, 0, 4]
    >>> shift(CircularList([1, -3, 2, 3, -2, 0, 4]), -3, -3)
    [4, 1, 2, 3, -2, -3, 0]
    >>> shift(CircularList([1, 2, 3, -2, -3, 0, 4]), 3, 3)
    [1, 2, -2, -3, 0, 3, 4]
    >>> shift(CircularList([1, 2, -2, -3, 0, 3, 4]), -2, -2)
    [-2, 1, 2, -3, 0, 3, 4]
    >>> shift(CircularList([1, 2, -3, 0, 3, 4, -2]), 0, 0)
    [1, 2, -3, 0, 3, 4, -2]
    >>> shift(CircularList([1, 2, -3, 0, 3, 4, -2]), 4, 4)
    [2, -3, 4, 0, 3, -2, 1]
    >>> shift(CircularList([7, 2, -3, 3, -2, 0, 4]), 7, 7)
    [7, -3, 3, -2, 0, 4, 2]
    >>> shift(CircularList([14, 2, -3, 3, -2, 0, 4]), 14, 14)
    [14, 3, -2, 0, 4, 2, -3]
    >>> shift(CircularList([15, 2, -3, 3, -2, 0, 4]), 15, 15)
    [3, 15, -2, 0, 4, 2, -3]
    >>> shift(CircularList([2, 8, -3, 3, -2, 0, 4]), 8, 8)
    [-3, 3, 8, -2, 0, 4, 2]
    >>> shift(CircularList([4, 0, -2, 3, -3, 8, 2]), 8, 8)
    [0, -2, 3, -3, 2, 4, 8]
    >>> shift(CircularList([2, -8, -3, 3, -2, 0, 4]), -8, -8)
    [-8, 4, 2, -3, 3, -2, 0]
    """
    # a: starting point, with index i_a and value v_a
    # b: point to the right of a, after shifting
    v_a = value
    i_a = c.index(v_a)
    i_a_2 = (i_a + n) % len(c)
    # Create a circular list 1 item shorter than c (it doesn't have v)
    c_aux = CircularList([0] * (len(c) - 1))
    for i in range(len(c_aux)):
        c_aux[i] = c[i_a + 1 + i]
    # Determine point that will be on the right of a after shifting
    v_b = c_aux[n]
    i_b = c_aux.index(v_b)
    # Create the shifted list
    c_shifted = CircularList([0] * (len(c)))
    c_shifted[i_a_2] = v_a
    for i in range(len(c_aux)):
        c_shifted[(i_a_2 + 1 + i) % len(c)] = c_aux[i_b + i]
    return c_shifted


def mix_array(array: List[int], num_rounds: int = 1) -> List[int]:
    """
    Runs mix() for every elements of the array, in the order they originally appear.
    This handles lists with duplicate values by doing the rotations of the indexes!!!
    (This was one of the main bugs in this problem...)

    >>> mix_array([1, 2, -3, 3, -2, 0, 4])
    [-2, 1, 2, -3, 4, 0, 3]
    >>> mix_array([v * DECRYPTION_KEY for v in [1, 2, -3, 3, -2, 0, 4]], num_rounds=1)
    [0, -2434767459, 3246356612, -1623178306, 2434767459, 1623178306, 811589153]
    >>> mix_array([v * DECRYPTION_KEY for v in [1, 2, -3, 3, -2, 0, 4]], num_rounds=10)
    [811589153, 0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459]
    """
    # Circular list of the indexes - this is what will be shifted around
    c: CircularList[int] = CircularList(list(range(len(array))))

    # Perform several rounds of mixing
    for _ in range(num_rounds):
        # Shift each indexes by its value
        for index, value in enumerate(array):
            c = shift(c, index, value)
            # mixed_array = [array[c[i]]) for i in range(len(array))]

    # Build the resulting mixed array
    mixed_array = [array[c[i]] for i in range(len(array))]
    return mixed_array


def sum_grove_coordinates(array: List[int]) -> int:
    """
    >>> sum_grove_coordinates([1, 2, -3, 4, 0, 3, -2])
    3
    >>> sum_grove_coordinates([811589153, 0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459])
    1623178306
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

    for part in [1, 2]:
        # Part 1: 21.433755 seconds
        # Part 2: 200.920255 seconds
        print(f"Part {part}:")
        start = timer()
        if part == 2:
            array = [v * DECRYPTION_KEY for v in array]
        mixed_array = mix_array(array, num_rounds=1 if part == 1 else NUM_ROUNDS_PART_2)
        print(sum_grove_coordinates(mixed_array))
        print(f"{timer() - start:4f} seconds")
        print()

    exit()
