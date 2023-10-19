from __future__ import annotations
import doctest
from typing import Any, List, Optional, Union

FILE_INPUT_EX = "src/adventofcode2022/day13_input_ex.txt"
FILE_INPUT = "src/adventofcode2022/day13_input.txt"
DIVIDER_PACKETS = [
    [[2]],
    [[6]],
]
Packet = Union[int, List[Any]]


class PacketObj:
    """This class was created just so that in Part 2 it's easy to sort lists of packets
    using the compare() function created in Part 1"""

    def __init__(self, value: Packet):
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PacketObj):
            return NotImplemented
        return compare(self.value, other.value) is None

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, PacketObj):
            return NotImplemented
        return compare(self.value, other.value) is True

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, PacketObj):
            return NotImplemented
        return compare(self.value, other.value) is False


def compare(packet1: Packet, packet2: Packet) -> Optional[bool]:
    """
    Returns True if packet1 < packet2
    Return False if packet1 > packet2
    Returns None if packet1 == packet2

    >>> compare([1,1,3,1,1], [1,1,5,1,1])
    True
    >>> compare([[1],[2,3,4]], [[1],4])
    True
    >>> compare([9], [[8,7,6]])
    False
    >>> compare([[4,4],4,4], [[4,4],4,4,4])
    True
    >>> compare([7,7,7,7], [7,7,7])
    False
    >>> compare([], [3])
    True
    >>> compare([[[]]], [[]])
    False
    >>> compare([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9])
    False
    """
    if isinstance(packet1, int) and isinstance(packet2, int):
        return None if packet1 == packet2 else packet1 < packet2
    if isinstance(packet1, int) and isinstance(packet2, list):
        return compare([packet1], packet2)
    if isinstance(packet1, list) and isinstance(packet2, int):
        return compare(packet1, [packet2])
    if isinstance(packet1, list) and isinstance(packet2, list):
        min_len = min(len(packet1), len(packet2))
        for i in range(min_len):
            c = compare(packet1[i], packet2[i])
            if c is not None:
                return c
        return None if len(packet1) == len(packet2) else len(packet1) < len(packet2)
    assert False


if __name__ == "__main__":
    assert not doctest.testmod().failed

    # with open(FILE_INPUT_EX) as f:
    with open(FILE_INPUT) as f:
        blocks = f.read().rstrip().split("\n\n")

    # Part 1
    counter = 0
    packets_txt = [block.split("\n") for block in blocks]
    for i, (packet1_txt, packet2_txt) in enumerate(packets_txt):
        if compare(eval(packet1_txt), eval(packet2_txt)):
            counter += i + 1
    print(counter)

    # Part 2
    packets = [PacketObj(key) for key in DIVIDER_PACKETS]
    for packet1_txt, packet2_txt in packets_txt:
        packets.append(PacketObj(eval(packet1_txt)))
        packets.append(PacketObj(eval(packet2_txt)))

    # Sort the array of PacketObj using the class sorting methods
    sorted_packets = sorted(packets)

    # Calculate decoder key
    packets_values = [packet.value for packet in sorted_packets]
    decoder_key = 1
    for key in DIVIDER_PACKETS:
        decoder_key *= packets_values.index(key) + 1
    print(decoder_key)
    exit()
