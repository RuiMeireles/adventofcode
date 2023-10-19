from commonlib import read_file_with_blocks_of_int

FILE_INPUT = "src/adventofcode2022/day01_input.txt"


if __name__ == "__main__":
    inventories = read_file_with_blocks_of_int(FILE_INPUT)

    sum_inventories = [sum(inventory) for inventory in inventories]
    print(f"The elf carrying more calories carrys {max(sum_inventories)} calories.")

    top_3 = sorted(sum_inventories, reverse=True)[0:3]
    print(f"The 3 elfs carrying more calories carry {sum(top_3)} calories.")
