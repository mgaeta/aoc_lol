import math
from typing import Any, Optional, Tuple


def get_inputs(file):
    with open(file, "r") as f:
        return [_ for _ in f.read().split() if _]


def parse_line_recursive(line: str):
    if len(line) == 1:
        return int(line[0])

    stack = 0
    for i, value in enumerate(line):
        if value == "," and stack == 1:
            return (
                parse_line_recursive(line[1:i]),
                parse_line_recursive(line[i + 1:-1])
            )

        if value == "[":
            stack += 1
        if value == "]":
            stack -= 1
    return None


def add_value_to_rightmost_tuple(t, value):
    if not value:
        return t
    if isinstance(t, int):
        return t + value
    a, b = t
    return a, add_value_to_rightmost_tuple(b, value)


def add_value_to_leftmost_tuple(t, value):
    if not value:
        return t
    if isinstance(t, int):
        return t + value
    a, b = t
    return add_value_to_leftmost_tuple(a, value), b


def explode_left_most_n_tuple(t, n) -> Tuple[Optional[Any], Optional[Any], Any]:
    if isinstance(t, int):
        return None, None, t

    a, b = t
    if n == 0:
        return a, b, 0

    left_a, right_a, new_value_a = explode_left_most_n_tuple(a, n - 1)
    if new_value_a != a:
        return (
            left_a,
            None,
            (new_value_a, add_value_to_leftmost_tuple(b, right_a))
        )
    left_b, right_b, new_value_b = explode_left_most_n_tuple(b, n - 1)
    if new_value_b != b:
        return (
            None,
            right_b,
            (add_value_to_rightmost_tuple(new_value_a, left_b), new_value_b)
        )
    return None, None, (new_value_a, new_value_b)


def split_left_most_tuple(t) -> Tuple[Any, bool]:
    if isinstance(t, int):
        if t < 10:
            return t, False
        return (math.floor(t / 2), (math.ceil(t / 2))), True

    a, b = t
    left, was_split = split_left_most_tuple(a)
    if was_split:
        return (left, b), True

    right, was_split = split_left_most_tuple(b)
    if was_split:
        return (a, right), True

    return (a, b), False


def reduce(t):
    old_value = t
    while True:
        _, _, new_value = explode_left_most_n_tuple(old_value, 4)
        if new_value == old_value:
            new_value, _ = split_left_most_tuple(new_value)
            if new_value == old_value:
                return old_value

        old_value = new_value


def add(a, b):
    return reduce((a, b))


def get_magnitude(t) -> int:
    if isinstance(t, int):
        return t
    a, b = t
    return 3 * get_magnitude(a) + (2 * get_magnitude(b))


def homework_1(file: str):
    inputs = get_inputs(file)

    result = parse_line_recursive(inputs[0])
    for xx in inputs[1:]:
        result = add(result, parse_line_recursive(xx))
    return get_magnitude(result)


def homework(file: str):
    inputs = get_inputs(file)

    return max(
        get_magnitude(
            add(
                parse_line_recursive(inputs[i]),
                parse_line_recursive(inputs[j])
            )
        )
        for i in range(len(inputs))
        for j in range(len(inputs))
        if i != j
    )

# print(homework("./inputs/18t5.txt"))
# print(homework("./inputs/18t.txt"))
print(homework("./inputs/18.txt"))
print("done")
