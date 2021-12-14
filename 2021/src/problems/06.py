import re
from collections import defaultdict


def get_inputs(file):
	with open(file, "r") as f:
		return [_ for _ in f.read().split("\n") if _]

def get_integer_inputs(file):
	return [int(_) for _ in get_inputs(file)]

def get_str_inputs(file):
	return [str(_) for _ in get_inputs(file)]

N = 256

def simulate_day(fishes):
	output = []
	for fish in fishes:
		if fish == 0:
			output.append(8)
			output.append(6)
		else:
			output.append(fish - 1)
	return output

def simulate_day_2(histogram):
	output = defaultdict(int)
	for key, count in histogram.items():
		if key == 0:
			output[8] += count
			output[6] += count
		else:
			output[key-1] += count
	return output


def get_histogram(fishes):
	output = defaultdict(int)
	for fish in fishes:
		output[fish] += 1
	return output


def fishies(file):
	inputs = get_inputs(file)

	fishes = [int(_) for _ in inputs[0].split(",")] 
	histogram = get_histogram(fishes)
	for i in range(N):
		histogram = simulate_day_2(histogram)

	return sum(histogram.values())
	



# TODO MARCOS take command line args to do test mode
# print(play("./inputs/6_test.txt"))
print(play("./inputs/6.txt"))
print("done")
