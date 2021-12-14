import re
from collections import defaultdict


def get_inputs(file):
	with open(file, "r") as f:
		return [_ for _ in f.read().split("\n") if _]

def get_integer_inputs(file):
	return [int(_) for _ in get_inputs(file)]

def get_str_inputs(file):
	return [str(_) for _ in get_inputs(file)]

def is_valid(line):
	(x0, y0, x1, y1) = line
	return (x0 == x1) or (y0 == y1) or (abs(x1 - x0) == abs(y1 - y0))

REGEX = r"(\d+),(\d+) -> (\d+),(\d+)"

def get_lines(ll):
	return [tuple(int(c) for c in re.findall(REGEX, l)[0]) for l in ll]

def count_board(board):
	return len([value for value in board.values() if value > 1])

def fill_board(lines):
	board = defaultdict(int)
	for x0, y0, x1, y1 in lines:
		x_inc = int((x1 - x0)/(abs(x0 - x1) or 1))
		y_inc = int((y1 - y0)/(abs(y0 - y1) or 1))
		length = abs(x1 - x0) or abs(y1 - y0)
		for i in range(length + 1):
			board[x0 + x_inc * i, y0 + y_inc * i] += 1			

	return board

def play(file):
	inputs = get_inputs(file)
	lines = [line for line in get_lines(inputs) if is_valid(line)]
	board = fill_board(lines)
	return count_board(board)

# TODO MARCOS take command line args to do test mode
# print(play("./inputs/5_test.txt"))
print(play("./inputs/5.txt"))
print("done")
