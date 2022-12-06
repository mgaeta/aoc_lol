from y22.src.utils import io

COUNT = 14


def main():
    current_day = io.get_day()

    for test in [True, False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        print(communication(raw_input, COUNT))


def communication(raw_input, count):
    i = count - 1
    while i < len(raw_input[0]):
        char = raw_input[0][i]
        previous = set()

        for j in range(count - 1):
            previous.add(raw_input[0][i - j - 1])
        if len(previous) == count - 1 and char not in previous:
            return i+1
        i += 1
    raise Exception("didn't find subsequence.")


if __name__ == "__main__":
    main()
