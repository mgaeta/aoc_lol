from collections import defaultdict

from y22.src.utils import io


def main():
    current_day = io.get_day()

    for test in [True, False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)

        board = rope_snake(raw_input)
        print_board(board)


def rope_snake1(raw_input):
    total = 0
    cycle = 1
    register = {"X": 1}

    for row in raw_input:
        if row == "":
            continue

        if row == "noop":
            if (cycle + 20) % 40 == 0:
                print(cycle, register["X"], cycle * register["X"], "c")
                total += cycle * register["X"]
            cycle += 1
        else:
            instruction, value_str = row.split(" ")

            if (cycle + 20) % 40 == 0:
                print(cycle, register["X"], cycle * register["X"], "b")
                total += cycle * register["X"]
            cycle += 1

            # print(int(value_str))
            register["X"] = register["X"] + int(value_str)
            if (cycle + 20) % 40 == 0:
                register["X"] -= 1
                print(cycle, register["X"], cycle * register["X"], "c")
                total += cycle * register["X"]
            cycle += 1

    return total


def print_board(board: list[bool]) -> None:
    for row in range(6):
        output = ""
        for column in range(40):
            if board[column + row * 40]:
                output += "#"
            else:
                output += "."
        print(output)
    print("\n")


def rope_snake(raw_input):
    board = defaultdict(bool)
    cycle = 1
    register = {"X": 1}

    for row in raw_input:
        if row == "":
            continue

        if row == "noop":
            sprite_locations = [register["X"] + 1, register["X"], register["X"] - 1]
            if cycle % 40 in sprite_locations:
                board[cycle] = True
            cycle += 1
        else:
            instruction, value_str = row.split(" ")
            sprite_locations = [register["X"] + 1, register["X"], register["X"] - 1]
            if cycle % 40 in sprite_locations:
                board[cycle] = True
            cycle += 1

            register["X"] = register["X"] + int(value_str)
            sprite_locations = [register["X"] + 1, register["X"], register["X"] - 1]
            if cycle % 40 in sprite_locations:
                board[cycle] = True
            cycle += 1

    return board


if __name__ == "__main__":
    main()
