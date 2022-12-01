def get_inputs(file):
    with open(file, "r") as f:
        return [_ for _ in f.read().split() if _]


def get_integer_inputs(file):
    return [int(_) for _ in get_inputs(file)]


def depth_deltas(file):
    count = 0
    old_sum = None

    xx = get_integer_inputs(file)
    index = 0
    while index < len(xx) - 2:
        new_sum = 0
        for lookahead in range(2):
            new_sum += xx[index + lookahead]

        if old_sum is not None and new_sum > old_sum:
            count += 1
        old_sum = new_sum
        index += 1
    return count


print(depth_deltas("./inputs/1.txt"))
print("done")
