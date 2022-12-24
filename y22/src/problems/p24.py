from collections import defaultdict

from y22.src.utils import io

DIRS = {
    ">": (1, 0),
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
}


def invert_storm(storm: str) -> str:
    return {
        ">": "<",
        "^": "v",
        "v": "^",
        "<": ">",
    }[storm]


def invert_board(
        board: dict[tuple[int, int], set[str]],
        bounds: tuple[int, int],
) -> dict[tuple[int, int], set[str]]:
    width, height = bounds
    next_board = {}
    for row in range(height):
        for col in range(width):
            next_board[(width - col - 1, height - row - 1)] = {
                invert_storm(v)
                for v in board[(col, row)]
            }
    return next_board


def main():
    current_day = io.get_day()
    for test in [True, False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        board, bounds = parse_input(raw_input)

        output = []
        for i in range(3):
            t, board = simulate(board, bounds, verbose=False)
            output.append(t)
            board = invert_board(board, bounds)

        print(output)
        print(sum(output))


def get_next_positions(
        map_cache: list[dict[tuple[int, int], set[str]]],
        bounds: tuple[int, int],
        position: tuple[int, int],
        t: int,
) -> list[tuple[int, int]]:
    width, height = bounds
    x, y = position
    options = [position]
    for dx, dy in DIRS.values():
        next_x = x + dx
        next_y = y + dy
        # check bounds
        if (0 <= next_x < width) and (0 <= next_y < height):
            options.append((next_x, next_y))

    # check map
    next_board = get_map_at_t(map_cache, bounds, t + 1)
    return [option for option in options if option not in next_board]


def get_heuristic(position: tuple[int, int], t: int):
    x, y = position
    return x + y - t


def simulate(
        board: dict[tuple[int, int], set[str]],
        bounds: tuple[int, int],
        verbose: bool = False
) -> tuple[int, dict[tuple[int, int], set[str]]]:
    # Load starting board into cache
    map_cache = [board]

    seen = set()

    # This maps scores to a list of states. The states are tuples of
    # positions and timestamps.
    queues_by_priority: dict[
        int,
        list[tuple[tuple[int, int], int]]
    ] = defaultdict(list)
    queues_by_priority[-1].append(((0, -1), 0))
    while True:
        max_key = max([
            key
            for key, value in queues_by_priority.items()
            if len(value)
        ])
        if verbose:
            print("max_key", max_key)
        position, t = None, None
        while len(queues_by_priority[max_key]):
            position, t = queues_by_priority[max_key].pop()
            if (position, t) not in seen:
                break

        if verbose:
            print_board(get_map_at_t(map_cache, bounds, t), bounds, position, t)

        if position == (bounds[0] - 1, bounds[1] - 1):
            # Move off the board
            return t + 1, get_map_at_t(map_cache, bounds, t + 1)

        seen.add((position, t))

        for p in get_next_positions(map_cache, bounds, position, t):
            heuristic = get_heuristic(p, t)
            if (p, t + 1) not in seen:
                queues_by_priority[heuristic].append((p, t + 1))


def get_map_at_t(
        map_cache: list[dict[tuple[int, int], set[str]]],
        bounds: tuple[int, int],
        t: int
) -> dict[tuple[int, int], set[str]]:
    if t == len(map_cache):
        next_board = step(map_cache[-1], bounds)
        map_cache.append(next_board)
    return map_cache[t]


def print_board(
        board: dict[tuple[int, int], set[str]],
        bounds: tuple[int, int],
        position: tuple[int, int],
        t: int
) -> None:
    width, height = bounds
    print(f"Minute {t}:")
    print(f'#.{"#" * width}')
    for row in range(height):
        line = ["#"]
        for col in range(width):
            if (col, row) == position:
                line.append("E")
                continue
            v = board[(col, row)]
            if len(v) < 1:
                line.append(".")
            elif len(v) >= 10:
                line.append("*")
            elif len(v) == 1:
                line.append(list(v)[0])
            else:
                line.append(str(len(v)))
        line.append("#")
        print("".join(line))
    print(f'{"#" * width}.#')
    print()


def step(
        board: dict[tuple[int, int], set[str]],
        bounds: tuple[int, int]
) -> dict[tuple[int, int], set[str]]:
    width, height = bounds
    next_board = defaultdict(set)
    for (x, y), vs in board.items():
        for v in vs:
            if v in DIRS:
                next_x, next_y = DIRS[v]
                next_board[((x + next_x) % width, (y + next_y) % height)].add(v)
    return next_board


def parse_input(raw_data):
    output = defaultdict(set)
    y = 0
    max_x = -1
    for row in raw_data[1:-2]:
        if row == "":
            continue
        for x, storm in enumerate(list(row[1:-1])):
            max_x = max(max_x, x)
            output[(x, y)].add(storm)
        y += 1

    return output, (max_x + 1, y)


if __name__ == "__main__":
    main()
