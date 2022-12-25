from y22.src.utils import io

I_TO_X = list("210-=")
X_TO_I = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}


def main():
    current_day = io.get_day()
    for test in [False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        data = parse_input(raw_input)
        print(simulate(data))


def simulate(data):
    return i_to_x(sum(x_to_i(snafu) for snafu in data))


def i_to_x(v: int) -> str:
    if v <= 0:
        return ""

    i = 0
    while 5 ** i < v:
        i += 1

    return i_to_x((v + 2) // 5) + I_TO_X[(2 - v) % 5]


def x_to_i(number: str) -> int:
    return sum(
        (5 ** (len(number) - i - 1) * X_TO_I[v])
        for i, v in enumerate(list(number))
    )


def parse_input(raw_data):
    output = []
    for row in raw_data:
        if row == "":
            continue

        output.append(row)
    return output


if __name__ == "__main__":
    main()
