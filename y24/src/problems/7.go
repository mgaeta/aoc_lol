package problems

import (
	"fmt"
	"strconv"
	"strings"
	"y24/src/utils"
)

func Solve7a(data string, verbose bool) string {
	output := 0
	lines := utils.GetStrings(data)
	for _, line := range lines {
		testValue, values, err := parseLine(line)
		if err != nil {
			panic(err)
		}
		if isValid(testValue, values, verbose) {
			if verbose {
				fmt.Println(testValue)
			}
			output += testValue
		}
	}

	return strconv.Itoa(output)
}

func isValid(expected int, inputs []int, verbose bool) bool {
	if verbose {
		fmt.Println("expected", expected, "inputs", inputs)
	}
	if len(inputs) == 1 {
		return inputs[0] == expected
	}

	// We're assuming none of the values are zero
	firstValue := inputs[0]

	// if we can be in multiply
	if expected%firstValue == 0 && expected >= firstValue {
		canBeMult := isValid(expected/firstValue, inputs[1:], verbose)
		if canBeMult {
			return true
		}
	}

	if expected > firstValue {
		return isValid(expected-firstValue, inputs[1:], verbose)
	}

	return false
}

func isValid2(expected int, inputs []int, verbose bool) bool {
	if verbose {
		fmt.Println("expected", expected, "inputs", inputs)
	}
	if len(inputs) == 1 {
		return inputs[0] == expected
	}

	// We're assuming none of the values are zero
	firstValue := inputs[0]

	// if we can be in multiply
	if expected%firstValue == 0 && expected >= firstValue {
		canBeMult := isValid2(expected/firstValue, inputs[1:], verbose)
		if canBeMult {
			return true
		}
	}

	// if we can add
	if expected > firstValue {
		canBeAdd := isValid2(expected-firstValue, inputs[1:], verbose)
		if canBeAdd {
			return true
		}
	}

	// if we can concat
	if len(inputs) >= 2 {
		result, err := quickCut(expected, firstValue)
		if verbose {
			fmt.Println("attempting cut", expected, firstValue, result, err)
		}
		if err == nil {
			return isValid2(result, inputs[1:], verbose)
		}
	}

	return false
}

func quickCut(a int, b int) (int, error) {
	aString := strconv.Itoa(a)
	bString := strconv.Itoa(b)

	delta := len(aString) - len(bString)

	if delta < 0 {
		return 0, fmt.Errorf("didn't fit")
	}
	suffix := aString[delta:]
	if suffix != bString {
		return 0, fmt.Errorf("didn't match")
	}

	return strconv.Atoi(aString[:delta])
}

func parseLine(line string) (int, []int, error) {
	parts := strings.Split(line, ": ")
	testValue, err := strconv.Atoi(parts[0])
	if err != nil {
		return 0, nil, err
	}
	values := make([]int, 0)
	for _, vString := range strings.Split(parts[1], " ") {
		v, err := strconv.Atoi(vString)
		if err != nil {
			return 0, nil, err
		}
		values = append([]int{v}, values...)
	}

	return testValue, values, nil
}

func Solve7b(data string, verbose bool) string {
	output := 0
	lines := utils.GetStrings(data)
	for _, line := range lines {
		testValue, values, err := parseLine(line)
		if err != nil {
			panic(err)
		}
		if isValid2(testValue, values, verbose) {
			if verbose {
				fmt.Println("adding", testValue)
			}
			output += testValue
		}
	}

	return strconv.Itoa(output)
}
