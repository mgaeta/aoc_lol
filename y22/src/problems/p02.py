import math

from y22.src.utils import io


def main():
    current_day = io.get_day()
    filename_test = io.get_input_filename(2022, current_day, test=True)
    raw_input_test = io.get_inputs_raw(filename_test)
    filename = io.get_input_filename(2022, current_day, test=False)
    raw_input = io.get_inputs_raw(filename)

    print(roshambo2(raw_input_test))
    print(roshambo2(raw_input))


def roshambo2(raw_input):
    total = 0

    for row in raw_input:
        x = row.split(" ")
        opponent = x[0]
        outcome = x[1]

        total += {
            "X": 0,
            "Y": 3,
            "Z": 6,
        }[outcome]

        if opponent == "A":
            throw = {
                "X": "Z",
                "Y": "X",
                "Z": "Y",
            }[outcome]
        if opponent == "B":
            throw = {
                "X": "X",
                "Y": "Y",
                "Z": "Z",
            }[outcome]
        if opponent == "C":
            throw = {
                "X": "Y",
                "Y": "Z",
                "Z": "X",
            }[outcome]

        total += {
            "X": 1,
            "Y": 2,
            "Z": 3,
        }[throw]

    return total


def roshambo1(raw_input):
    total = 0
    for row in raw_input:
        x = row.split(" ")
        opponent = x[0]
        throw = x[1]

        total += {
            "X": 1,
            "Y": 2,
            "Z": 3,
        }[throw]

        if opponent == "A":
            total += {
                "X": 3,
                "Y": 6,
                "Z": 0,
            }[throw]
        if opponent == "B":
            total += {
                "X": 0,
                "Y": 3,
                "Z": 6,
            }[throw]
        if opponent == "C":
            total += {
                "X": 6,
                "Y": 0,
                "Z": 3,
            }[throw]

    return total


if __name__ == "__main__":
    main()
