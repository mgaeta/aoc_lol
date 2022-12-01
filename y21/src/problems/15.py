import sys
import heapq


def get_inputs(file):
    with open(file, "r") as f:
        return [_ for _ in f.read().split() if _]


def get_neighbors(index, width, height):
    output = set()

    # left
    if index % width != 0:
        output.add(index - 1)

    # right
    if index % width != (width - 1):
        output.add(index + 1)

    # top
    if index >= width:
        output.add(index - width)

    # bottom
    if index + width < width * height:
        output.add(index + width)

    return output


def calculate_cost(inputs, path):
    return sum(inputs[i] for i in path)


def greedy(board, width, height):
    one_path = []
    cursor = 0
    while cursor < width * height:
        one_path.append(cursor)

        right = None
        bottom = None
        if cursor % width != (width - 1):
            right = cursor + 1

        if cursor + width < width * height:
            bottom = cursor + width

        if not bottom and not right:
            break
        elif not bottom:
            cursor = right
        elif not right:
            cursor = bottom
        else:
            if board[bottom] < board[right]:
                cursor = bottom
            else:
                cursor = right

    return calculate_cost(board, one_path)


EXPAND_DEGREE = 5


def expand_board(board, width, height):
    output = [0] * (width * height * EXPAND_DEGREE * EXPAND_DEGREE)
    for horizontal in range(EXPAND_DEGREE):  # horizontal
        for vertical in range(EXPAND_DEGREE):  # vertical
            for z in range(len(board)):
                output[
                    z % width
                    + (int(z / width) * width * EXPAND_DEGREE)
                    + width * horizontal
                    + (width * EXPAND_DEGREE * height * vertical)
                ] = (board[z] + horizontal + vertical) % 9 or 9
    return output


def print_board(board, width, height):
    for i in range(height):
        print("".join([str(board[i * width + j]) for j in range(width)]))


def dijkstra(file):
    inputs = get_inputs(file)
    width = len(inputs[0])
    height = len(inputs)

    board = expand_board([int(_) for _ in "".join(inputs)], width, height)
    new_width = width * EXPAND_DEGREE
    new_height = height * EXPAND_DEGREE
    END_PIECE = (new_width * new_height - 1)

    print_board(board, new_width, new_height)

    tentative_distance = [sys.maxsize] * (new_width * new_height)
    tentative_distance[0] = 0

    unvisited_set = set()
    unvisited = []
    for i in range(new_width * new_height):
        heapq.heappush(unvisited, (tentative_distance[i], i))
        unvisited_set.add(i)

    while unvisited:
        _, current_node = heapq.heappop(unvisited)
        unvisited_set.remove(current_node)
        unvisited_neighbors = [
            n
            for n in get_neighbors(current_node, new_width, new_height)
            if n in unvisited_set
        ]
        for n in unvisited_neighbors:
            tentative_distance[n] = min(
                tentative_distance[n],
                tentative_distance[current_node] + board[n]
            )

            if tentative_distance[END_PIECE] < sys.maxsize:
                break
    return tentative_distance[END_PIECE]


# print(dijkstra("./inputs/15tt.txt"))
print(dijkstra("./inputs/15t.txt"))
# print(dijkstra("./inputs/15.txt"))
print("done")
