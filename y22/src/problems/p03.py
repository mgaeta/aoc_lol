from y22.src.utils import io


def main():
    current_day = io.get_day()

    for test in [True, False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        print(luggage2(raw_input))


POINTS = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
    "i": 9,
    "j": 10,
    "k": 11,
    "l": 12,
    "m": 13,
    "n": 14,
    "o": 15,
    "p": 16,
    "q": 17,
    "r": 18,
    "s": 19,
    "t": 20,
    "u": 21,
    "v": 22,
    "w": 23,
    "x": 24,
    "y": 25,
    "z": 26,
    "A": 26 + 1,
    "B": 26 + 2,
    "C": 26 + 3,
    "D": 26 + 4,
    "E": 26 + 5,
    "F": 26 + 6,
    "G": 26 + 7,
    "H": 26 + 8,
    "I": 26 + 9,
    "J": 26 + 10,
    "K": 26 + 11,
    "L": 26 + 12,
    "M": 26 + 13,
    "N": 26 + 14,
    "O": 26 + 15,
    "P": 26 + 16,
    "Q": 26 + 17,
    "R": 26 + 18,
    "S": 26 + 19,
    "T": 26 + 20,
    "U": 26 + 21,
    "V": 26 + 22,
    "W": 26 + 23,
    "X": 26 + 24,
    "Y": 26 + 25,
    "Z": 26 + 26,
}


def luggage2(raw_input):
    total = 0
    current: set[str] | None = None
    for i, row in enumerate(raw_input):
        if row == "":
            total += POINTS[current.pop()]
        else:
            next = set(list(row))
            if i % 3 == 0:
                if i > 0:
                    total += POINTS[current.pop()]
                current = next
            else:
                current = current.intersection(next)
    return total


def luggage1(raw_input):
    total = 0

    for row in raw_input:
        if row == "":
            continue
        pivot = int(len(row) / 2)

        first = set(list(row)[:pivot])
        second = set(list(row)[pivot:])

        total += POINTS[first.intersection(second).pop()]

    return total


if __name__ == "__main__":
    main()
