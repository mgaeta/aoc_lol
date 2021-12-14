import re
import copy
from collections import defaultdict


def get_inputs(file):
	with open(file, "r") as f:
		return [_ for _ in f.read().split("\n\n") if _]


def get_template_and_rules(file):
	inputs = "".join([_ for _ in get_inputs(file)])
	template = [_ for _ in inputs[0]]	
	rules = {
		x[0]: x[1]
		for x in [
			x.split(" -> ") 
			for x in inputs[1].split("\n")
		] 
		if len(x) == 2 
	}
	return template, rules

def step_1(template, rules):
	output = ""
	for i in range(len(template) - 1):
		a = template[i]
		b = template[i+1]

		output += a
		found = rules.get(f"{a}{b}")
		if found:
			output += found
	return output + template[-1]

# (template, steps) -> counts
memo = {}

def recurse(template, rules, steps_remaining):
	found = memo.get((template, steps_remaining))
	if found:
		return found

	if steps_remaining == 0:
		final_answer = histogram(template)
	else:
		final_answer = defaultdict(int)
		for i in range(len(template) - 1):
			z = step_1(f"{template[i]}{template[i+1]}", rules)
			for k, v in recurse(z, rules, steps_remaining - 1).items():
				final_answer[k] += v
			final_answer[z[-1]] -= 1
		final_answer[template[-1]] += 1

	memo[(template, steps_remaining)] = final_answer
	return final_answer

def histogram(template):
	h = defaultdict(int)
	for i in template:
		h[i] += 1
	return h

def polymerize(file):
	template, rules = get_template_and_rules(file)
	h = recurse(template, rules, 40)
	return max(h.values()) - min(h.values())


# TODO MARCOS take command line args to do test mode
# print(polymerize("./inputs/14tt.txt"))
# print(polymerize("./inputs/14t.txt"))
print(polymerize("./inputs/14.txt"))
print("done")
