from y22.src.utils import io
import re
from collections import defaultdict


def main():
    current_day = io.get_day()

    for test in [True, False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        print(crane2(raw_input))


def parse_board(raw_input):
    count = 0
    for row in raw_input:
        count += 1
        if row == "":
            break

    data = defaultdict(list)

    for i, row in enumerate(reversed(raw_input[0:count-2])):
        if row == "":
            continue

        j = 1
        column = 0
        while j < len(row):
            next_char = row[j]
            if next_char != " ":
                data[column].append(next_char)

            j += 4
            column += 1

    return {
        "count": count,
        "data": data
    }


def crane2(raw_input):
    board_data = parse_board(raw_input)
    board = board_data["data"]

    for row in raw_input[board_data["count"]:]:
        if row == "":
            continue

        x, y, z = re.findall(r'move (\d+) from (\d+) to (\d+)', row)[0]
        count = int(x)
        from_column = int(y) - 1
        to_column = int(z) - 1

        stack = []
        for j in range(count):
            stack.append(board[from_column].pop())

        for item in reversed(stack):
            board[to_column].append(item)

    return "".join([stack.pop() for stack in board.values()])


def crane1(raw_input):
    board_data = parse_board(raw_input)
    board = board_data["data"]

    for row in raw_input[board_data["count"]:]:
        if row == "":
            continue

        x, y, z = re.findall(r'move (\d+) from (\d+) to (\d+)', row)[0]
        count = int(x)
        from_column = int(y) - 1
        to_column = int(z) - 1

        for j in range(count):
            temp = board[from_column].pop()
            board[to_column].append(temp)

    return "".join([stack.pop() for stack in board.values()])


if __name__ == "__main__":
    main()
