def get_inputs(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()


def get_lines(filename):
    inputs = get_inputs(filename)
    return inputs


def get_csv_str(filename):
    inputs = get_inputs(filename)
    return inputs[0].split(",")


def get_csv_int(filename):
    inputs = get_inputs(filename)
    return [int(_) for _ in inputs[0].split(",")]


def split_to_inputs_outputs(line):
    input, output = line.split("|")
    return input.split(), output.split()


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


def get_basin(index, width, height, points_in_order):
    basin_members = set([index])

    neighbors_checked = set()
    neighbors_to_check = get_neighbors(index, width, height)
    while len(neighbors_to_check) > 0:
        next_neighbor = neighbors_to_check.pop()
        neighbors_checked.add(next_neighbor)
        if points_in_order[next_neighbor] != 9:
            neighbors_to_add = set(
                x
                for x in get_neighbors(next_neighbor, width, height)
                if x not in neighbors_checked
            )
            neighbors_to_check = neighbors_to_check.union(neighbors_to_add)
            basin_members.add(next_neighbor)
    return basin_members


def run(filename):
    inputs = get_lines(filename)
    w = len(inputs[0])
    h = len(inputs)
    points_in_order = [int(_) for _ in "".join(inputs)]

    found = set()
    output = []
    for i, point in enumerate(points_in_order):
        neighbor_indexes = get_neighbors(i, w, h)
        neighbor_values = [points_in_order[x] for x in neighbor_indexes]
        if point < min(neighbor_values):
            basin = get_basin(i, w, h, points_in_order)
            if basin.intersection(found):
                continue
            found = found.union(basin)
            output.append(len(basin))

    product = 1
    for a in sorted(output)[-3:]:
        product *= a
    return product


# print(run("./9t.txt"))
print(run("./9.txt"))
