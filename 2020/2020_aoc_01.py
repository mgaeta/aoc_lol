def get_inputs(file):
	with open(file, "r") as f:
		return [_ for _ in f.read().split() if _]


def get_integer_inputs(file):
	return [int(_) for _ in get_inputs(file)]




def find_matches(file):
	x = 0
	old_sum = None

	xx = get_integer_inputs(file)
	i = 0
	while i < len(xx) - 2:
		new_sum = xx[i] + xx[i + 1] +  xx[i + 2] 

		if old_sum is not None and new_sum > old_sum:
			x = x + 1
		old_sum = new_sum	
		i +=1
	return x


print(find_matches("./inputs/1.txt"))
print("done")
