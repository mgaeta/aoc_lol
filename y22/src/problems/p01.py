from y22.src.utils import io



def main():
    filename = io.get_input_filename(2022, 1, test=False)
    raw_input = io.get_inputs_raw(filename)
    print(calories(raw_input))


COUNT = 3


def calories(raw_input):
    totals = []
    current = 0
    for i in raw_input:
        if i == "":
            totals.append(current)
            current = 0
        else:
            current += int(i)
    totals.append(current)

    totals.sort()

    topmost = totals[-COUNT:]
    return sum(topmost)


if __name__ == "__main__":
    main()
