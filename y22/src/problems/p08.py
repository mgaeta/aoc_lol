from collections import defaultdict

from y22.src.utils import io


def main():
    current_day = io.get_day()

    for test in [True, False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        board, width, length = parse_board(raw_input)

        print(treehouse_2(board, width, length))


def parse_board(raw_input) -> tuple[list[int], int, int]:
    board = []
    width = None
    length = 0
    for row in raw_input:
        if row == "":
            continue

        length += 1
        width = len(row)
        for j in list(row):
            board.append(int(j))

    return board, width, length


def get_index(width: int, row: int, column: int) -> int:
    return row * width + column


def get_all_neighbors(width: int, length: int, row: int, column: int) -> dict[int, [list[int]]]:
    output = defaultdict(list)
    for c in range(width):
        index = get_index(width, row, c)
        if c < column:
            output[0].insert(0, index)
        if c > column:
            output[1].append(index)

    for r in range(length):
        index = get_index(width, r, column)
        if r < row:
            output[2].insert(0, index)
        if r > row:
            output[3].append(index)
    return output


def treehouse_2(board: list[int], width: int, length: int) -> int:
    max_score = 0
    for column in range(width):
        for row in range(length):
            value = board[get_index(width, row, column)]
            neighbors = get_all_neighbors(width, length, row, column)

            if len(neighbors) < 4:
                continue

            product = 1
            for side in neighbors.values():
                for count, index in enumerate(side):
                    neighbor_value = board[index]
                    if neighbor_value >= value:
                        break
                product *= count + 1
            max_score = max(max_score, product)
    return max_score


def treehouse_1(board: list[int], width: int, length: int) -> int:
    total = 0
    for column in range(width):
        for row in range(length):
            value = board[get_index(width, row, column)]
            neighbors = get_all_neighbors(width, length, row, column)

            visible = False
            if len(neighbors) < 4:
                total += 1
                continue

            for side in neighbors.values():
                taller_exists = False
                for index in side:
                    neighbor_value = board[index]
                    if neighbor_value >= value:
                        taller_exists = True
                if not taller_exists:
                    visible = True
            if visible:
                total += 1

    return total


if __name__ == "__main__":
    main()
