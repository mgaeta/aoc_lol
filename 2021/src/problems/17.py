import sys
from typing import Tuple, Optional


def get_inputs(file):
    with open(file, "r") as f:
        return [_ for _ in f.read().split() if _]


MAX_T = 1000


def get_coordinates(file: str) -> Tuple[int, int, int, int]:
    inputs = get_inputs(file)
    a = inputs[2][2:-1].split("..")
    b = inputs[3][2:].split("..")
    return int(a[0]), int(a[1]), int(b[0]), int(b[1])


def blatantly_out_of_range(x: int, y: int, x_end: int, y_start: int) -> bool:
    return (x > x_end) or (y < y_start)


def in_range(x: int, y: int, x_start: int, x_end: int , y_start: int, y_end: int) -> bool:
    return (x_start <= x <= x_end) and (y_start <= y <= y_end)


def test_values(
    v_x: int,
    v_y: int,
    x_start: int,
    x_end: int,
    y_start: int ,
    y_end: int,
) -> Optional[Tuple[int, int]]:
    x = 0
    y = 0

    highest_y = -sys.maxsize
    for t in range(MAX_T):
        x += max((abs(v_x) - t), 0) * int(v_x / v_x)
        y += (v_y - t)

        if y > highest_y:
            highest_y = y

        if blatantly_out_of_range(x, y, x_end, y_start):
            return None

        if in_range(x, y, x_start, x_end, y_start, y_end):
            return v_x, v_y
    return None


def fire(file: str) -> int:
    x_start, x_end, y_start, y_end = get_coordinates(file)
    outputs = set()
    for i in range(1, x_end * 2):
        for j in range(-100, 100):
            result = test_values(i, j, x_start, x_end, y_start, y_end)
            if result:
                outputs.add(result)
    return len(outputs)


# print(fire("./inputs/17tt.txt"))
# print(fire("./inputs/17t.txt"))
print(fire("./inputs/17.txt"))
print("done")
