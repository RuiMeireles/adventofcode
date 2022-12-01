from typing import List


def read_file_with_blocks_of_int(filename: str) -> List[List[int]]:
    """Reads a file that has blocks of integers.
    Blocks are separated by an empty line.
    Otherwise expects all lines to have integers.
    """
    out_list: List[List[int]] = []
    with open(filename) as f:
        text = f.read()
        text_blocks = text.split("\n\n")
        for text_block in text_blocks:
            out_list.append([int(line) for line in text_block.split("\n")])
    return out_list
