import re
from collections import defaultdict


def get_inputs(file):
	with open(file, "r") as f:
		return [_ for _ in f.read().split("\n") if _]

def get_integer_inputs(file):
	return [int(_) for _ in get_inputs(file)]

def get_str_inputs(file):
	return [str(_) for _ in get_inputs(file)]

def crab_army(file):
	ii = [int(_) for _ in get_inputs(file)[0].split(",")]
	return min([
		sum([int((abs(i - p)) * (abs(i - p) + 1) /2) for i in ii])
		for p in range(min(ii), max(ii))
	])

def crab_army(file):
	inputs = [int(_) for _ in get_inputs(file)[0].split(",")]
	minimum = None
	for pivot in range(min(inputs), max(inputs)):
		fuel = 0
		for i in inputs:
			distance = abs(i - pivot)
			fuel += int(distance * (distance + 1) /2)

		if not minimum or minimum > fuel:
			minimum = fuel

	return minimum


# TODO MARCOS take command line args to do test mode
# print(crab_army("./inputs/7_test.txt"))
print(crab_army("./inputs/7.txt"))
print("done")
