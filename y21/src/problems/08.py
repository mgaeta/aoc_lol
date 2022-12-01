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


def count_line(input, output):
    return sum([1 for y in output if len(y) in [2, 3, 4, 7]])


def get_bits(input):
    for i in input:
        if len(i) == 7:
            # string_8 = i
            string_8 = set(sorted(i))
        elif len(i) == 2:
            # string_8 = i
            string_1 = set(sorted(i))
        elif len(i) == 3:
            # string_8 = i
            string_7 = set(sorted(i))
        elif len(i) == 4:
            # string_8 = i
            string_4 = set(sorted(i))

    return string_1, string_4, string_7, string_8, string_4 - string_1


def get_value(
    y,
    string_1,
    string_4,
    string_7,
    string_8,
    the_ell,
):
    if len(y) == 2:
        return 1

    elif len(y) == 4:
        return 4

    elif len(y) == 3:
        return 7

    elif len(y) == 5:
        if string_1.intersection(y) == string_1:
            return 3
        elif the_ell.intersection(y) == the_ell:
            return 5
        else:
            return 2

    elif len(y) == 6:
        if string_1.intersection(y) != string_1:
            return 6
        elif string_4.intersection(y) != string_4:
            return 0
        else:
            return 9

    elif len(y) == 7:
        return 8


def get_digits(input, output):
    bits = get_bits(input)
    return int("".join([str(get_value(y, *bits)) for y in output]))


def run(filename):
    inputs = get_lines(filename)
    xx = [split_to_inputs_outputs(line) for line in inputs]
    return sum([get_digits(input, output) for input, output in xx])


# print(run("./8_test.txt"))
print(run("./8.txt"))
