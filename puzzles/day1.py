from typing import List

FILE_INPUT = "puzzles/day1_input.txt"


def read_file_with_blocks(filename: str) -> List[List[int]]:
    out_list: List[List[int]] = []
    with open(filename) as f:
        text = f.read()
        text_blocks = text.split("\n\n")
        for block in text_blocks:
            out_list.append([int(block) for block in block.split("\n")])
    return out_list


if __name__ == "__main__":
    inventories = read_file_with_blocks(FILE_INPUT)
    sum_inventories = [sum(inventory) for inventory in inventories]
    print(f"The elf carrying more calories carrys {max(sum_inventories)} calories.")

    top_3 = sorted(sum_inventories, reverse=True)[0:3]
    print(f"The 3 elfs carrying more calories carry {sum(top_3)} calories.")
