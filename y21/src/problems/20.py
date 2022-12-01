import math
import sys
from collections import defaultdict
from typing import List, Mapping, Tuple

STEPS = 50
ALGORITHM_LENGTH = 2 ** 3 ** 2


def get_inputs(file):
    with open(file, "r") as f:
        return [_ for _ in f.read().split("\n\n") if _]


def get_conway():
    output = ""
    for i in range(ALGORITHM_LENGTH):
        s = (("0" * 9) + str(bin(i))[2:])[-9:]
        count = sum(int(_) for _ in s)

        if (s[4] == "1" and (count - 1 in [2, 3])) or (s[4] == "0" and count == 3):
            output += "#"
        else:
            output += "."
    return output


def print_board(
    board: Mapping[Tuple[int, int], bool],
) -> None:
    min_x = sys.maxsize
    min_y = sys.maxsize
    max_x = -sys.maxsize
    max_y = -sys.maxsize
    for x, y in board.keys():
        if x > max_x:
            max_x = x
        if x < min_x:
            min_x = x
        if y > max_y:
            max_y = y
        if y < min_y:
            min_y = y

    height = abs(max_y - min_y) + 1
    width = abs(max_x - min_x) + 1
    print("=" * width)
    count = 0
    for y in range(height):
        line = ""
        inverse = ""
        for x in range(width):
            if board[(x + min_x, y + min_y)]:
                line += "#"
                inverse += "."
                count += 1
            else:
                line += "."
                inverse += "#"
        print(f"{line} {inverse}")
    print(f"= {count} {'=' * (width - 4 - int(math.log10(count)))}")


def get_neighbors(coordinates: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = coordinates
    return [
        (x + i - 1, y + j - 1,)
        for j in range(3)
        for i in range(3)
    ]


def two_step(
    board: Mapping[Tuple[int, int], bool],
    algorithm: List[bool],
) -> Mapping[Tuple[int, int], bool]:
    inverted_board = step(board, algorithm, is_input_inverted=False)
    return step(inverted_board, algorithm, is_input_inverted=algorithm[0])


def get_neighbors_key(neighbors_values: List[bool]) -> int:
    return int("".join(str(int(_)) for _ in neighbors_values), 2)


def get_sparse_board(
    board: List[bool],
    width: int,
    height: int,
) -> Mapping[Tuple[int, int], bool]:
    infinite_board = defaultdict(bool)
    for x in range(width):
        for y in range(height):
            infinite_board[(x, y)] = board[y * width + x]
    return infinite_board


def step(
    board: Mapping[Tuple[int, int], bool],
    algorithm: List[bool],
    is_input_inverted: bool
) -> Mapping[Tuple[int, int], bool]:
    should_invert = algorithm[0]
    new_board = defaultdict(bool)

    seen = set(board.keys())
    queue = list(board.keys())
    while len(queue):
        next_coordinates = queue.pop()
        neighbors_coordinates = get_neighbors(next_coordinates)

        key = get_neighbors_key([board[v] ^ is_input_inverted for v in neighbors_coordinates])
        new_board[next_coordinates] = algorithm[key] ^ should_invert ^ is_input_inverted

        if key != ((ALGORITHM_LENGTH - 1) if is_input_inverted else 0):
            for n in neighbors_coordinates:
                if n not in seen:
                    queue.append(n)
                    seen.add(n)

    return new_board


def game_of_life(file: str):
    inputs = get_inputs(file)

    algorithm = [(_ == "#") for _ in inputs[0]]
    image = inputs[1].split("\n")[:-1]

    board = get_sparse_board(
        [(_ == "#") for _ in "".join(image)],
        len(image[0]),
        len(image),
    )

    for i in range(int(STEPS / 2)):
        board = two_step(board, algorithm)

    return sum(board.values())

# print(game_of_life("./inputs/20ttt.txt"))
# print(game_of_life("./inputs/20tt.txt"))
print(game_of_life("./inputs/20t.txt"))
# print(game_of_life("./inputs/20.txt"))
