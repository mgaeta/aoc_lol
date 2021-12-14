def get_inputs(file):
    with open(file, "r") as f:
        return [_ for _ in f.read().split("\n") if _]


def get_integer_inputs(file):
    return [int(_) for _ in get_inputs(file)]


def get_str_inputs(file):
    return [str(_) for _ in get_inputs(file)]


def split_input(input_line):
    lol = input_line.split(" ")
    if len(lol) >= 2:
        return lol[0], int(lol[1])
    return None


def depth_deltas(file):
    xx = get_str_inputs(file)
    aim = 0
    forward = 0
    depth = 0
    for line in xx:
        lol = split_input(line)
        if not lol:
            continue
        command, length = lol
        if command == "forward":
            forward += length
            depth += aim * length
        elif command == "up":
            aim -= length
        elif command == "down":
            aim += length

    return forward * depth


print(depth_deltas("./inputs/2.txt"))
print("done")
