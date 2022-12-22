from collections import defaultdict

from y22.src.utils import io

LARGE_INT = 1_000_000
DIRS = [
    # x, y
    (1, 0),  # >
    (0, 1),  # v
    (-1, 0),  # <
    (0, -1),  # ^
]


def dir_to_str(d: int) -> str:
    return ">v<^"[d % 4]


def main():
    current_day = io.get_day()
    for test in [True]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        board, bounds, instructions = parse_input(raw_input)
        print(
            simulate(
                board,
                bounds,
                instructions,
                grid_size=4,
                region_offsets={
                    "a": (2, 0),
                    "b": (0, 1),
                    "c": (1, 1),
                    "d": (2, 1),
                    "e": (2, 2),
                    "f": (3, 2),
                },
                rules={
                    #       >         v           <           ^
                    "a": [("f", 2), ("d", 1), ("c", 1), ("b", 1)],
                    "b": [("c", 0), ("e", 3), ("f", 3), ("a", 1)],
                    "c": [("d", 0), ("e", 0), ("b", 2), ("a", 0)],
                    "d": [("f", 1), ("e", 1), ("c", 2), ("a", 3)],
                    "e": [("f", 0), ("b", 3), ("c", 3), ("d", 3)],
                    "f": [("a", 2), ("b", 0), ("e", 2), ("d", 0)],
                }
            )
        )

    for test in [False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        board, bounds, instructions = parse_input(raw_input)

        print(
            simulate(
                board,
                bounds,
                instructions,
                grid_size=50,
                region_offsets={
                    "a": (1, 0),
                    "b": (2, 0),
                    "c": (1, 1),
                    "d": (1, 2),
                    "e": (0, 2),
                    "f": (0, 3),
                },
                rules={
                    #       >         v           <           ^
                    "a": [("b", 0), ("c", 1), ("e", 0), ("f", 0)],
                    "b": [("d", 2), ("c", 2), ("a", 2), ("f", 3)],
                    "c": [("b", 3), ("d", 1), ("e", 1), ("a", 3)],
                    "d": [("b", 2), ("f", 2), ("e", 2), ("c", 3)],
                    "e": [("d", 0), ("f", 1), ("a", 0), ("c", 0)],
                    "f": [("d", 3), ("b", 1), ("a", 1), ("e", 3)],
                }
            )
        )


def get_current_region(x: int, y: int, grid_size: int, region_offsets: dict[str, tuple[int, int]]) -> str:
    for key, (start_x, start_y) in region_offsets.items():
        if (
                (start_x * grid_size < x <= (start_x + 1) * grid_size) and
                (start_y * grid_size < y <= (start_y + 1) * grid_size)
        ):
            return key
    raise Exception("bad", x, y)


def determine_next_position(
        x: int,
        y: int,
        d: int,
        grid_size: int,
        region_offsets: dict[str, tuple[int, int]],
        rules: dict[str, list[tuple[str, int]]],
        verbose: bool = False
) -> (int, int, int):
    current_region = get_current_region(x, y, grid_size, region_offsets)
    relative_x = ((x - 1) % grid_size) + 1
    relative_y = ((y - 1) % grid_size) + 1

    next_region, next_direction = rules[current_region][d]
    absolute_offset_x, absolute_offset_y = region_offsets[next_region]

    if (d - next_direction) % 4 == 0:
        if d in [0, 2]:  # left, right
            next_x = grid_size - relative_x + 1
            next_y = relative_y
        else:  # up, down
            next_x = relative_x
            next_y = grid_size - relative_y + 1
    elif (d - next_direction) % 4 == 2:
        if d in [0, 2]:  # left, right
            next_x = relative_x
            next_y = grid_size - relative_y + 1
        else:  # up, down
            next_x = grid_size - relative_x + 1
            next_y = relative_x + 1
    elif (d - next_direction) % 4 == 1:
        if d in [0, 2]:  # left, right
            next_x = relative_y
            next_y = relative_x
        else:  # up, down
            next_x = relative_y
            next_y = grid_size - relative_x + 1
    else:
        if d in [0, 2]:  # left, right
            next_x = grid_size - relative_y + 1
            next_y = grid_size - relative_y + 1
        else:  # up, down
            next_x = relative_y
            next_y = relative_x

    if verbose:
        print("moving from", current_region, next_region)
        print("relative", relative_x, relative_y)
        print(d, next_direction, (d - next_direction) % 4)
        print(absolute_offset_x * grid_size, absolute_offset_y * grid_size)
        print("next", next_x, next_y)
    out_x = absolute_offset_x * grid_size + next_x
    out_y = absolute_offset_y * grid_size + next_y
    return out_x, out_y, next_direction


def simulate(
        board: dict[tuple[int, int], str],
        bounds: tuple[any, any, any, any],
        instructions: list[tuple[int | None, str | None]],
        grid_size: int,
        region_offsets: dict[str, tuple[int, int]],
        rules: dict[str, list[tuple[str, int]]],
        verbose: bool = False
) -> int:
    x_mins, x_maxes, y_mins, y_maxes = bounds
    x = x_mins[1]
    y = y_mins[x]
    d = 0

    for (distance, direction) in instructions:
        if direction:
            if direction == "L":
                d -= 1
            else:
                d += 1
            continue

        for i in range(distance):
            dx, dy = DIRS[d % 4]
            next_x = x + dx
            next_y = y + dy
            next_d = d

            if (
                    next_x < x_mins[y] or
                    next_x > x_maxes[y] or
                    next_y < y_mins[x] or
                    next_y > y_maxes[x]
            ):
                next_x, next_y, next_d = determine_next_position(
                    x, y, d % 4,
                    grid_size,
                    region_offsets,
                    rules
                )

            next_space = board.get((next_x, next_y))
            if next_space == "#":
                break

            if verbose:
                print(f"({x}, {y}) {dir_to_str(d)} ({next_x}, {next_y})[{dir_to_str(next_d)}]")
            x = next_x
            y = next_y
            d = next_d

    if verbose:
        print(x, y, d)
    return 1000 * y + 4 * x + (d % 4)


def simulate1(board, bounds, instructions) -> int:
    x_mins, x_maxes, y_mins, y_maxes = bounds
    x = x_mins[1]
    y = y_mins[x]
    d = 0

    for (distance, direction) in instructions:
        if direction:
            if direction == "L":
                d -= 1
            else:
                d += 1
            print("rotating", d)
            continue

        for i in range(distance):
            dx, dy = DIRS[d % 4]
            next_x = x + dx
            next_y = y + dy

            if next_x < x_mins[y]:
                next_x = x_maxes[y]
            elif next_x > x_maxes[y]:
                next_x = x_mins[y]
            elif next_y < y_mins[x]:
                next_y = y_maxes[x]
            elif next_y > y_maxes[x]:
                next_y = y_mins[x]

            next_space = board.get((next_x, next_y))
            print("x", x, "y", y, "next_x", next_x, "next_y", next_y, next_space)
            if next_space == "#":
                print("wall")
                break
            x = next_x
            y = next_y

    print(x, y, d)
    return 1000 * y + 4 * x + (d % 4)


def parse_input(raw_data):
    board = {}
    x_mins = defaultdict(lambda: LARGE_INT)
    x_maxes = defaultdict(lambda: -1)
    y_mins = defaultdict(lambda: LARGE_INT)
    y_maxes = defaultdict(lambda: -1)
    instructions = []

    mode = 0
    y = 1
    for row in raw_data:
        if row == "":
            if mode == 0:
                mode = 1
            continue
        if mode == 0:
            for _x, value in enumerate(list(row)):
                x = _x + 1
                if value in [".", "#"]:
                    board[(x, y)] = value
                    x_mins[y] = min(x_mins[y], x)
                    y_mins[x] = min(y_mins[x], y)
                    x_maxes[y] = max(x_maxes[y], x)
                    y_maxes[x] = max(y_maxes[x], y)
        else:
            buffer = 0
            for i in list(row):
                if i in ["L", "R"]:
                    instructions.append((buffer, None))
                    instructions.append((None, i))
                    buffer = 0
                else:
                    buffer *= 10
                    buffer += int(i)
            instructions.append((buffer, None))
        y += 1

    bounds = (x_mins, x_maxes, y_mins, y_maxes)
    return board, bounds, instructions


if __name__ == "__main__":
    main()
