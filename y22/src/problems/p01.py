from y22.src.utils import io, parse


def main():
    filename = io.get_input_filename(2022, 1)
    print(parse.get_integer_inputs(filename))


if __name__ == "__main__":
    main()
