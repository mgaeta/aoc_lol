import copy
from collections import defaultdict


def get_inputs(file):
    with open(file, "r") as f:
        return [_ for _ in f.read().split("\n") if _]


def get_integer_inputs(file):
    return [int(_) for _ in get_inputs(file)]


def get_str_inputs(file):
    return [str(_) for _ in get_inputs(file)]


DUPLICATE_KEY = "xxxxxxxxx"


def recurse(start_key, all_paths, path_so_far, dup_cave):
    if start_key == "end":
        return set([path_so_far.replace(DUPLICATE_KEY, dup_cave)])

    paths_copy = copy.deepcopy(all_paths)
    available_keys = paths_copy.get(start_key, set())

    if not start_key.isupper() and start_key in paths_copy:
        del paths_copy[start_key]

    output = set()
    for next_key in available_keys:
        output |= recurse(next_key, paths_copy, f"{path_so_far}-{next_key}", dup_cave)

    return output


def get_all_paths(file):
    inputs = [_.split("-") for _ in get_inputs(file)]

    all_paths = defaultdict(set)
    for a, b in inputs:
        all_paths[a].add(b)
        all_paths[b].add(a)
    return all_paths


def get_small_caves(all_paths):
    output = set(k for k in all_paths if not k.isupper())
    output.remove("start")
    output.remove("end")
    return output


def count_paths(file):
    all_paths = get_all_paths(file)

    outputs = set()
    for small_cave in get_small_caves(all_paths):
        all_paths_copy = copy.deepcopy(all_paths)
        connections = all_paths_copy[small_cave]
        all_paths_copy[DUPLICATE_KEY] = copy.deepcopy(connections)
        for connection in connections:
            all_paths_copy[connection].add(DUPLICATE_KEY)

        outputs |= recurse("start", all_paths_copy, "start", small_cave)
    return len(outputs)


# print(count_paths("./inputs/12tt.txt"))
# print(count_paths("./inputs/12t.txt"))
print(count_paths("./inputs/12.txt"))
print("done")
