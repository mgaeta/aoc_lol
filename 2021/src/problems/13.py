def get_inputs(file):
    with open(file, "r") as f:
        return [_ for _ in f.read().split("\n\n") if _]


def get_integer_inputs(file):
    return [int(_) for _ in get_inputs(file)]


def get_str_inputs(file):
    return [str(_) for _ in get_inputs(file)]


def print_page(board, w, h):
    print("\n".join([
        "".join([
            ("#" if board[j + i * w] else ".")
            for j in range(w)
        ])
        for i in range(h)
    ]), "\n")


def create_board(tuples, w, h):
    output = [False] * (w * h)
    for x, y in tuples:
        index = x + y * w
        output[index] = True
    return output


def transform_board_to_tuples(board, w, h, axis, value):
    tuples = []
    for index, z in enumerate(board):
        if z:
            x = index % w
            y = int(index / w)

            if axis == "x":
                if x > value:
                    x = w - x - 1
            elif axis == "y":
                if y > value:
                    y = h - y - 1

            tuples.append((x, y))

    return tuples


def apply_fold(board, w, h, axis, value):
    if axis == "x":
        new_w = int(w / 2)
        new_h = h
    else:
        new_w = w
        new_h = int(h / 2)

    tuples = transform_board_to_tuples(board, w, h, axis, value)
    new_board = create_board(tuples, new_w, new_h)
    return new_board, new_w, new_h


def count_dots(board):
    return sum(i for i in board)


def get_dots_and_folds(file):
    inputs = [_ for _ in get_inputs(file)]
    dots = [
        (int(x), int(y))
        for x, y in [_.split(",") for _ in inputs[0].split()]
    ]
    folds = [(_[11], int(_[13:])) for _ in inputs[1].split("\n")]
    return dots, folds


def origami(file):
    tuples, folds = get_dots_and_folds(file)

    w = max([x for x, y in tuples]) + 1
    h = max([y for x, y in tuples]) + 1

    board = create_board(tuples, w, h)

    for axis, value in folds:
        board, w, h = apply_fold(board, w, h, axis, value)
        print_page(board, w, h)
    return count_dots(board)


# print(origami("./inputs/13tt.txt"))
# print(origami("./inputs/13t.txt"))
print(origami("./inputs/13.txt"))
print("done")
