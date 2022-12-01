def get_inputs(file):
    with open(file, "r") as f:
        return [_ for _ in f.read().split("\n") if _]


def get_integer_inputs(file):
    return [int(_) for _ in get_inputs(file)]


def get_str_inputs(file):
    return [str(_) for _ in get_inputs(file)]
