from collections import defaultdict

from y22.src.utils import io


def main():
    current_day = io.get_day()

    for test in [False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        board, width, length = parse_board(raw_input)

        print(treehouse_2(board, width, length))


def parse_board(raw_input):
    board = []
    width = None
    for i, row in enumerate(raw_input):
        if row == "":
            continue

        width = len(row)
        for j in list(row):
            board.append(int(j))

    return board, width, len(raw_input),


def get_all_neighbors(width, length, row, column):
    output = defaultdict(list)
    for i in range(width):
        if i < column:
            output[0].append((i, row))

    for i in range(width):
        if i > column:
            output[1].append((i, row))

    for j in range(length):
        if j < row:
            output[2].append((column, j))
    for j in range(length):
        if j > row:
            output[3].append((column, j))

    output[0] = list(reversed(output[0]))
    output[2] = list(reversed(output[2]))
    return output


def treehouse_2(board, width, length):
    max_score = 0
    for column in range(width):
        for row in range(length - 1):
            index = row * width + column
            value = board[index]
            neighbors = get_all_neighbors(width, length - 1, row, column)

            if len(neighbors) < 4:
                continue

            product = 1
            for side in neighbors.values():
                for i, (c, r) in enumerate(side):
                    neighbor_value = board[r * width + c]
                    if neighbor_value >= value:
                        break
                product *= i + 1
            max_score = max(max_score, product)
    return max_score


def treehouse_1(board, width, length):
    total = 0
    for column in range(width):
        for row in range(length - 1):
            index = row * width + column
            value = board[index]
            neighbors = get_all_neighbors(width, length - 1, row, column)

            visible = False
            if len(neighbors) < 4:
                total += 1
                continue

            for side in neighbors.values():
                taller_exists = False
                for c, r in side:
                    neighbor_value = board[r * width + c]
                    if neighbor_value >= value:
                        taller_exists = True
                if not taller_exists:
                    visible = True
            if visible:
                total += 1

    return total


if __name__ == "__main__":
    main()
