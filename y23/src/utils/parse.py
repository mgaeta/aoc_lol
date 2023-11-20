from y22.src.utils.io import get_inputs_raw


def get_str_inputs(file: str) -> list[str]:
    return [_ for _ in get_inputs_raw(file) if _]


def get_integer_inputs(file: str) -> list[int]:
    return [int(_) for _ in get_str_inputs(file)]


def get_lists_of_lists(file: str) -> list[list[str]]:
    # TODO MARCOS FIRST
    return [_ for _ in get_str_inputs(file)].split()


def parse_board(board: str) -> list[str]:
    return [
        cell
        for row in board.split("\n")
        for cell in row.strip().split()
    ]


def parse_board_int(board: str) -> list[int]:
    return [
        int(cell)
        for row in board.split("\n")
        for cell in row.strip().split()
    ]


