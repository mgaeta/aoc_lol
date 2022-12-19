from y22.src.utils import io


def main():
    current_day = io.get_day()
    for test in [False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        data = parse_input(raw_input)
        print(simulate(data))


def simulate(data):
    output = 0

    for row in data:
        output += 1
    return output


def parse_input(raw_data):
    output = []
    for row in raw_data:
        if row == "":
            continue

        output.append(row)
    return output


if __name__ == "__main__":
    main()
