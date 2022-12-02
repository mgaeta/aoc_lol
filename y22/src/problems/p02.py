from y22.src.utils import io


def main():
    current_day = io.get_day()

    for test in [True, False]:
        filename = io.get_input_filename(2022, current_day, test=test)
        raw_input = io.get_inputs_raw(filename)
        print(roshambo2(raw_input))


def roshambo2(raw_input):
    total = 0

    for row in raw_input:
        opponent, outcome = row.split(" ")

        total += {
            "X": 0,
            "Y": 3,
            "Z": 6,
        }[outcome]

        throw = {
            "A": {
                "X": "Z",
                "Y": "X",
                "Z": "Y",
            },
            "B": {
                "X": "X",
                "Y": "Y",
                "Z": "Z",
            },
            "C": {
                "X": "Y",
                "Y": "Z",
                "Z": "X",
            },
        }[opponent][outcome]

        total += {
            "X": 1,
            "Y": 2,
            "Z": 3,
        }[throw]

    return total


def roshambo1(raw_input):
    total = 0
    for row in raw_input:
        opponent, throw = row.split(" ")

        total += {
            "X": 1,
            "Y": 2,
            "Z": 3,
        }[throw]

        total += {
            "A": {
                "X": 3,
                "Y": 6,
                "Z": 0,
            },
            "B": {
                "X": 0,
                "Y": 3,
                "Z": 6,
            },
            "C": {
                "X": 6,
                "Y": 0,
                "Z": 3,
            }
        }[opponent][throw]

    return total


if __name__ == "__main__":
    main()
