from y22.src.utils import io


SIMULATION_ROCKS = 1_000_000_000_000
# (x, y)
PIECES = [
    # 0: -
    {
        "id": 0,
        "height": 1,
        "shape": [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
        ]},
    # 1: +
    {
        "id": 1,
        "height": 3,
        "shape": [
            (1, 0),
            (0, 1),
            (1, 1),
            (2, 1),
            (1, 2),
        ]},
    # 2: J
    {
        "id": 2,
        "height": 3,
        "shape": [
            (0, 0),
            (1, 0),
            (2, 0),
            (2, 1),
            (2, 2),
        ]},
    # 3: I
    {
        "id": 3,
        "height": 4,
        "shape": [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
        ]},
    # 4: o
    {
        "id": 4,
        "height": 2,
        "shape": [
            (0, 0),
            (1, 0),
            (0, 1),
            (1, 1),
        ]}
]


def main():
    current_day = io.get_day()
    for test in [False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        data = parse_input(raw_input)

        # print(simulate1({}, data))
        print(simulate(data))


def simulate(data: list[str]) -> int:
    height_before_repeat = 0
    height_per_repeat = 0
    piece_count_before_repeat = 0
    piece_count_per_repeat = 0

    highest_point = -1
    board: dict[tuple[int, int], bool] = {}
    piece_count = 0
    piece = insert_piece(highest_point, piece_count)
    landed = False
    for i in range(2):
        gas_count = 0
        while gas_count < len(data):
            if landed:
                piece = insert_piece(highest_point, piece_count)
                piece_count += 1

            next_gas = data[gas_count % len(data)]
            new_location, landed = get_next_location(board, piece, next_gas)
            piece["location"] = new_location
            if landed:
                for x, y in piece["location"]:
                    board[(x, y)] = True

                highest_point = max(highest_point, max(y for x, y in piece["location"]))

            print_board(board, highest_point, piece["location"])
            gas_count += 1

            print_board(
                board,
                highest_point,
                piece["location"],
                start=highest_point - 2,
                end=highest_point + 5,
            )
        if i == 0:
            height_before_repeat = highest_point
            piece_count_before_repeat = piece_count
        if i == 1:
            height_per_repeat = highest_point - height_before_repeat
            piece_count_per_repeat = piece_count - piece_count_before_repeat
    repeats = SIMULATION_ROCKS // piece_count_per_repeat - 1
    height_after_repeats = height_before_repeat + repeats * height_per_repeat
    pieces_remaining = SIMULATION_ROCKS % piece_count_per_repeat
    the_rest = simulate1(board, data, highest_point, pieces_remaining) - highest_point

    return height_after_repeats + the_rest


def simulate1(
        board: dict[tuple[int, int], bool],
        data: list[str],
        highest_point: int = -1,
        until: int = 2022
) -> int:
    landed = False
    gas_count = 0
    piece = insert_piece(highest_point, 0)
    piece_count = 1
    while piece_count <= until:
        if landed:
            piece = insert_piece(highest_point, piece_count)
            piece_count += 1

        next_gas = data[gas_count % len(data)]
        new_location, landed = get_next_location(board, piece, next_gas)
        piece["location"] = new_location
        if landed:
            for x, y in piece["location"]:
                board[(x, y)] = True

            highest_point = max(highest_point, max(y for x, y in piece["location"]))

        print_board(board, highest_point, piece["location"])
        gas_count += 1
    return highest_point + 1


def print_piece(piece_number: int) -> None:
    points = set(PIECES[piece_number % len(PIECES)]["shape"])
    piece = []
    for row in range(4):
        out = "".join(
            "#" if (column, row) in points else "."
            for column in range(4)
            if (column, row) in points
        )
        if out != "....":
            piece.append(out)
    print("\n".join(piece))


def insert_piece(highest_point: int, piece_number: int) -> dict[str, any]:
    piece = PIECES[piece_number % len(PIECES)]
    return {
        "id": piece["id"],
        "height": piece["height"],
        "location": [
            (x + 2, y + highest_point + 4)
            for x, y in piece["shape"]
        ]
    }


def print_board(
        board: dict[tuple[int, int], bool],
        highest_point: int,
        new_location: list[tuple[int, int]],
        start: int = 0,
        end: int | None = None,
        verbose: bool = False,
) -> None:
    if not verbose:
        return
    output = []
    highest_point = max(highest_point, max(y for x, y in new_location))
    for row in range(start, end or highest_point + 1):
        out = ""
        for column in range(7):
            if (column, row) in new_location:
                out += "@"
            elif board.get((column, row), False):
                out += "#"
            else:
                out += "."
        output.append(out)
    output.reverse()
    for i, row in enumerate(output):
        print(f"|{row}|")
    if start == 0:
        print("+-------+")
    print()


def get_next_location(
        board: dict[tuple[int, int], bool],
        piece: dict[str, any],
        gas_str: str,
        verbose: bool = False,
) -> tuple[list[tuple[int, int]], bool]:
    # Part 1: jet
    translate_x = 1 if gas_str == ">" else -1
    old_location = piece["location"]
    proposed_location_x = [
        (x + translate_x, y)
        for (x, y) in piece["location"]
    ]
    collision_x = any(
        (x < 0 or x >= 7 or board.get((x, y), False))
        for x, y in proposed_location_x
    )
    if collision_x:
        proposed_location_x = old_location

    # Part 2: gravity
    proposed_location_y = [
        (x, y - 1)
        for (x, y) in proposed_location_x
    ]

    landed = any(
        (y == -1 or board.get((x, y), False))
        for x, y in proposed_location_y
    )
    return proposed_location_x if landed else proposed_location_y, landed


def parse_input(raw_data):
    output = []
    for row in raw_data:
        if row == "":
            continue
        output += (list(row))
    return output


if __name__ == "__main__":
    main()
