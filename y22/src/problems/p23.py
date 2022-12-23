from y22.src.utils import io
from collections import defaultdict

LARGE_NUMBER = 1_000_000
COUNT = 10
DIRS = [
    [(-1, -1), (0, -1), (1, -1)],
    [(-1, 1), (0, 1), (1, 1)],
    [(-1, -1), (-1, 0), (-1, 1)],
    [(1, -1), (1, 0), (1, 1)],
]


def main():
    current_day = io.get_day()
    for test in [False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        board = parse_input(raw_input)
        # print(simulate(board, count=COUNT))
        print(simulate(board))


def simulate(board: set[tuple[int, int]]) -> int:
    i = 0
    while i < LARGE_NUMBER:
        # print_board(board, i)
        next_board = step(board, i)
        if compare_boards(next_board, board):
            return i + 1
        board = next_board
        i += 1
    return -1


def compare_boards(a: set[tuple[int, int]], b: set[tuple[int, int]]) -> bool:
    return len(a) == len(b) and len(a.difference(b)) == 0


def simulate1(board: set[tuple[int, int]], count: int) -> int:
    for i in range(count):
        board = step(board, i)

    min_x, min_y, max_x, max_y = get_bounds(board)
    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(board)


def get_bounds(board) -> tuple[int, int, int, int]:
    max_x = -1
    max_y = -1
    min_x = LARGE_NUMBER
    min_y = LARGE_NUMBER
    for x, y in board:
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        min_x = min(min_x, x)
        min_y = min(min_y, y)

    return min_x, min_y, max_x, max_y


def step(board: set[tuple[int, int]], i: int) -> set[tuple[int, int]]:
    next_board = set()

    # Populate the reverse_proposals table
    reverse_proposals = defaultdict(set)
    for (x, y) in board:
        proposed_cardinal_direction = propose_direction(board, x, y, i)
        if proposed_cardinal_direction is not None:
            d_x, d_y = DIRS[proposed_cardinal_direction][1]
            reverse_proposals[(x + d_x, y + d_y)].add((x, y))

    # Move all unopposed proposals
    to_move = set(board)
    for proposal, origins in reverse_proposals.items():
        if len(origins) == 1:
            origin = origins.pop()
            to_move.remove(origin)
            next_board.add(proposal)

    # Everyone else stays put.
    for leftover in to_move:
        next_board.add(leftover)

    return next_board


def print_board(board: set[tuple[int, int]], i: int) -> None:
    min_x, min_y, max_x, max_y = get_bounds(board)
    print(f"--- {i} ----------------")
    for row in range(min_y, max_y + 1):
        line = []
        for col in range(min_x, max_x + 1):
            c = "#" if (col, row) in board else "."
            line.append(c)
        print("".join(line))
    print(f"-----------------------")
    print()


def propose_direction(board: set[tuple[int, int]], x: int, y: int, d: int) -> int | None:
    results = []
    for i in range(4):
        next_d = (d + i) % 4
        proposals = DIRS[next_d]
        found = False
        for p_x, p_y in proposals:
            if (x + p_x, y + p_y) in board:
                found = True
        if not found:
            results.append(next_d)

    if len(results) in [0, 4]:
        return None
    return results[0]


def parse_input(raw_data):
    board = set()
    y = 0
    for row in raw_data:
        if row == "":
            continue
        for x, v in enumerate(list(row)):
            if v == "#":
                board.add((x, y))
        y += 1
    return board


if __name__ == "__main__":
    main()
