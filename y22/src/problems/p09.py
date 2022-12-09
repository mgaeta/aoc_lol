from collections import defaultdict

from y22.src.utils import io

LENGTH = 10
# LENGTH = 2


def main():
    current_day = io.get_day()

    for test in [True, False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)

        print(rope_snake(raw_input))


def rope_snake(raw_input):
    history = {(0, 0)}
    # head first, (x, y)
    positions = [(0, 0)] * LENGTH
    for row in raw_input:
        if row == "":
            continue

        direction, count_str = row.split(" ")
        count = int(count_str)

        for i in range(count):
            if direction == "L":
                head_position = (positions[0][0] - 1, positions[0][1])
            elif direction == "R":
                head_position = (positions[0][0] + 1, positions[0][1])
            elif direction == "U":
                head_position = (positions[0][0], positions[0][1] + 1)
            elif direction == "D":
                head_position = (positions[0][0], positions[0][1] - 1)
            else:
                raise Exception("bad input")

            positions = handle_move(head_position, positions)
            history.add(positions[len(positions) - 1])

    return len(history)


def handle_move(head_position: tuple[int, int], positions: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if len(positions) == 1:
        return [head_position]

    next_tail = next_tail_position(head_position, positions[1])
    return [head_position, *handle_move(next_tail, positions[1:])]


def next_tail_position(head_position: tuple[int, int], tail_position: tuple[int, int]) -> tuple[int, int]:
    delta_x = head_position[0] - tail_position[0]
    delta_y = head_position[1] - tail_position[1]

    if abs(delta_x) <= 1 and abs(delta_y) <= 1:
        return tail_position

    elif abs(delta_x) >= 1 and abs(delta_y) >= 1:
        if delta_x <= -1 and delta_y <= -1:
            return (tail_position[0] - 1, tail_position[1] - 1)
        elif delta_x >= 1 and delta_y >= 1:
            return (tail_position[0] + 1, tail_position[1] + 1)
        elif delta_x >= 1 and delta_y <= -1:
            return (tail_position[0] + 1, tail_position[1] - 1)
        elif delta_x <= -1 and delta_y >= 1:
            return (tail_position[0] - 1, tail_position[1] + 1)
        else:
            raise Exception("bad")
    elif abs(delta_x) <= 1:
        if delta_y < -1:
            return (tail_position[0], tail_position[1] - 1)
        elif delta_y > 1:
            return (tail_position[0], tail_position[1] + 1)
    elif abs(delta_y) <= 1:
        if delta_x < -1:
            return (tail_position[0] - 1, tail_position[1])
        elif delta_x > 1:
            return (tail_position[0] + 1, tail_position[1])

    raise Exception("bad", delta_x, delta_y)


if __name__ == "__main__":
    main()
