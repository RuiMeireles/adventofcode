from __future__ import annotations
from dataclasses import dataclass, field
import doctest
from textwrap import dedent
from typing import Dict, List, Optional

FILE_INPUT = "src/adventofcode2022/day07_input.txt"
MAX_DIR_SIZE = 100_000
DISK_SIZE = 70_000_000
UPDATE_SIZE = 30_000_000
TEST_INPUT = dedent(
    """\
    $ cd /
    $ ls
    dir a
    14848514 b.txt
    8504156 c.dat
    dir d
    $ cd a
    $ ls
    dir e
    29116 f
    2557 g
    62596 h.lst
    $ cd e
    $ ls
    584 i
    $ cd ..
    $ cd ..
    $ cd d
    $ ls
    4060174 j
    8033020 d.log
    5626152 d.ext
    7214296 k
    """.rstrip()
)


@dataclass
class Node:
    """Represents a directory or a file.
    Files must never have children.
    """

    name: str
    is_dir: bool
    size: int = 0
    children: Dict[str, Node] = field(repr=False, default_factory=dict)
    parent: Optional[Node] = field(repr=False, default=None)

    @property
    def full_path(self) -> str:
        """The full_path property is not required for anything, it was just added for completeness"""
        if self.parent:
            spfp = self.parent.full_path
            parent_full_path = spfp[:-1] if spfp.endswith("/") else spfp
            return parent_full_path + "/" + self.name
        else:
            return self.name

    def disk_usage(self) -> int:
        """Recursive method that calculates on the fly and returns the disk usage of each directory.
        This was created as an alternative to update_directory_sizes(), which actually sets the size of each directory.
        However, the remaining functions and tests haven't been adapted to use this method.
        """
        if not self.is_dir:
            return self.size
        return sum(child.disk_usage() for child in self.children.values())


def parse_input(input: str) -> List[List[str]]:
    """
    >>> parse_input(TEST_INPUT)
    [['cd /'], ['ls', 'dir a', '14848514 b.txt', '8504156 c.dat', 'dir d'], ['cd a'], ['ls', 'dir e', '29116 f', '2557 g', '62596 h.lst'], ['cd e'], ['ls', '584 i'], ['cd ..'], ['cd ..'], ['cd d'], ['ls', '4060174 j', '8033020 d.log', '5626152 d.ext', '7214296 k']]
    """
    parsed_commands: List[List[str]] = []
    input = "\n" + input
    commands = input.split("\n$ ")[1:]  # Remove the first empty element
    for command in commands:
        parsed_commands.append(command.split("\n"))
    return parsed_commands


def build_tree(commands: List[List[str]]) -> Node:
    """Builds a tree of Directories and files

    >>> build_tree(parse_input(TEST_INPUT))
    Node(name='/', is_dir=True, size=0)
    """
    tree = Node("/", is_dir=True, parent=None)
    cwd = tree
    for command in commands:
        command_words = command[0].split(" ")

        if command_words[0] == "cd":
            dir_name = command_words[1]
            if dir_name == "/":
                cwd = tree
            elif dir_name == "..":
                assert cwd.parent is not None
                cwd = cwd.parent
            else:
                cwd = cwd.children[dir_name]

        if command_words[0] == "ls":
            for content in command[1:]:
                word1, name = content.split(" ")
                if word1 == "dir":
                    cwd.children[name] = Node(name, is_dir=True, parent=cwd)
                else:
                    cwd.children[name] = Node(name, is_dir=False, parent=cwd, size=int(word1))
    return tree


def update_directory_sizes(node: Node) -> int:
    """Recursive function that calculates and updates the size of each directory

    >>> tree = build_tree(parse_input(TEST_INPUT))
    >>> update_directory_sizes(tree)
    48381165
    """
    size = 0
    for content in node.children.values():
        if content.is_dir:
            size += update_directory_sizes(content)
        else:
            size += content.size
    node.size = size
    return size


def directories_with_given_size(node: Node, size: int, size_below: bool) -> List[Node]:
    """Recursive function that returns the directories above or below a certain size

    >>> tree = build_tree(parse_input(TEST_INPUT))
    >>> _ = update_directory_sizes(tree)
    >>> directories_with_given_size(tree, 100_000, size_below=True)
    [Node(name='a', is_dir=True, size=94853), Node(name='e', is_dir=True, size=584)]
    >>> directories_with_given_size(tree, 8_381_165, size_below=False)
    [Node(name='/', is_dir=True, size=48381165), Node(name='d', is_dir=True, size=24933642)]
    """
    directories: List[Node] = []
    if size_below and node.size < size:
        directories.append(node)
    if not size_below and node.size > size:
        directories.append(node)
    for content in node.children.values():
        if content.is_dir:
            directories += directories_with_given_size(content, size, size_below)
    return directories


def sum_node_sizes(nodes: List[Node]) -> int:
    """
    >>> sum_node_sizes([Node(name='a', is_dir=True, size=94853), Node(name='e', is_dir=True, size=584)])
    95437
    """
    return sum([n.size for n in nodes])


def smallest_sized_node(nodes: List[Node]) -> Node:
    """
    >>> smallest_sized_node([Node(name='/', is_dir=True, size=48381165), Node(name='d', is_dir=True, size=24933642)])
    Node(name='d', is_dir=True, size=24933642)
    """
    return sorted(nodes, key=lambda x: x.size)[0]


if __name__ == "__main__":
    assert not doctest.testmod().failed

    with open(FILE_INPUT) as f:
        input = f.read()

    commands = parse_input(input)
    tree = build_tree(commands)
    update_directory_sizes(tree)

    # Part 1
    directories = directories_with_given_size(tree, MAX_DIR_SIZE, size_below=True)
    print(sum_node_sizes(directories))

    # Part 2
    used_space = tree.size
    free_space = DISK_SIZE - used_space
    free_space_required = UPDATE_SIZE - free_space
    directories = directories_with_given_size(tree, free_space_required, size_below=False)
    smallest_sized_directory = smallest_sized_node(directories)
    print(smallest_sized_directory.size)
    print(smallest_sized_directory.disk_usage())
    print(smallest_sized_directory.full_path)
    exit()
