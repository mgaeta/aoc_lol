def get_inputs(file):
    with open(file, "r") as f:
        return [_ for _ in f.read().split("\n") if _]


def get_integer_inputs(file):
    return [int(_) for _ in get_inputs(file)]


def get_str_inputs(file):
    return [str(_) for _ in get_inputs(file)]


def crab_army(file):
    ii = [int(_) for _ in get_inputs(file)[0].split(",")]
    return min([
        sum([int((abs(i - p)) * (abs(i - p) + 1) / 2) for i in ii])
        for p in range(min(ii), max(ii))
    ])


def print_board(board, width, height, name="result"):
    print(f"- {name} ---------------")
    for j in range(height):
        line = ""
        for i in range(width):
            d = board[j * height + i]
            if d > 9:
                d = "x"
            line += str(d)
        print(line)
    print("---------------")


def create_board(inputs):
    return [int(_) for _ in inputs]


def get_neighbors(index, width, height):
    w = int(index % width)
    h = int(index / width)

    output = set()
    if w > 0:
        output.add(index - 1)
    if h > 0 and w > 0:
        output.add(index - width - 1)
    if h > 0:
        output.add(index - width)
    if h > 0 and w < width - 1:
        output.add(index - width + 1)
    if w < width - 1:
        output.add(index + 1)
    if h < height - 1 and w > 0:
        output.add(index + width - 1)
    if h < height - 1:
        output.add(index + width)
    if h < height - 1 and w < width - 1 and (w * h < width * height):
        output.add(index + width + 1)

    return output


def step(board, width, height):
    has_flashed = set()

    q = []
    for i in range(len(board)):
        board[i] += 1
        q.append(i)

    while len(q):
        n = q.pop()
        if board[n] > 9 and not n in has_flashed:
            has_flashed.add(n)
            for nn in get_neighbors(n, width, height):
                board[nn] += 1
                if board[nn] > 9 and not nn in has_flashed:
                    q.append(nn)

    for i in has_flashed:
        board[i] = 0

    return board, len(has_flashed)


N = 1000


def octopodes(file):
    inputs = [_ for _ in get_inputs(file)]
    w = len(inputs[0])
    h = len(inputs)

    output = 0
    board = create_board("".join(inputs))
    for i in range(N):
        board, flashes = step(board, w, h)
        if flashes == w * h:
            return i


# print(octopodes("./inputs/11tt.txt"))
print(octopodes("./inputs/11t.txt"))
# print(octopodes("./inputs/11.txt"))
print("done")
