from __future__ import annotations
from collections import defaultdict
from typing import Mapping, MutableMapping, Set, Tuple

Point = Tuple[int, int, int]
Region = Tuple[Point, Point]
Tree = MutableMapping[Region, "Tree"]
Instruction = Tuple[bool, Region]

INF = 100000
LIMIT = 50


def get_inputs(file):
    with open(file, "r") as f:
        return [_ for _ in f.read().split("\n") if _]


def get_instruction(line: str, limit: int | None = None) -> Instruction:
    on_off, coordinates = line.split(" ")
    x_range, y_range, z_range = [
        (int(a[0]), int(a[1]))
        for a in [
            _[2:].split("..")
            for _ in coordinates.split(",")
        ]
    ]

    region = (
        (
            min(x_range),
            min(y_range),
            min(z_range),
        ),
        (
            max(x_range),
            max(y_range),
            max(z_range),
        )
    )

    if limit:
        limit_region = ((-limit, -limit, -limit), (limit, limit, limit))
        region = region_intersect(region, limit_region)

    return on_off == "on", region


def recurse_count(board: Tree, limit: int | None = None) -> int:
    output = 0
    for region, children in board.items():
        if children:
            output += recurse_count(children, limit)
        else:
            # Leaf
            output += calculate_volume(region, limit)
    return output


def limit_value(value, limit: int | None = None) -> int:
    limit = limit or INF
    return min(limit, max(-limit, value))


def calculate_volume(region: Region | None, limit: int | None = None) -> int:
    if not region:
        return 0

    return (
        (abs(limit_value(region[0][0], limit) - limit_value(region[1][0], limit)) + 1)
        * (abs(limit_value(region[0][1], limit) - limit_value(region[1][1], limit)) + 1)
        * (abs(limit_value(region[0][2], limit) - limit_value(region[1][2], limit)) + 1)
    )


def region_intersect(region_a: Region, region_b: Region, depth: int = 0) -> Region | None:
    regions = [region_a, region_b]

    if any(
        (regions[j][1][i] < regions[int(not j)][0][i])
        for i in range(3)
        for j in range(2)
    ):
        return None

    p = [
        sorted(
            regions[i][j][k]
            for i in range(2)
            for j in range(2)
        )
        for k in range(3)
    ]

    return (
        (p[0][1], p[1][1], p[2][1]),
        (p[0][2], p[1][2], p[2][2]),
    )


def step(board: MutableMapping[Point, bool], instruction: Instruction):
    on_off, region = instruction
    if not (region and calculate_volume(region)):
        return board

    for i in range(abs(region[0][0] - region[1][0]) + 1):
        for j in range(abs(region[0][1] - region[1][1]) + 1):
            for k in range(abs(region[0][2] - region[1][2]) + 1):
                x = region[0][0] + i
                y = region[0][1] + j
                z = region[0][2] + k

                board[(x, y, z)] = on_off
    return board


def count_board(board: Mapping[Point, bool]) -> int:
    return sum([int(i) for i in board.values()])


def set_up_1(file: str, limit: int | None = None) -> int:
    inputs = get_inputs(file)
    instructions = [get_instruction(input, limit) for input in inputs]

    board = defaultdict(bool)
    for instruction in instructions:
        board = step(board, instruction)

    return count_board(board)


def divide_all_space_by_region(region: Region) -> Set[Region]:
    xx = [-INF, region[0][0], region[1][0], INF]
    yy = [-INF, region[0][1], region[1][1], INF]
    zz = [-INF, region[0][2], region[1][2], INF]

    output = {
        (
            (
                xx[i] + (i - 1),
                yy[j] + (j - 1),
                zz[k] + (k - 1),
            ),
            (
                xx[i + 1] + (i - 1),
                yy[j + 1] + (j - 1),
                zz[k + 1] + (k - 1),
            ),
        )
        for i in range(3)
        for j in range(3)
        for k in range(3)
        if not ((i == 1) and (j == 1) and (k == 1))
    }
    return output


def handle_old_region(region_b: Region, divided_space: Set[Region], depth: int) -> Set[Region]:
    intersections = set()
    for region_c in divided_space:
        intersection = region_intersect(region_c, region_b, depth)
        volume = calculate_volume(intersection)

        if not volume:
            continue

        intersections.add(intersection)
    return intersections


def recursive_step(board: Tree, instruction: Instruction, depth: int) -> Tree:

    on_off, region_a = instruction
    if not (region_a and calculate_volume(region_a)):
        return board

    divided_space = divide_all_space_by_region(region_a)
    new_board = {}
    for region_b, children in board.items():
        initial_intersection = region_intersect(region_a, region_b, depth)
        if not initial_intersection:
            # If they do not collide, put B back.divided_space
            new_board[region_b] = children
            continue

        if initial_intersection == region_b:
            # If B is in A, delete B
            continue

        if initial_intersection == region_a and not children and on_off:
            # If A is in B leaf, board should remain the same!
            return board

        if not children:
            sub_board = {
                intersection: {}
                for intersection in handle_old_region(region_b, divided_space, depth)
            }
        else:
            sub_board = recursive_step(children, instruction, depth + 1)

        if sub_board:
            new_board[region_b] = sub_board

    if depth == 0 and on_off:
        new_board[region_a] = {}
    return new_board


def set_up(file: str) -> int:
    instructions = [get_instruction(input) for input in get_inputs(file)]
    tree = {}
    board = defaultdict(bool)
    for instruction in instructions:
        tree = recursive_step(tree, instruction, 0)

    return recurse_count(tree)

print(set_up("./inputs/22.txt"))
