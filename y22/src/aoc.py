import argparse
import configparser

from y22.src.constants import CONFIG_FILE
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
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        destination = io.download_input(dict(config['secrets']), current_day)
        print(f"Downloaded inputs to '{destination}'.")
        exit()

    print("Day:", current_day)
    print("Test:", args.test)

