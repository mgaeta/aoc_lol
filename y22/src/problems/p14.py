from y22.src.utils import io


def main():
    current_day = io.get_day()
    for test in [False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)

        parts = parse_inputs(raw_input)
        board = build_board(parts)
        print(simulate(board))


ORIGIN = (500, 0)
# FACTOR = 0
FACTOR = 2


def simulate(board: dict[(int, int), int]) -> int:
    output = 0
    min_x, max_x, max_depth = get_board_dimensions(board)
    while True:
        x, y = step(board, max_depth)
        if y > max_depth + FACTOR:
            return output
        if y == 0:
            return output + 1
        output += 1
        board[(x, y)] = 2


def step(board: dict[(int, int), int], max_depth: int) -> tuple[int, int] | None:
    next_sand = ORIGIN
    while next_sand[1] < max_depth + 1:
        x, y = next_sand
        if (x, y + 1) not in board:
            next_sand = (x, y + 1)
        elif (x - 1, y + 1) not in board:
            next_sand = (x - 1, y + 1)
        elif (x + 1, y + 1) not in board:
            next_sand = (x + 1, y + 1)
        else:
            # blocked
            break
    return next_sand


def build_board(parts_list: list[list[tuple[int, int]]]) -> dict[(int, int), int]:
    output = {}
    for parts in parts_list:
        start_x, start_y = parts[0]

        for end_x, end_y in parts[1:]:
            if start_x == end_x:
                min_y = min(start_y, end_y)
                for i in range(abs(end_y - start_y) + 1):
                    output[(start_x, i + min_y)] = 1
            elif start_y == end_y:
                min_x = min(start_x, end_x)
                for i in range(abs(end_x - start_x) + 1):
                    output[(i + min_x, start_y)] = 1
            else:
                raise Exception("bad")
            start_x, start_y = end_x, end_y

    output[ORIGIN] = 3
    return output


def get_board_dimensions(board: dict[(int, int), int]) -> tuple[int, int, int]:
    min_x = 100_000
    max_x = 0
    max_depth = 0

    for x, y in board.keys():
        min_x = min(x, min_x)
        max_x = max(x, max_x)
        max_depth = max(y, max_depth)

    return min_x, max_x, max_depth


def print_board(board: dict[(int, int), int]) -> None:
    min_x, max_x, max_depth = get_board_dimensions(board)
    for row in range(max_depth + 1):
        print("".join([
            get_representation(board.get((min_x + column, row)))
            for column in range(max_x + 1 - min_x)
        ]))


def get_representation(value: int) -> str:
    return {
        0: ".",
        1: "#",
        2: "O",
        3: "+",
    }.get(value, ".")


def parse_inputs(raw_input) -> list[list[tuple[int, int]]]:
    output = []
    for row in raw_input:
        if row == "":
            continue

        parts_str = [
            tuple(part.split(","))
            for part in row.split(" -> ")
        ]
        output.append([(int(a), int(b)) for a, b in parts_str])
    return output


if __name__ == "__main__":
    main()
