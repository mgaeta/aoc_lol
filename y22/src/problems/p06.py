from y22.src.utils import io

# COUNT = 4
COUNT = 14


def main():
    current_day = io.get_day()

    for test in [True, False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        print(communication(raw_input, COUNT))


def communication(raw_input, count):
    code = raw_input[0]
    for i in range(len(code[count - 1:])):
        if len(set(code[i: i + count])) == count:
            return i + count
    raise Exception("didn't find subsequence.")


if __name__ == "__main__":
    main()
