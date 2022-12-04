from y22.src.utils import io


def main():
    current_day = io.get_day()

    for test in [True, False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        print(overlap1(raw_input))


def overlap2(raw_input):
    total = 0
    for i, row in enumerate(raw_input):
        if row == "":
            continue
        first, second = row.split(",")
        fstart, fend = first.split("-")
        sstart, send = second.split("-")

        fstart = int(fstart)
        fend = int(fend)
        sstart = int(sstart)
        send = int(send)

        if (fend < sstart) or (fstart > send):
            total += 1
    return len(raw_input) - total


def overlap1(raw_input):
    total = 0
    for i, row in enumerate(raw_input):
        if row == "":
            continue
        first, second = row.split(",")
        fstart, fend = first.split("-")
        sstart, send = second.split("-")

        fstart = int(fstart)
        fend = int(fend)
        sstart = int(sstart)
        send = int(send)

        if (
            (fstart >= sstart and fend <= send)
            or (sstart >= fstart and send <= fend)
        ):
            total += 1
    return total


if __name__ == "__main__":
    main()
