from collections import defaultdict


def get_inputs(file):
	with open(file, "r") as f:
		return [_ for _ in f.read().split("\n\n") if _]


def get_integer_inputs(file):
	return [int(_) for _ in get_inputs(file)]

def get_str_inputs(file):
	return [str(_) for _ in get_inputs(file)]

def parse_board(board):
	return [
		int(cell)
		for row in board.split("\n")
		for cell in row.strip().split()
	]

def get_all_unmarked_sum(board, sub_list):
	return sum([
		cell 
		for cell in board 
		if cell not in sub_list
	])

def is_a_bingo(board, sub_list):
	return any([
		all([
			board[column * a + row * b] in sub_list 
			for column in range(5)
		])
		for (a, b) in [(1, 5), (5, 1)]
		for row in range(5)
	])


def play(file):
	boards = get_inputs(file)
	full_list = [int(_) for _ in boards.pop(0).split(",")]
	boards = [parse_board(b) for b in boards]

	done_boards = set()
	for i in range(len(full_list)):
		sub_list = full_list[:i]
		for n, board in enumerate(boards):
			if n not in done_boards and is_a_bingo(board, sub_list):
				done_boards.add(n)
				if len(done_boards) == len(boards):
					return get_all_unmarked_sum(board, sub_list) * full_list[i-1]
	return None

# TODO MARCOS take command line args to do test mode
# print(play("./inputs/4_test.txt"))
print(play("./inputs/4.txt"))
print("done")
