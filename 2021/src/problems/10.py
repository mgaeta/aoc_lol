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


def process_line(line):
    stack = []
    for i in line:
        if i in "{[(<":
            stack.append(i)
            continue
        last = stack.pop()
        if not (
            (last == "{" and i == "}")
            or (last == "<" and i == ">")
            or (last == "[" and i == "]")
            or (last == "(" and i == ")")

        ):
            return i, None
    return None, stack


def calculate_score(stack):
    if not stack:
        return None

    SCORES = {
        "(": 1,
        "[": 2,
        "{": 3,
        "<": 4,
    }

    stack.reverse()

    output = 0
    for value in stack:
        output *= 5
        output += SCORES[value]

    return output


def run_1(filename):
    SCORES = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    x = [process_line(line) for line in get_lines(filename)]
    return sum([SCORES.get(i, 0) for i, _ in x])


def run(filename):
    x = [process_line(line) for line in get_lines(filename)]
    scores = [calculate_score(i) for _, i in x]
    scores = sorted([_ for _ in scores if _])

    return scores[len(scores) / 2]


# print(run("./10t.txt"))
print(run("./10.txt"))
