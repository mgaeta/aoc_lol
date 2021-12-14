from collections import defaultdict
def get_inputs(file):
	with open(file, "r") as f:
		return [_ for _ in f.read().split("\n") if _]


def get_integer_inputs(file):
	return [int(_) for _ in get_inputs(file)]

def get_str_inputs(file):
	return [str(_) for _ in get_inputs(file)]


def split_input(input_line):
	lol = input_line.split(" ")
	if len(lol) >= 2:
		return lol[0], int(lol[1])
	return None

def diagnose(file):
	COUNT = 12
	xx = get_str_inputs(file)
	

	new_xx = get_str_inputs(file)
	new_yy = get_str_inputs(file)
	index = 0
	while index < COUNT:
		buffer_x = set()
		buffer_y = set()

		#  most popular
		dx = 0
		for row_str in new_xx:
			val = row_str[index]
			if val == "1":
				dx += 1

		# least popular
		dy = 0
		for row_str in new_yy:
			val = row_str[index]
			if val == "1":
				dy += 1


		if dx >= (len(new_xx)/2):
			most_popular_x = "1"
			least_popular_x = "0"
		else:
			most_popular_x = "0"
			least_popular_x = "1"

		if dy >= (len(new_yy)/2):
			most_popular_y = "1"
			least_popular_y = "0"
		else:
			most_popular_y = "0"
			least_popular_y = "1"


		if len(new_xx) == 1:
			buffer_x = new_xx
		else:
			for x in new_xx:
				if x[index] == most_popular_x:
					buffer_x.add(x)

		if len(new_yy) == 1:
			buffer_y = new_yy
		else:
			for y in new_yy:
				if y[index] == least_popular_y:
					buffer_y.add(y)

		new_xx = buffer_x
		new_yy = buffer_y

		index += 1
	delta = int(new_xx.pop(), 2)
	epsilon = int(new_yy.pop(), 2)
	return delta * epsilon


print(diagnose("./inputs/3.txt"))
print("done")
