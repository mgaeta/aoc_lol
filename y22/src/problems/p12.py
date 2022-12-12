from y22.src.utils import io
from queue import PriorityQueue

MAX_HEIGHT = 100_000
CHEAT_FACTOR = 2  # lower is better, but too low and the program doesn't halt.


def main():
    current_day = io.get_day()

    for test in [True, False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)

        board, width, height, start_x, start_y, end_x, end_y = parse_board(raw_input)
        print(get_shortest_path(board, width, height, start_x, start_y, end_x, end_y))


def get_shortest_path(
        board: list[int],
        width: int,
        height: int,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
) -> int:
    memo = {}
    q = PriorityQueue()

    q.put((0, (board, start_x, start_y)))
    while True:
        old_v, item = q.get()
        board, x, y = item
        if (x, y) in memo:
            if old_v >= memo[(x, y)]:
                continue
        if x == end_x and y == end_y:
            print_board(board, width, height)
            return calculate_depth(board)
        results = step(board, width, height, x, y)
        for next_board, next_x, next_y in results:
            v = heuristic_value(board, next_x, next_y, end_x, end_y)
            q.put((v, (next_board, next_x, next_y)))
        memo[(x, y)] = min(memo.get((x, y), MAX_HEIGHT), old_v)


def step(
        board: list[int],
        width: int,
        height: int,
        x: int,
        y: int,
) -> list[tuple[list[int], int, int]] | None:
    output = []
    neighbors = determine_options(board, width, height, x, y)
    for neighbor_x, neighbor_y in neighbors:
        # prevent backtracking
        next_board = board.copy()
        next_board[x + y * width] = MAX_HEIGHT
        output.append((next_board, neighbor_x, neighbor_y))
    return output


A_TO_I = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9,
    "k": 10,
    "l": 11,
    "m": 12,
    "n": 13,
    "o": 14,
    "p": 15,
    "q": 16,
    "r": 17,
    "s": 18,
    "t": 19,
    "u": 20,
    "v": 21,
    "w": 22,
    "x": 23,
    "y": 24,
    "z": 25,
    "X": MAX_HEIGHT
}


def i_to_a(i: int) -> str:
    if i == MAX_HEIGHT:
        return "."
    return "abcdefghijklmnopqrstuvwxyz"[i]


def print_board(board: list[int], width: int, height: int) -> None:
    for i in range(height):
        print("".join(i_to_a(board[i * width + j]) for j in range(width)))
    print("")


def calculate_depth(board: list[int]) -> int:
    depth = 0
    for i in board:
        if i == MAX_HEIGHT:
            depth += 1
    return depth


def heuristic_value(board: list[int], x: int, y: int, end_x, end_y) -> int:
    return abs(end_x - x) + abs(end_y - y) + calculate_depth(board)


def determine_options(board: list[int], width: int, height: int, x: int, y: int) -> list[tuple[int, int]]:
    current_height = board[x + width * y]
    candidates = []
    if x > 0:
        candidates.append((x - 1, y))
    if x < width - 1:
        candidates.append((x + 1, y))
    if y > 0:
        candidates.append((x, y - 1))
    if y < height - 1:
        candidates.append((x, y + 1))

    neighbors = []
    for neighbor_x, neighbor_y in candidates:
        neighbor_value = board[neighbor_x + width * neighbor_y]
        if (
                (neighbor_value != MAX_HEIGHT) and
                (current_height - CHEAT_FACTOR <= neighbor_value <= current_height + 1)
        ):
            neighbors.append((neighbor_value, (neighbor_x, neighbor_y)))
    neighbors.sort(key=lambda d: d[0], reverse=True)
    return [t for score, t in neighbors]


def parse_board(raw_input) -> tuple[list[int], int, int, int, int, int, int]:
    board = []
    width, height, start_x, start_y, end_x, end_y = 0, 0, 0, 0, 0, 0

    for row in raw_input:
        if row == "":
            continue
        for x, value in enumerate(list(row)):
            width = len(row)
            if value == "S":
                start_x = x
                start_y = height
                next = 0
            elif value == "E":
                end_x = x
                end_y = height
                next = 25
            else:
                next = A_TO_I[value]
            board.append(next)
        height += 1
    return board, width, height, start_x, start_y, end_x, end_y


if __name__ == "__main__":
    main()
