import argparse

from y22.src.utils import io


def get_args():
    parser = argparse.ArgumentParser(
        prog='Advent of Code Runner',
        description='Tools for better hacking',
        epilog=':D'
    )
    parser.add_argument('-t', '--test', action='store_true')
    parser.add_argument('-i', '--inputs', action='store_true')
    parser.add_argument('-d', '--day', type=int)
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    current_day = io.get_day(args.day)

    if args.inputs:
        destination = io.download_input(current_day)
        print(f"Downloaded inputs to '{destination}'.")
        exit()

    print("Day:", current_day)
    print("Test:", args.test)

