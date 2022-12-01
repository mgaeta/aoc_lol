from datetime import datetime
from pytz import timezone
import requests
import os


from y22.src.constants import AOC_ROOT, BASE_URL, TOKEN_FILE


def get_input_filename(year: int, day: int) -> str:
    path = f"{AOC_ROOT}/{year_to_directory(year)}/inputs/"

    # Ensure path exists.
    if not os.path.isdir(path):
        os.mkdir(path)

    return f"{path}/{day_to_input_filename(day)}.txt"


def get_inputs(file):
    with open(file, "r") as f:
        return [_ for _ in f.read().split("\n") if _]


def year_to_directory(year: int) -> str:
    return f"y{str(year)[2:]}"


def day_to_input_filename(day: int) -> str:
    prefix = "" if day > 10 else "0"
    return f"{prefix}{day}"


def download_input(day: int, year: int = 2022) -> str:
    source_url = f"{BASE_URL}/{year}/day/{day}/input"
    destination_file = get_input_filename(year, day)

    # Get token from file.
    cookies = {}
    with open(TOKEN_FILE, 'r') as f:
        cookies["session"] = f.readline()

    # Read
    response = requests.get(source_url, cookies=cookies)

    # Write
    with open(destination_file, 'w') as f:
        f.write(response.content.decode("utf-8"))

    return destination_file


def get_day(args_day: int) -> int:
    if not args_day:
        # Infer today's day.
        return datetime.now(timezone('EST')).day

    if 0 < args_day <= 25:
        return args_day

    raise Exception(f"invalid day: {args_day}")
